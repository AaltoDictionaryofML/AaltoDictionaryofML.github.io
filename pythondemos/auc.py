"""
auc.py — ROC curve and AUC for a linear classifier on 2D Gaussian data.

Purpose
-------
Illustrate the receiver operating characteristic (ROC) curve and the
area under it (AUC).  A linear classifier is applied to synthetic
two-class Gaussian data, and the ROC curve is computed by sweeping
the decision threshold over the full range of classifier scores.

Relationship to acc.py
----------------------
Uses the same two-cluster setup (same class means, same classifier
direction) but with more data points (200 per class instead of 30)
to produce a smoother ROC curve.

How the ROC curve is computed
-----------------------------
For each threshold tau in a fine grid:
  1. Predict y_hat = 1 if score >= tau, else y_hat = 0.
  2. Compute:
       TPR (true positive rate)  = TP / (TP + FN)  = recall
       FPR (false positive rate) = FP / (FP + TN)
  3. Record the pair (FPR, TPR).

Sweeping tau from +inf to -inf traces the ROC curve from (0,0) to
(1,1).  A high threshold is strict (few positives predicted, low FPR,
low TPR); a low threshold is lenient (many positives predicted, high
FPR, high TPR).

The AUC is the area under this curve, computed via the trapezoidal
rule.  AUC = 1 means perfect separation; AUC = 0.5 means random.

Output
------
  pythondemos/auc_roc.csv — columns: fpr, tpr (~80 subsampled points)
  pythondemos/auc.pdf     — matplotlib preview
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

OUT_DIR = Path(__file__).parent

# Fix random seed for reproducibility
np.random.seed(42)

# ── Generate two Gaussian clusters ────────────────────────────
# Same class means and sigma as acc.py, but 200 points per class
# for a smoother ROC curve.
n_per_class = 200
mu0 = np.array([1.0, 2.0])   # mean of class 0 (negative)
mu1 = np.array([3.0, 1.0])   # mean of class 1 (positive)
sigma = 0.8

X0 = mu0 + sigma * np.random.randn(n_per_class, 2)
X1 = mu1 + sigma * np.random.randn(n_per_class, 2)
X = np.vstack([X0, X1])
y = np.array([0] * n_per_class + [1] * n_per_class)

# ── Linear classifier score ──────────────────────────────────
# Same classifier as acc.py: w points from mu0 toward mu1,
# boundary passes through the midpoint.
w = mu1 - mu0
w = w / np.linalg.norm(w)
midpoint = 0.5 * (mu0 + mu1)
b = -w @ midpoint

# Score for each data point: s(x) = w^T x + b
# Positive scores lean toward class 1, negative toward class 0.
scores = X @ w + b

# ── Compute ROC curve ─────────────────────────────────────────
# Sweep 500 thresholds from below the minimum score to above the
# maximum score.  At each threshold, compute TPR and FPR.
thresholds = np.linspace(scores.min() - 0.1, scores.max() + 0.1, 500)
fpr_list = []
tpr_list = []

for t in thresholds:
    y_pred = (scores >= t).astype(int)

    # Count the four entries of the confusion matrix:
    #   TP = true positive:  predicted 1, actually 1
    #   FP = false positive: predicted 1, actually 0
    #   FN = false negative: predicted 0, actually 1
    #   TN = true negative:  predicted 0, actually 0
    tp = np.sum((y_pred == 1) & (y == 1))
    fp = np.sum((y_pred == 1) & (y == 0))
    fn = np.sum((y_pred == 0) & (y == 1))
    tn = np.sum((y_pred == 0) & (y == 0))

    # TPR = TP / (TP + FN)  — also called recall or sensitivity
    # FPR = FP / (FP + TN)  — also called 1 - specificity
    tpr = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
    fpr_list.append(fpr)
    tpr_list.append(tpr)

fpr_arr = np.array(fpr_list)
tpr_arr = np.array(tpr_list)

# Sort by FPR so the curve is monotone (needed for area computation)
order = np.argsort(fpr_arr)
fpr_arr = fpr_arr[order]
tpr_arr = tpr_arr[order]

# Compute AUC via the trapezoidal rule:
#   AUC ≈ sum of trapezoids under the (FPR, TPR) curve
auc_val = np.trapezoid(tpr_arr, fpr_arr)
print(f"AUC = {auc_val:.4f}")

# ── Verify ────────────────────────────────────────────────────
assert 0.9 < auc_val < 1.0, f"AUC out of expected range: {auc_val}"

# ── Subsample for CSV ─────────────────────────────────────────
# pgfplots does not need 500 points; ~80 evenly spaced points
# produce a visually identical curve and keep the CSV small.
idx = np.linspace(0, len(fpr_arr) - 1, 80, dtype=int)
fpr_sub = fpr_arr[idx]
tpr_sub = tpr_arr[idx]

# Ensure the curve starts at (0,0) and ends at (1,1)
roc_data = np.column_stack([fpr_sub, tpr_sub])
if roc_data[0, 0] != 0.0 or roc_data[0, 1] != 0.0:
    roc_data = np.vstack([[0.0, 0.0], roc_data])
if roc_data[-1, 0] != 1.0 or roc_data[-1, 1] != 1.0:
    roc_data = np.vstack([roc_data, [1.0, 1.0]])

# ── Save CSV ──────────────────────────────────────────────────
# auc_roc.csv: columns fpr, tpr — read by pgfplots in the AUC entry
np.savetxt(OUT_DIR / "auc_roc.csv", roc_data,
           delimiter=",", header="fpr,tpr", comments="",
           fmt="%.6f")
print(f"Saved {OUT_DIR / 'auc_roc.csv'}")

# ── Preview plot ──────────────────────────────────────────────
# Shaded area = AUC; dashed diagonal = random classifier (AUC = 0.5)
fig, ax = plt.subplots(figsize=(4.0, 3.5))

ax.fill_between(fpr_arr, tpr_arr, alpha=0.15, color="tab:blue")
ax.plot(fpr_arr, tpr_arr, "-", color="tab:blue", linewidth=1.5,
        label=f"ROC (AUC = {auc_val:.2f})")
ax.plot([0, 1], [0, 1], "--", color="gray", linewidth=0.8,
        label="random")

ax.set_xlabel("false positive rate")
ax.set_ylabel("true positive rate")
ax.set_xlim(-0.02, 1.02)
ax.set_ylim(-0.02, 1.02)
ax.set_aspect("equal")
ax.legend(fontsize=8, loc="lower right")
ax.tick_params(labelsize=8)

fig.tight_layout()
out = OUT_DIR / "auc.pdf"
fig.savefig(out, bbox_inches="tight")
print(f"Saved {out}")
plt.close()
