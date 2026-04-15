"""
adam.py — Compare gradient descent (GD) vs Adam on a quadratic objective.

Purpose
-------
Illustrate why Adam converges faster than plain GD on ill-conditioned
problems.  The objective is a simple quadratic with controllable
condition number kappa:

    f(w) = w1^2 + kappa * w2^2

The Hessian is diag(2, 2*kappa), so the condition number of the
Hessian equals kappa.  GD with a fixed learning rate eta must satisfy
eta < 1/kappa to avoid divergence (the largest eigenvalue of the
Hessian is 2*kappa, and GD converges iff eta < 2/(2*kappa) = 1/kappa).
This forces GD to take tiny steps along the w1 direction, where the
curvature is low.

Adam, by contrast, maintains per-coordinate running averages of the
first moment (mean) and second moment (uncentered variance) of the
gradient.  Dividing by the square root of the second moment rescales
each coordinate independently, effectively adapting the learning rate
to the local curvature.  This allows Adam to make progress along both
coordinates at a similar rate.

Parameters chosen
-----------------
- kappa = 50      : makes the landscape 50x steeper in w2 than w1
- w0 = (1, 1)     : starting point (both coordinates equal)
- GD lr = 9e-3    : just below 1/kappa = 0.02 (conservative)
- Adam lr = 0.02  : moderate; Adam's adaptive scaling handles the rest
- 120 iterations  : enough for Adam to converge, GD still far from zero

Output
------
  pythondemos/adam_gd.csv    — GD trajectory (iter, w1, w2, fval)
  pythondemos/adam_adam.csv  — Adam trajectory (iter, w1, w2, fval)
  pythondemos/adam.pdf       — matplotlib preview (two panels)
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

OUT_DIR = Path(__file__).parent

# ── Parameters ────────────────────────────────────────────────
kappa = 50.0           # condition number of the Hessian
w0 = np.array([1.0, 1.0])  # starting point
n_iter = 120           # number of optimization steps

# GD learning rate: must satisfy eta < 1/kappa = 0.02 to converge.
# Choosing eta = 9e-3 leaves some margin but is slow along w1.
gd_lr = 9.0e-3

# Adam hyperparameters (Kingma & Ba, 2015, default recommendations):
#   beta1 = 0.9   — exponential decay rate for the first moment
#   beta2 = 0.999 — exponential decay rate for the second moment
#   eps   = 1e-8  — small constant to prevent division by zero
adam_lr = 0.02
beta1, beta2, eps = 0.9, 0.999, 1e-8


# ── Objective and gradient ────────────────────────────────────
# f(w) = w1^2 + kappa * w2^2
# grad f(w) = (2*w1, 2*kappa*w2)
def f(w):
    """Evaluate the quadratic objective at w = (w1, w2)."""
    return w[0]**2 + kappa * w[1]**2


def grad_f(w):
    """Evaluate the gradient of f at w = (w1, w2)."""
    return np.array([2.0 * w[0], 2.0 * kappa * w[1]])


# ── Gradient descent ──────────────────────────────────────────
# Standard GD update: w <- w - eta * grad_f(w)
# The same learning rate eta is used for both coordinates.
def run_gd(w0, lr, steps):
    """Run gradient descent and return the full trajectory."""
    path = [w0.copy()]
    w = w0.copy()
    for _ in range(steps):
        w = w - lr * grad_f(w)
        path.append(w.copy())
    return np.array(path)


# ── Adam ──────────────────────────────────────────────────────
# Adam update (Kingma & Ba, 2015):
#   m_t = beta1 * m_{t-1} + (1 - beta1) * g_t        (first moment)
#   v_t = beta2 * v_{t-1} + (1 - beta2) * g_t ⊙ g_t  (second moment)
#   m_hat = m_t / (1 - beta1^t)                       (bias correction)
#   v_hat = v_t / (1 - beta2^t)                       (bias correction)
#   w <- w - lr * m_hat ⊘ (sqrt(v_hat) + eps)         (parameter update)
#
# The element-wise division by sqrt(v_hat) rescales each coordinate
# by its running RMS gradient magnitude.  Coordinates with large
# gradients (like w2 here) get their effective step size reduced;
# coordinates with small gradients (like w1 late in training) get
# their effective step size increased.
def run_adam(w0, lr, steps):
    """Run Adam optimizer and return the full trajectory."""
    path = [w0.copy()]
    w = w0.copy()
    m = np.zeros_like(w)  # first moment estimate (initialized to zero)
    v = np.zeros_like(w)  # second moment estimate (initialized to zero)
    for t in range(1, steps + 1):
        g = grad_f(w)
        # Update biased first and second moment estimates
        m = beta1 * m + (1 - beta1) * g
        v = beta2 * v + (1 - beta2) * (g * g)  # Hadamard product g ⊙ g
        # Bias-correct (compensates for zero initialization of m, v)
        m_hat = m / (1 - beta1**t)
        v_hat = v / (1 - beta2**t)
        # Parameter update with per-coordinate adaptive learning rate
        w = w - lr * m_hat / (np.sqrt(v_hat) + eps)
        path.append(w.copy())
    return np.array(path)


# ── Run both optimizers ───────────────────────────────────────
path_gd = run_gd(w0, gd_lr, n_iter)
path_adam = run_adam(w0, adam_lr, n_iter)

# Compute objective value at each iterate
fvals_gd = np.array([f(w) for w in path_gd])
fvals_adam = np.array([f(w) for w in path_adam])
iters_gd = np.arange(len(path_gd))
iters_adam = np.arange(len(path_adam))

# ── Verify ────────────────────────────────────────────────────
# GD should not diverge (fval should decrease monotonically for
# a quadratic with eta < 1/kappa)
assert fvals_gd[-1] < fvals_gd[0], "GD diverged — check learning rate"
# Adam should reach a lower objective than GD
assert fvals_adam[-1] < fvals_gd[-1], "Adam did not beat GD"
print(f"GD  final objective: {fvals_gd[-1]:.6e}")
print(f"Adam final objective: {fvals_adam[-1]:.6e}")

# ── Save CSVs for pgfplots ────────────────────────────────────
# Each CSV has columns: iter, w1, w2, fval
# The LaTeX figure reads these with \addplot table[col sep=comma].
for name, path, fvals, iters in [
    ("adam_gd", path_gd, fvals_gd, iters_gd),
    ("adam_adam", path_adam, fvals_adam, iters_adam),
]:
    data = np.column_stack([iters, path, fvals])
    np.savetxt(OUT_DIR / f"{name}.csv", data,
               delimiter=",", header="iter,w1,w2,fval", comments="")
    print(f"Saved {OUT_DIR / name}.csv")

# ── Preview plot (two panels) ─────────────────────────────────
# Left panel:  parameter-space trajectories (w1 vs w2)
# Right panel: objective value vs iteration (log scale)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3.2))

# Left: parameter-space trajectory
ax1.plot(path_gd[:, 0], path_gd[:, 1], "o-", color="tab:blue",
         markersize=2, linewidth=0.8, label="GD", markevery=3)
ax1.plot(path_adam[:, 0], path_adam[:, 1], "s-", color="tab:red",
         markersize=2, linewidth=0.8, label="Adam", markevery=3)
ax1.plot(*w0, "k^", markersize=7, zorder=4)
ax1.annotate(r"$\mathbf{w}^{(0)}$", w0, textcoords="offset points",
             xytext=(5, 5), fontsize=9)
ax1.plot(0, 0, "k*", markersize=9, zorder=4)
ax1.annotate(r"$\mathbf{w}^{\star}$", (0, 0), textcoords="offset points",
             xytext=(5, -10), fontsize=9)
ax1.set_xlabel(r"$w_1$")
ax1.set_ylabel(r"$w_2$")
ax1.legend(fontsize=7)
ax1.set_title("parameter space", fontsize=9)
ax1.tick_params(labelsize=8)

# Right: objective vs iterations (log scale)
# On a log scale, linear convergence appears as a straight line.
# GD converges linearly with rate (1 - 2*eta); Adam is faster.
ax2.semilogy(iters_gd, fvals_gd, "o-", color="tab:blue",
             markersize=2, linewidth=0.8, label="GD", markevery=3)
ax2.semilogy(iters_adam, fvals_adam, "s-", color="tab:red",
             markersize=2, linewidth=0.8, label="Adam", markevery=3)
ax2.set_xlabel("iteration $t$")
ax2.set_ylabel(r"$f(\mathbf{w}^{(t)})$")
ax2.legend(fontsize=7)
ax2.set_title("objective value", fontsize=9)
ax2.tick_params(labelsize=8)

fig.tight_layout()
out = OUT_DIR / "adam.pdf"
fig.savefig(out, bbox_inches="tight")
print(f"Saved {out}")
plt.close()
