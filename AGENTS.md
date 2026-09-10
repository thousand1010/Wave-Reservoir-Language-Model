# Public Repository Guidelines / 公開リポジトリ運用指針

[日本語](#日本語) | [English](#english)

## 日本語

本リポジトリは WRLM のキュレーションされた公開ポートフォリオである。非公開ラボに
アクセスできなくても実行でき、小さく、理解できる状態に保つこと。ラボの履歴をコピーしたり、
ラボのファイルを一括エクスポートしたりしてはならない。

すべての実験は、証拠クラス (`confirmatory`、`exploratory`、`diagnostic`)、再現ティア、
正確な設定、コマンド、簡潔な結果、限界、ソースの来歴を明示しなければならない。
プリミティブの診断に成功したことは、システムレベルの主張や機構に関する主張を許可しない。

トピックブランチとプルリクエストを使うこと。`main` を実行可能に保ち、公開スモーク
チェックを必須とし、squash merge を用いる。資格情報、私的なパス、生の大規模ラン、
モデルの重み、データダンプ、エージェントの状態を決してコミットしてはならない。大きな
学習済み成果物は、レビューを経たうえで対になる Hugging Face リポジトリに置く。

AI による支援は公開ドキュメント上で開示しなければならない。公開の判断と主張については
人間のオーナーが責任を負う。

公開ドキュメントは日本語と英語の両方で提供する。目安として 2 KB / 60 行未満の短い文書は
1 ファイル内に `## 日本語` と `## English` の節を置き、それ以上の長い文書は日本語版を
`<name>.md`（正本）、英語版を `<name>.en.md` として併置する。評価ラベル、証拠クラス、
再現ティア、コマンド、しきい値などの識別子は翻訳せず、英語のまま保持すること。

## English

This repository is the curated public portfolio for WRLM. Keep it runnable,
small, and understandable without access to the private lab. Do not copy the
lab history or bulk-export lab files.

Every experiment must declare its evidence class (`confirmatory`,
`exploratory`, or `diagnostic`), reproduction tier, exact configuration,
commands, compact results, limitations, and source provenance. A successful
primitive diagnostic does not authorize a system-level or mechanism claim.

Use topic branches and pull requests. Keep `main` runnable, require the public
smoke check, and use squash merges. Never commit credentials, private paths,
raw large runs, model weights, data dumps, or agent state. Large learned
artifacts belong in the paired Hugging Face repository after review.

AI assistance must be disclosed in public documentation. The human owner is
responsible for publication decisions and claims.

Public documentation is provided in both Japanese and English. As a rule of
thumb, a short document under about 2 KB or 60 lines carries `## 日本語` and
`## English` sections in one file; a longer document keeps the Japanese text as
the canonical `<name>.md` and places the English text alongside it in
`<name>.en.md`. Do not translate identifiers such as evaluation labels,
evidence classes, reproduction tiers, commands, and thresholds; keep them in
English.
