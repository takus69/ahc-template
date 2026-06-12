import argparse
import datetime
import json
import multiprocessing
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import numpy as np
import pandas as pd


BIN_PATH = r".\target\release\ahc066.exe"
INPUT_DIR = Path("in")
OUTPUT_DIR = Path("out")
DEFAULT_RESULT_CSV = Path("result.csv")
DEFAULT_TRIAL = 150


def parse_env_args(env_args: List[str]) -> Dict[str, str]:
    """Parse --env KEY=VALUE arguments."""
    env: Dict[str, str] = {}
    for item in env_args:
        if "=" not in item:
            raise ValueError(f"--env must be KEY=VALUE format: {item}")
        key, value = item.split("=", 1)
        key = key.strip()
        if not key:
            raise ValueError(f"--env key is empty: {item}")
        env[key] = value
    return env


def parse_result(stderr: str) -> dict:
    """
    Read result JSON from stderr.

    The solver must print at least one JSON line containing `score` to stderr.
    Debug output may be mixed in, so this searches from the end.
    """
    for line in reversed(stderr.splitlines()):
        s = line.strip()
        if s.startswith("{") and s.endswith("}"):
            result = json.loads(s)
            if "score" not in result:
                raise ValueError(f"result JSON must contain score: {result}")
            return result
    raise ValueError(f"result JSON not found in stderr:\n{stderr}")


def run_solver(seed: int, extra_env: Dict[str, str]) -> dict:
    input_path = INPUT_DIR / f"{seed:04}.txt"
    output_path = OUTPUT_DIR / f"{seed:04}.txt"

    if not input_path.exists():
        raise FileNotFoundError(f"input file not found: {input_path}")

    OUTPUT_DIR.mkdir(exist_ok=True)

    env = os.environ.copy()
    env.update(extra_env)

    cmd = f"powershell cat {input_path} | {BIN_PATH} > {output_path}"
    completed = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        env=env,
    )
    return parse_result(completed.stderr)


def run_one(args: Tuple[int, Dict[str, str]]) -> dict:
    seed, extra_env = args
    start = time.time()
    result = run_solver(seed, extra_env)
    elapsed = round(time.time() - start, 4)

    data = {
        "i": seed,
        "score": result["score"],
        "time": elapsed,
    }

    # Add every additional result JSON field as a CSV column.
    for key, value in result.items():
        if key not in data:
            data[key] = value

    return data


def make_seed_list(start: int, end: int | None, trial: int | None) -> List[int]:
    if end is not None:
        if end < start:
            raise ValueError(f"--end must be >= --start: start={start}, end={end}")
        return list(range(start, end + 1))

    if trial is None:
        trial = DEFAULT_TRIAL
    if trial <= 0:
        raise ValueError(f"--trial must be positive: {trial}")
    return list(range(start, start + trial))


def render_progress(done: int, total: int, width: int = 30) -> str:
    if total <= 0:
        return ""
    filled = int(width * done / total)
    bar = "#" * filled + "-" * (width - filled)
    percent = 100.0 * done / total
    return f"[{bar}] {done}/{total} {percent:5.1f}%"


def run_simulation(
    seeds: Iterable[int],
    output_csv: Path,
    jobs: int,
    extra_env: Dict[str, str],
) -> float:
    seeds = list(seeds)
    start_time = time.time()

    print("start:", datetime.datetime.fromtimestamp(start_time))
    print(f"seeds: {seeds[0]}..{seeds[-1]} ({len(seeds)} cases)")
    print(f"jobs: {jobs}")
    if extra_env:
        print("env:", ", ".join(f"{k}={v}" for k, v in sorted(extra_env.items())))

    results: List[dict] = []
    worker_args = [(seed, extra_env) for seed in seeds]

    with multiprocessing.Pool(processes=jobs) as pool:
        for data in pool.imap_unordered(run_one, worker_args):
            results.append(data)
            print("\r" + render_progress(len(results), len(seeds)), end="", flush=True)
    print()

    df = pd.DataFrame(results).sort_values("i")
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_csv, index=False)

    score_sum = int(np.sum(df["score"]))
    score_mean = float(np.mean(df["score"]))
    time_mean = float(np.mean(df["time"]))
    time_max = float(np.max(df["time"]))

    print(f"score: {score_sum:,}, score mean: {score_mean:.2f}")
    print(f"time mean: {time_mean:.4f}s, time max: {time_max:.4f}s")
    print(f"wrote: {output_csv}")
    print(f"end elapsed time: {time.time() - start_time:.2f}s")

    return score_mean


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run AHC solver for multiple seeds.")
    parser.add_argument("--trial", type=int, default=None, help="number of cases to run")
    parser.add_argument("--start", type=int, default=0, help="first seed index")
    parser.add_argument("--end", type=int, default=None, help="last seed index, inclusive")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_RESULT_CSV,
        help="output CSV path",
    )
    parser.add_argument(
        "--jobs",
        type=int,
        default=multiprocessing.cpu_count(),
        help="number of parallel worker processes",
    )
    parser.add_argument(
        "--env",
        action="append",
        default=[],
        help="extra environment variable in KEY=VALUE format; can be repeated",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.jobs <= 0:
        raise ValueError(f"--jobs must be positive: {args.jobs}")

    seeds = make_seed_list(args.start, args.end, args.trial)
    extra_env = parse_env_args(args.env)
    run_simulation(seeds, args.output, args.jobs, extra_env)


if __name__ == "__main__":
    main()
