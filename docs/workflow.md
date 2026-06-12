# workflow.md

このドキュメントは、AHC参加中のChatGPT UI運用手順を定義する。

---

## 基本原則

* ChatGPT UIで考察・実装案作成・実験結果分析を行う。
* ローカル実行、提出、コミットは人間が行う。
* 現在状態は`state.md`を唯一の正とする。
* 実装は`todo.md`に基づいて行う。
* `todo.md`は未完了TODOを優先順に並べる。
* 完了したTODOは`todo.md`から削除する。
* Implementerには`todo.md`を直接渡さない。
* Strategistが`todo.md`先頭TODOを展開してImplementer向けプロンプトを作る。
* 実験結果は`experiments.md`に短く記録する。
* 提出履歴は`scoreboard.md`に記録する。

---

## 開始直後の流れ

1. 問題文を`problem.html`として保存する。
2. `prompt.md`のproblem.md作成プロンプトで`problem.md`を作成する。
3. `prompt.md`のproblem.md確認プロンプトで`problem.md`を確認する。
4. `prompt.md`のVisualizer作成プロンプトで簡易`visualizer.html`を作成する。
5. 最小合法解を作成する。
6. `simulator.py`とローカル評価環境を確認する。
7. 最小合法解の出力を`visualizer.html`で確認する。
8. 初期`state.md`を作成する。
9. 初期`strategy.md`を作成する。
10. 初期`todo.md`を作成する。
11. 通常改善サイクルへ進む。

---

## 通常改善サイクル

1. Strategistが現状を確認する。
2. Strategistが`todo.md`先頭TODO、または次に実装するTODOを整理する。
3. StrategistがImplementer向けプロンプトを作成する。
4. Implementerが実装案を出す。
5. 人間がコードを反映する。
6. 人間がビルド・実行などの評価を行う。
7. 人間が結果をStrategistに共有する。
8. Strategistが結果を分析する。
9. StrategistがTODOを完了 / 継続 / 撤退のいずれかで判断する。
10. 必要に応じて`state.md`、`todo.md`、`experiments.md`、`scoreboard.md`の更新案を出す。
11. 次のTODOへ進む。

---

## Strategistの結果判断

実験結果を受け取ったStrategistは、必ず次のいずれかを明示する。

```text
判断: 完了
判断: 継続
判断: 撤退
```

### 完了

TODOの目的を達成した、または採用・不採用まで結論が出た状態。

出力するもの:

* 完了理由
* 採用 / 不採用
* `experiments.md`記録案
* `todo.md`更新案
* `state.md`更新案
* 次のTODO

### 継続

同じTODOを続ける状態。

出力するもの:

* 継続理由
* 次に確認する内容
* `todo.md`修正案、または修正なしで継続と明示
* 必要なら次のImplementer向けプロンプト

### 撤退

効果が薄い、危険、時間が重いなどでTODOを打ち切る状態。

出力するもの:

* 撤退理由
* `experiments.md`記録案
* `todo.md`更新案
* `state.md`更新案
* 次のTODO

---

## 提出時の流れ

1. 現在ローカル評価を確認する。
2. safetyを確認する。
3. 実行時間とTLEリスクを確認する。
4. コードサイズを確認する。
5. 人間がAtCoderへ提出する。
6. 提出結果を確認する。
7. `scoreboard.md`に提出履歴を1行追加する。
8. ベスト更新なら`state.md`の提出ベストを更新する。

---

## スレッド切替

* `prompt.md`のStrategist初期・引継ぎプロンプトを使う。
* 直近実験や判断の要約は、引継ぎプロンプト本文に書く。
* 引継ぎ時は、`state.md`を現在状態の唯一の正と明記する。

---

## ファイルの役割

* `AGENTS.md`: AI運用の基本ルール
* `state.md`: 現在状態の唯一の正
* `problem.md`: 問題事実
* `strategy.md`: 解法構造・設計方針
* `evaluation.md`: 評価方針
* `workflow.md`: 運用手順
* `prompt.md`: プロンプトテンプレート
* `cmd.md`: コマンド集
* `todo.md`: 未完了TODO
* `experiments.md`: 実験履歴の短い索引
* `scoreboard.md`: 提出履歴
* `simulator.py`: ローカル評価基盤
* `visualizer.html`: 簡易Visualizer
