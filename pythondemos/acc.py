"""
acc.py — Accuracy of a linear classifier on a 2D binary dataset.

Purpose
-------
Illustrate the concept of accuracy: the fraction of data points
whose predicted label matches the true label.  A simple linear
classifier is applied to synthetic 2D Gaussian data, and each
data point is marked as correctly or incorrectly classified.

Data generation
---------------
Two classes (y=0 and y=1) are generated from isotropic Gaussian
distributions with different means:
    class 0: x ~ N(mu0, sigma^2 I),  mu0 = (1, 2)
    class 1: x ~ N(mu1, sigma^2 I),  mu1 = (3, 1)
    sigma = 0.8, 30 points per class

Classifier
----------
A linear decision boundary is constructed using the direction
between the two class means (Fisher's discriminant direction):
    w = (mu1 - mu0) / ||mu1 - mu0||
    b = -w^T * midpoint,  where midpoint = (mu0 + mu1) / 2
A data point x is classified as y=1 if w^T x + b > 0, else y=0.

This is not a trained classifier — it uses the known class means
directly.  The purpose is to produce a clean, reproducible example
with a few misclassified points near the decision boundary.

Output
------
  pythondemos/acc_data.csv     — columns: x1, x2, label, predicted, correct
  pythondemos/acc_boundary.csv — columns: x1, x2 (two endpoints of boundary)
  pythondemos/acc.pdf          — matplotlib preview
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

OUT_DIR = Path(__file__).parent

# Fix random seed for reproducibility (re-running produces identical CSVs)
np.random.seed(42)

# ── Generate two Gaussian clusters ────────────────────────────
# 30 points per class, 60 total.  The means are chosen so that
# the clusters overlap slightly, producing a few misclassifications.
n_per_class = 30
mu0 = np.array([1.0, 2.0])   # mean of class 0
mu1 = np.array([3.0, 1.0])   # mean of class 1
sigma = 0.8                   # standard deviation (same for both classes)

X0 = mu0 + sigma * np.random.randn(n_per_class, 2)  # class 0 samples
X1 = mu1 + sigma * np.random.randn(n_per_class, 2)  # class 1 samples
X = np.vstack([X0, X1])                              # (60, 2) feature matrix
y = np.array([0] * n_per_class + [1] * n_per_class)  # true labels

# ── Linear classifier: h(x) = sign(w^T x + b) ───────────────
# The weight vector w points from mu0 toward mu1 (the direction
# that best separates the two class means).  The bias b is chosen
# so that the decision boundary passes through the midpoint of
# the two means, which is the Bayes-optimal boundary when both
# classes have equal covariance and equal prior probability.
w = mu1 - mu0                   # direction between class means
w = w / np.linalg.norm(w)       # normalize to unit length
midpoint = 0.5 * (mu0 + mu1)   # midpoint between the means
b = -w @ midpoint               # bias: boundary passes through midpoint

# Compute the classifier score for each data point.
# Positive score → predict class 1; negative score → predict class 0.
scores = X @ w + b
y_pred = (scores > 0).astype(int)

# Determine which predictions are correct (1) or incorrect (0)
correct = (y_pred == y).astype(int)
accuracy = correct.mean()

print(f"Accuracy: {accuracy:.2f} ({correct.sum()}/{len(y)})")

# ── Verify ────────────────────────────────────────────────────
assert 0.8 < accuracy < 1.0, f"Accuracy out of expected range: {accuracy}"
assert len(y) == 2 * n_per_class, f"Unexpected sample size: {len(y)}"

# ── Save CSV ──────────────────────────────────────────────────
# acc_data.csv: one row per data point, columns:
#   x1, x2    — feature values
#   label     — true class (0 or 1)
#   predicted — predicted class (0 or 1)
#   correct   — 1 if prediction matches label, 0 otherwise
data = np.column_stack([X, y, y_pred, correct])
header = "x1,x2,label,predicted,correct"
np.savetxt(OUT_DIR / "acc_data.csv", data,
           delimiter=",", header=header, comments="",
           fmt=["%.6f", "%.6f", "%d", "%d", "%d"])

# acc_boundary.csv: two endpoints of the decision boundary line.
# The boundary is the set {x : w^T x + b = 0}, which is a line
# in 2D.  Solving for x2: x2 = -(w1*x1 + b) / w2.
x1_range = np.array([X[:, 0].min() - 0.5, X[:, 0].max() + 0.5])
x2_boundary = -(w[0] * x1_range + b) / w[1]
np.savetxt(OUT_DIR / "acc_boundary.csv",
           np.column_stack([x1_range, x2_boundary]),
           delimiter=",", header="x1,x2", comments="")

print(f"Saved {OUT_DIR / 'acc_data.csv'}")
print(f"Saved {OUT_DIR / 'acc_boundary.csv'}")

# ── Nonlinear (overfit) classifier ────────────────────────────
# RBF-weighted score:
#   f(x) = sum_{class 1} exp(-||x-x_i||^2 / (2 sigma_rbf^2))
#        - sum_{class 0} exp(-||x-x_i||^2 / (2 sigma_rbf^2))
# A small bandwidth sigma_rbf makes the classifier approach
# 1-NN, which achieves perfect training accuracy but wiggles
# sharply near misclassified points.  This illustrates how
# optimizing accuracy alone can yield a highly non-smooth
# decision boundary that is sensitive to feature perturbations.
sigma_rbf = 0.10

def rbf_score(points, centers, s):
    d2 = ((points[:, None, :] - centers[None, :, :]) ** 2).sum(-1)
    return np.exp(-d2 / (2.0 * s ** 2)).sum(axis=1)

# Grid for extracting the 0-level contour.
x1_min, x1_max = X[:, 0].min() - 0.6, X[:, 0].max() + 0.6
x2_min, x2_max = X[:, 1].min() - 0.6, X[:, 1].max() + 0.6
xx, yy = np.meshgrid(
    np.linspace(x1_min, x1_max, 500),
    np.linspace(x2_min, x2_max, 500),
)
grid = np.stack([xx.ravel(), yy.ravel()], axis=1)
Z = rbf_score(grid, X1, sigma_rbf) - rbf_score(grid, X0, sigma_rbf)
Z = Z.reshape(xx.shape)

# Verify perfect training accuracy of the RBF classifier.
train_scores = rbf_score(X, X1, sigma_rbf) - rbf_score(X, X0, sigma_rbf)
rbf_pred = (train_scores > 0).astype(int)
rbf_acc = (rbf_pred == y).mean()
assert rbf_acc == 1.0, f"RBF classifier not at perfect accuracy: {rbf_acc}"

# Extract the 0-level contour (may consist of several pieces).
fig_tmp, ax_tmp = plt.subplots()
cs = ax_tmp.contour(xx, yy, Z, levels=[0])
segs = cs.allsegs[0]
plt.close(fig_tmp)

# Write a single CSV with segments separated by "nan,nan" rows.
# pgfplots with [unbounded coords=jump] starts a new path at each
# NaN coordinate, so the resulting plot has disjoint pieces.
with open(OUT_DIR / "acc_overfit_boundary.csv", "w") as f:
    f.write("x1,x2\n")
    for i, seg in enumerate(segs):
        if i > 0:
            f.write("nan,nan\n")
        for px, py in seg:
            f.write(f"{px:.6f},{py:.6f}\n")
print(f"Saved {OUT_DIR / 'acc_overfit_boundary.csv'}"
      f"  ({len(segs)} contour segment(s))")

# ── Preview plot ──────────────────────────────────────────────
# Blue circles: class 0, correctly classified
# Red squares:  class 1, correctly classified
# Black open circles: misclassified (either class)
# Dashed line: decision boundary
fig, ax = plt.subplots(figsize=(4.5, 3.5))

mask_c = correct == 1  # correctly classified mask
ax.scatter(X[mask_c & (y == 0), 0], X[mask_c & (y == 0), 1],
           c="tab:blue", marker="o", edgecolors="k", linewidths=0.3,
           s=30, label=r"$y=0$, correct", zorder=3)
ax.scatter(X[mask_c & (y == 1), 0], X[mask_c & (y == 1), 1],
           c="tab:red", marker="s", edgecolors="k", linewidths=0.3,
           s=30, label=r"$y=1$, correct", zorder=3)

mask_w = correct == 0  # incorrectly classified mask
ax.scatter(X[mask_w, 0], X[mask_w, 1],
           c="none", marker="o", edgecolors="black", linewidths=1.5,
           s=80, label="incorrect", zorder=4)

ax.plot(x1_range, x2_boundary, "k--", linewidth=1.0, label="linear $h$")
for i, seg in enumerate(segs):
    ax.plot(seg[:, 0], seg[:, 1], color="tab:green", linewidth=1.2,
            label="overfit $h'$" if i == 0 else None)

ax.set_xlabel(r"$x_1$")
ax.set_ylabel(r"$x_2$")
ax.set_title(f"accuracy = {accuracy:.2f}")
ax.legend(fontsize=7, loc="upper left")
ax.tick_params(labelsize=8)

fig.tight_layout()
out = OUT_DIR / "acc.pdf"
fig.savefig(out, bbox_inches="tight")
print(f"Saved {out}")
plt.close()
