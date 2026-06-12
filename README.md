# ahc-template

AtCoder Heuristic Contest（AHC）向けの、ChatGPT UI運用を前提にしたテンプレートリポジトリです。

このテンプレートは、AHC参加中に次の作業を安定して回すことを目的にしています。

* 問題理解
* 方針整理
* 実装
* ローカル評価
* 実験結果分析
* 提出管理
* スレッド切替時の引継ぎ
* 提出コードと分析コードの分離

## 方針

このテンプレートでは、ChatGPTを次のように使います。

* Strategist: 方針整理、実験結果分析、TODO管理、Implementer向けプロンプト作成
* Implementer: Strategistが展開した実装TODOのみを実装
* 人間: ローカル実行、提出、コミット

現在状態は `docs/state.md` を唯一の正として扱います。
実装TODOは `docs/todo.md` に未完了分だけを優先順に並べます。
実験結果は `docs/experiments.md` に短く記録し、提出履歴は `docs/scoreboard.md` に記録します。

## ディレクトリ構成

```text
.
├── Cargo.toml
├── simulator.py
├── visualizer.html
├── src/
│   ├── main.rs
│   └── analysis.rs
└── docs/
    ├── AGENTS.md
    ├── cmd.md
    ├── evaluation.md
    ├── experiments.md
    ├── problem.md
    ├── prompt.md
    ├── scoreboard.md
    ├── state.md
    ├── strategy.md
    ├── todo.md
    └── workflow.md
```

## 主要ファイル

### `docs/AGENTS.md`

ChatGPTが従う基本ルールです。

* 判断優先順位
* Strategist / Implementer の役割
* TODO運用
* 実験結果の扱い
* 提出コードと分析コードの分離
* 乱数seed方針
* 提出前確認

### `docs/state.md`

現在状態の唯一の正です。

* 提出ベスト
* 現在ローカル評価
* 現在TODO

頻繁に変わる情報はここに集約します。

### `docs/todo.md`

未完了TODOだけを優先順に並べます。

Implementerにはこのファイルを直接渡さず、Strategistが先頭TODOを展開して実装プロンプトを作ります。

### `docs/experiments.md`

実験履歴を短く記録します。

長大なログではなく、目的・結果・判断・次アクションが分かる最小限の記録にします。

### `docs/scoreboard.md`

提出履歴を記録します。

現在の提出ベストは `docs/state.md` に書き、`scoreboard.md` は履歴専用にします。

### `simulator.py`

複数seedでSolverを実行する汎用ランナーです。

* `--trial`
* `--start`
* `--end`
* `--output`
* `--jobs`
* `--env`

に対応しています。

Solverはstderrに `score` を含むJSONを出力する前提です。
`simulator.py` はstderr末尾からJSONを読み取り、JSON内の全フィールドをCSV列として保存します。

### `visualizer.html`

簡易Visualizerのテンプレートです。

問題ごとに主に次の関数を差し替えて使います。

* `parseInput`
* `parseOutput`
* `buildStates`
* `drawTurn`

### `src/main.rs`

提出候補コードのテンプレートです。

`src/main.rs` は常に提出候補として保ち、採用しない候補生成・実験専用集計・大量ログ出力は残さない方針です。

### `src/analysis.rs`

分析用コードの置き場です。

`analysis` feature付きビルド時だけ使います。

```powershell
cargo build --release --features analysis
```

通常提出ビルドでは使いません。

```powershell
cargo build --release
```

## 基本的な使い方

### 1. 問題文を保存する

AtCoderの問題文HTMLを `problem.html` として保存します。

### 2. `docs/prompt.md` のプロンプトで `docs/problem.md` を作る

`problem.md` には問題の事実だけを書きます。
仮説・解法・推測は書きません。

### 3. 簡易Visualizerを作る

`visualizer.html` を問題用に修正します。

最初から完璧に作らず、まずはInput / Outputを貼り付けて最終状態を確認できる状態を目指します。

### 4. 最小合法解を作る

`src/main.rs` に最小合法解を実装し、ローカル評価環境を確認します。

### 5. 改善サイクルを回す

通常は次の流れで進めます。

1. Strategistが `docs/todo.md` の先頭TODOを整理する
2. StrategistがImplementer向けプロンプトを作る
3. Implementerが実装案を出す
4. 人間がコードを反映する
5. 人間がビルド・実行する
6. Strategistが結果を分析する
7. Strategistが `完了 / 継続 / 撤退` を判断する
8. 必要に応じて `state.md`、`todo.md`、`experiments.md`、`scoreboard.md` を更新する

## よく使うコマンド

### build

```powershell
cargo build --release
```

### quick

```powershell
python .\simulator.py --trial 1 --output result_quick.csv
```

### daily

```powershell
python .\simulator.py --trial 150 --output result.csv
```

### 1000ケース評価

```powershell
python .\simulator.py --trial 1000 --output result_1000.csv
```

### seed範囲指定

```powershell
python .\simulator.py --start 100 --end 149 --output result_100_149.csv
```

### 分析feature付き評価

```powershell
cargo build --release --features analysis
python .\simulator.py --trial 150 --output result_analysis.csv
```

## 提出前確認

提出前は通常ビルドで評価します。

```powershell
cargo build --release
python .\simulator.py --trial 150 --output result.csv
```

確認すること:

* コンパイルできる
* stdoutが提出形式のみになっている
* stderrが提出形式を壊していない
* safetyに問題がない
* 実行時間に余裕がある
* コードサイズに問題がない
* Solver内部seedが意図通り固定されている
* 分析feature付きビルドの結果だけで提出判断していない

## 更新方針

このテンプレートは、AHC参加後の振り返りに合わせて継続的に更新します。

改善したい点が出たら、テンプレート自体に反映して次回のコンテストで使いやすくします。
