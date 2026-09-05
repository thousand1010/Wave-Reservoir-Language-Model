# Minimal field model

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
