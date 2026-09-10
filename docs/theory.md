# Minimal field model / 最小の場のモデル

[日本語](#日本語) | [English](#english)

## 日本語

公開されている診断は、1 次元の駆動・減衰つき離散非線形シュレディンガー場を用いる。

\[
i\dot{\psi}_n = -C(\psi_{n+1}+\psi_{n-1}-2\psi_n)
+ \gamma |\psi_n|^2\psi_n - i\alpha_n\psi_n + V_n\psi_n + d_n(t).
\]

ここで `C` は分散を、`gamma` は局所的なカー非線形性を制御する。`alpha` は減衰、`V` は
静的ポテンシャル、`d(t)` は任意の駆動項である。数値ステップは周期境界と Strang 分割を
用いる。分散はフーリエ空間での厳密な位相回転として適用する。減衰、ポテンシャル、
非線形位相は実空間で適用する。

`gamma = 0` では、フーリエモードは数値的な丸め誤差を除いて独立に発展する。`gamma` が
ゼロでない場合、3 次項は注入されたモード `k_i, k_j, k_l` を、格子サイズを法として
`k_i + k_j - k_l` に混合しうる。Gate NL は、状態スペクトルにおけるこれら予測された
新規モードのエネルギーを測定する。

これはプリミティブ・レベルの試験である。物理的な機構が存在していても、学習、記憶、効率、
言語モデリングにとって有用でないことはありうる。それらの判断には、別途の統制された実験が
必要である。

## English

The public diagnostic uses a one-dimensional driven, damped discrete nonlinear
Schrödinger field:

\[
i\dot{\psi}_n = -C(\psi_{n+1}+\psi_{n-1}-2\psi_n)
+ \gamma |\psi_n|^2\psi_n - i\alpha_n\psi_n + V_n\psi_n + d_n(t).
\]

Here `C` controls dispersion, `gamma` controls the local Kerr nonlinearity,
`alpha` is damping, `V` is a static potential, and `d(t)` is an optional drive.
The numerical step uses periodic boundaries and Strang splitting. Dispersion is
applied as an exact Fourier-space phase rotation. Damping, the potential, and
the nonlinear phase are applied in real space.

For `gamma = 0`, Fourier modes evolve independently apart from numerical
roundoff. For nonzero `gamma`, the cubic term can mix injected modes
`k_i, k_j, k_l` into `k_i + k_j - k_l` modulo the lattice size. Gate NL measures
energy at these predicted new modes in the state spectrum.

This is a primitive-level test. A physical mechanism may exist while remaining
unhelpful for learning, memory, efficiency, or language modeling. Those require
separate controlled experiments.
