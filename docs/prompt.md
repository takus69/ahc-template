# prompt.md

このファイルは、ChatGPT UIで使うプロンプトテンプレートを管理する。
共通ルールは各プロンプト内に直接書く。
現在状態は`state.md`を唯一の正とする。

---

## 1. problem.md 作成プロンプト

```text
AHCプロジェクトです。

役割: Strategist

AGENTS.mdに従って作業してください。
ChatGPT UI前提で、人間がローカル実行・提出・コミットを行います。
現在渡したファイルを唯一の正として扱ってください。
古い会話中のコード・数値・方針をベースにしないでください。

まず以下を読んでください。

- AGENTS.md
- problem.html

目的:
problem.html をもとに、problem.md のたたき台を作成してください。

重要:
- problem.mdには問題の事実のみを書く
- 仮説・解法・推測は書かない
- スコア計算式、制約、入出力形式、提供ツールを漏らさない
- 問題文と矛盾しない
- 不明な点は不明と書く

出力は problem.md にそのまま貼れる形式にしてください。
```

---

## 2. problem.md 確認プロンプト

```text
AHCプロジェクトです。

役割: Strategist

AGENTS.mdに従って作業してください。
ChatGPT UI前提で、人間がローカル実行・提出・コミットを行います。
現在渡したファイルを唯一の正として扱ってください。
古い会話中のコード・数値・方針をベースにしないでください。

まず以下を読んでください。

- AGENTS.md
- problem.html
- problem.md

目的:
problem.md を確認してください。

確認する点:
- problem.html の事実と矛盾していないか
- 制約が漏れていないか
- 入出力形式が正しいか
- スコア構造が正しく整理されているか
- 推測や仮説が混ざっていないか
- 用語の定義が曖昧でないか

問題があれば修正案を出してください。
```

---

## 3. Strategist 初期・引継ぎプロンプト

```text
AHCプロジェクトです。

役割: Strategist

AGENTS.mdに従って作業してください。
ChatGPT UI前提で、人間がローカル実行・提出・コミットを行います。

現在状態は state.md を唯一の正として扱ってください。
現在渡したファイルを唯一の正として扱ってください。
古い会話中のコード・数値・方針をベースにしないでください。

まず以下を読んでください。

- AGENTS.md
- state.md
- problem.md
- strategy.md
- evaluation.md
- scoreboard.md
- todo.md
- src/main.rs
- simulator.py
- cmd.md

## 直近の実験・判断要約

ここに必要な直近実験・判断を文章で書く。
experiments.mdの直近部分を別途渡す運用にはしない。

## 今回の目的

- 現在状態を確認する
- 必要に応じて方針を整理する
- todo.md先頭TODOの完了 / 継続 / 撤退を判断する
- 必要なら todo.md 修正案、state.md 更新案、experiments.md 記録案を出す
- 次にImplementerへ依頼する場合は、todo.mdを渡さずに済む実装プロンプトを作成する
```

---

## 4. Implementerプロンプト生成用テンプレート

このテンプレートは、人間が直接使うものではなく、StrategistがImplementer向けプロンプトを生成するときの型として使う。
Implementerには`todo.md`を渡さない。TODO内容はプロンプト本文に展開する。

```text
AHCプロジェクトです。

役割: Implementer

AGENTS.mdに従って作業してください。
ChatGPT UI前提で、人間がローカルでコンパイル・実行・simulator.py実行・提出・コミットを行います。

現在渡したファイルを唯一の正として扱ってください。
古い会話中のコード・数値・方針をベースにしないでください。

まず以下を読んでください。

- AGENTS.md
- problem.md
- strategy.md
- evaluation.md
- state.md
- cmd.md
- Cargo.toml
- src/main.rs
- simulator.py

今回の実装対象は、Strategistが展開した以下のTODOのみです。
todo.mdは渡していません。
ここに書かれた内容以外は実装しないでください。

## 実装TODO

### 目的

...

### 内容

...

### 変更対象

...

### 確認方法

...

### 注意点

...

## 出力してほしいもの

- 変更概要
- 修正後コードまたは差分
- 確認手順
- リスク
- コミットメッセージ案
```

## 5. Visualizer作成プロンプト

```text
AHCプロジェクトです。

役割: Implementer

AGENTS.mdに従って作業してください。
ChatGPT UI前提で、人間がローカル実行・提出・コミットを行います。
現在渡したファイルを唯一の正として扱ってください。
古い会話中のコード・数値・方針をベースにしないでください。

まず以下を読んでください。

- AGENTS.md
- problem.md
- visualizer.html

目的:
visualizer.htmlをベースに、この問題用の簡易Visualizerを作成してください。

方針:
- 既存のUI構造はできるだけ維持する
- 問題ごとに必要な部分だけ差し替える
- 最初から完璧に作り込まず、Input / Outputを貼り付けて挙動確認できる状態を優先する
- 最低限、最終状態を描画できるようにする
- 可能ならターンごとの状態も確認できるようにする

主に差し替える関数:
- parseInput
- parseOutput
- buildStates
- drawTurn

最低限ほしい機能:
- Input貼り付け欄
- Output貼り付け欄
- Visualizeボタン
- canvas描画
- scoreまたは評価値表示
- パースエラー表示

可能なら追加する機能:
- turnスライダー
- 前後移動ボタン
- 現在ターンの操作内容
- valid / invalid表示
- 累積スコア
- 直前差分
- before / after比較

出力してほしいもの:
- 修正後のvisualizer.html全文
- 変更概要
- 使い方
- まだ未対応の点
```
