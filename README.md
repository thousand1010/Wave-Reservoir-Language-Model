**English**: [README.en.md](README.en.md)

# Wave Reservoir Language Model (WRLM)

WRLM は、駆動された非線形波動場が、言語指向の系列モデルにとって有用な状態・記憶・
相互作用の特徴を与えられるかを調べるための研究プロトタイプである。本プロジェクトは
基質検証の段階にあり、本リポジトリは動作する言語モデルを実現したとも、Transformer や
他のリザバーコンピュータに対する優位性があるとも主張しない。

この公開ポートフォリオは、別に存在する非公開の研究ラボから選抜され、レビューを経た
エクスポートを収める。出発点となるのは 1 件の決定論的な診断である。離散非線形
シュレディンガー (DNLS) 場におけるカー非線形性は、注入したモードから予測される
四光波混合 (FWM) モードを生成し、一方で線形コントロール（対照条件）ではそれらの
モードが数値的ゼロにとどまる。

## クイックスタート

CI では Python 3.11 を使用している。

```bash
python -m venv .venv
python -m pip install -r requirements.txt
python examples/wave_field_demo.py
python experiments/gate-nl/reproduce.py --check-reference
python -m unittest discover -s tests -v
```

このサンプルは `smoke-demo` である。再現コマンドは、公開されている Gate NL 診断の全体を
対象とする `full-reproduction` にあたる。訓練データ、学習済みパラメータ、実験用の乱数
シードは一切使用しない。浮動小数点値は文書化された許容誤差で比較され、再現性の第一の
契約は判定しきい値そのものである。

## この結果が支持する範囲

Gate NL は **診断的 (`diagnostic`)** な結果である。これは、この DNLS 実装が公開された
設定のもとで非線形の FWM プリミティブを含む、という限定的な主張のみを支持する。
言語モデルとしての性能、エンドツーエンドでの有用性、他の非線形リザバーに対する波動固有の
優位性を確立するものではない。

[実験のナラティブ](experiments/gate-nl/README.md)、
[理論ノート](docs/theory.md)、[実験インデックス](docs/experiments.md) を参照のこと。

## 成果物 (Artifacts)

大きな成果物や学習済みの成果物は
[Hugging Face](https://huggingface.co/Thousand1010/Wave-Reservoir-Language-Model)
に割り当てる。レビュー済みでリリース可能な重みが無い間、モデルリポジトリは非公開のまま
とする。この GitHub リポジトリにはソース、小さな設定、小さな結果レコードのみを置く。

## 開発体制と開示

公開履歴は非公開ラボの履歴とは独立にキュレーションされている。AI アシスタントは実装、
文書化、レビューに寄与した。研究の方向性、公開範囲、主張は人間のオーナーが選択した。
公開された結果は、実行可能なコードと保存された出力に紐づけられたままである。

## ライセンス

コードは [MIT License](LICENSE) のもとで利用できる。成果物のライセンスは、成果物が
リリースされる時点で Hugging Face 上に別途宣言する。
