use crate::{json_string, Solver};

pub(crate) fn collect(solver: &Solver) -> Vec<(&'static str, String)> {
    let mut extra = Vec::new();

    // analysis feature付きビルド時だけCSV列に追加したい値を書く。
    // valueはJSON値としてそのまま埋め込む。
    //
    // 数値: 123.to_string()
    // bool: true.to_string()
    // 文字列: json_string("text")
    //
    // 通常ビルド cargo build --release では、このファイルは使われない。

    extra.push(("analysis_enabled", true.to_string()));
    extra.push(("analysis_note", json_string("placeholder")));

    // 例:
    // extra.push(("analysis_score", solver.score.to_string()));
    // extra.push(("analysis_answer_len", solver.answer.len().to_string()));

    let _ = solver;

    extra
}
