#!/usr/bin/env python3
"""
==============================================================
IMAGE SEGMENTATION DEMO — USING KMEANS OR GMM (NO RESIZING)
==============================================================

This demo segments an image into visually coherent regions
based on pixel color and spatial position.

Supported methods:
------------------
- KMeans:     assigns each pixel to one of K clusters
- GMM:        Gaussian Mixture Model with soft (probabilistic) memberships

Outputs:
--------
- segmentation_flexible.png   (hard segmentation)
- soft_blended.png            (soft color mixture, only if GMM)
- soft_cluster{k}.png         (per-cluster membership maps, only if GMM)
- soft_entropy.png            (uncertainty / entropy map, only if GMM)

Dependencies:
-------------
pip install numpy pillow matplotlib scikit-learn
"""

from pathlib import Path
from typing import Optional, Tuple
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# --- scikit-learn imports ---
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler
from matplotlib.colors import rgb_to_hsv, hsv_to_rgb


# ===================== CONFIGURATION =====================
IMAGE_PATH       = "dachstein.png"   # Path to your image file
OUTPUT_FIG       = "segmentation_flexible.png"  # main output filename
N_CLUSTERS       = 10                 # Number of clusters (K)
CLUSTER_METHOD   = "gmm"          # "kmeans" or "gmm"
COLOR_SPACE      = "rgb"             # "rgb" or "hsv" (feature space)
INCLUDE_XY       = True              # Include pixel coordinates as features
XY_SCALE         = 0.25              # Relative weight of XY features
STANDARDIZE      = True              # Apply feature standardization
RANDOM_STATE     = 0                 # Reproducibility seed
# ==========================================================


# ---------------------------------------------------------------------
# 1. IMAGE LOADING AND PREPROCESSING
# ---------------------------------------------------------------------

def load_image(path: str | Path) -> np.ndarray:
    """
    Load an image, convert to RGB, and return a float32 array in [0,1].
    The original resolution is preserved — no resizing or cropping.
    """
    img = Image.open(path).convert("RGB")
    return np.asarray(img, dtype=np.float32) / 255.0


def to_color_space(img_rgb: np.ndarray, color_space: str) -> np.ndarray:
    """
    Convert image to the desired color space.
    Supports only 'rgb' (identity) and 'hsv' (Hue-Saturation-Value).
    """
    cs = color_space.lower()
    if cs == "rgb":
        return img_rgb
    if cs == "hsv":
        return rgb_to_hsv(img_rgb).astype(np.float32)
    raise ValueError("COLOR_SPACE must be 'rgb' or 'hsv'.")


# ---------------------------------------------------------------------
# 2. FEATURE CONSTRUCTION
# ---------------------------------------------------------------------

def build_features(
    img_rgb: np.ndarray,
    color_space: str = "rgb",
    include_xy: bool = True,
    xy_scale: float = 0.25,
    standardize: bool = True,
) -> tuple[np.ndarray, Optional[StandardScaler]]:
    """
    Construct per-pixel feature vectors.

    Each pixel contributes:
        - 3 color components (RGB or HSV)
        - optionally 2 coordinates (y,x) normalized to [0,1] and scaled

    Returns:
        X: (H*W, D) feature matrix (rows = pixels, columns = features)
        scaler: fitted StandardScaler or None
    """
    H, W, _ = img_rgb.shape

    # Convert to desired color representation
    img_cs = to_color_space(img_rgb, color_space)

    # Flatten color channels → shape (N,3)
    color_feat = img_cs.reshape(-1, 3).astype(np.float32)

    # Optionally append spatial coordinates
    feats = [color_feat]
    if include_xy:
        # Create normalized coordinate grid
        y = np.linspace(0, 1, H, dtype=np.float32)
        x = np.linspace(0, 1, W, dtype=np.float32)
        yy, xx = np.meshgrid(y, x, indexing="ij")
        xy = np.stack([yy.ravel(), xx.ravel()], axis=1) * xy_scale
        feats.append(xy.astype(np.float32))

    # Combine color and coordinate features
    X = np.concatenate(feats, axis=1)

    # Optional normalization (zero mean, unit variance per feature)
    scaler = None
    if standardize:
        scaler = StandardScaler()
        X = scaler.fit_transform(X)

    return X, scaler


# ---------------------------------------------------------------------
# 3. CLUSTERING
# ---------------------------------------------------------------------

def run_clustering(X: np.ndarray, method: str, n_clusters: int) -> Tuple[np.ndarray, Optional[np.ndarray]]:
    """
    Run pixel-level clustering using the chosen method.

    Arguments:
        X           : feature matrix (H*W, D)
        method      : "kmeans" or "gmm"
        n_clusters  : number of clusters (K)

    Returns:
        labels  : (N,) hard cluster assignments
        probs   : (N,K) soft probabilities (only for GMM)
    """
    method = method.lower()
    if method == "kmeans":
        # KMeans provides hard assignments only
        km = KMeans(n_clusters=n_clusters, n_init=10, random_state=RANDOM_STATE)
        labels = km.fit_predict(X)
        probs = None

    elif method == "gmm":
        # Gaussian Mixture allows probabilistic (soft) assignments
        gmm = GaussianMixture(n_components=n_clusters, random_state=RANDOM_STATE)
        labels = gmm.fit_predict(X)        # cluster with highest probability
        probs  = gmm.predict_proba(X)      # full soft membership matrix
        print(probs)

    else:
        raise ValueError("CLUSTER_METHOD must be 'kmeans' or 'gmm'.")

    return labels, probs


# ---------------------------------------------------------------------
# 4. VISUALIZATION UTILITIES
# ---------------------------------------------------------------------

def colorize_labels(labels_2d: np.ndarray) -> np.ndarray:
    """
    Assign visually distinct colors to integer cluster labels.

    - Uses evenly spaced hues around the HSV color wheel.
    - Returns an RGB float32 image in [0,1].
    """
    H, W = labels_2d.shape
    flat = labels_2d.ravel()
    uniq = np.unique(flat)
    K = len(uniq)

    if K <= 1:
        return np.ones((H, W, 3), dtype=np.float32)

    # Map arbitrary label IDs → [0..K-1]
    id_map = {lab: i for i, lab in enumerate(uniq)}
    idx = np.vectorize(id_map.get)(flat)

    # Build HSV colors
    hues = np.linspace(0.0, 1.0, K, endpoint=False, dtype=np.float32)
    hsv = np.zeros((flat.size, 3), dtype=np.float32)
    hsv[:, 0] = hues[idx]    # hue depends on cluster id
    hsv[:, 1] = 0.75         # medium saturation
    hsv[:, 2] = 0.95         # bright
    rgb = hsv_to_rgb(hsv).reshape(H, W, 3)
    return rgb


def save_hard_figure(original: np.ndarray, labels_2d: np.ndarray, method_name: str, out_path: str | Path):
    """
    Save a 2-panel figure:
        Left  : original image
        Right : cluster-colored segmentation
    """
    seg_rgb = colorize_labels(labels_2d)
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    axes[0].imshow(original)
    axes[0].set_title("Original Image")
    axes[0].axis("off")
    axes[1].imshow(seg_rgb)
    axes[1].set_title(f"{method_name.upper()} — Hard Segmentation")
    axes[1].axis("off")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


# --------- Soft-clustering visualizations (for GMM only) ---------

def soft_blend(probabilities: np.ndarray) -> np.ndarray:
    """
    Blend cluster colors proportionally to their soft probabilities.
    Produces a smooth, watercolor-like visualization.
    """
    H, W, K = probabilities.shape

    # Define a unique hue for each cluster
    hues = np.linspace(0.0, 1.0, K, endpoint=False, dtype=np.float32)
    hsv = np.zeros((K, 3), dtype=np.float32)
    hsv[:, 0] = hues
    hsv[:, 1] = 0.75
    hsv[:, 2] = 0.95
    cluster_colors = hsv_to_rgb(hsv).astype(np.float32)  # shape (K,3)

    # Blend each pixel’s cluster colors weighted by probabilities
    blended = probabilities @ cluster_colors
    return np.clip(blended, 0.0, 1.0)


def save_soft_visualizations(probs: np.ndarray, H: int, W: int, out_prefix: str = "soft"):
    """
    Save all GMM-specific soft segmentation visualizations:
        1. Blended RGB map (soft_blended.png)
        2. Per-cluster heatmaps (soft_cluster{k}.png)
        3. Entropy (uncertainty) map (soft_entropy.png)
    """
    K = probs.shape[1]
    probs_2d = probs.reshape(H, W, K)

    # --- 1) Blended map ---
    blended = soft_blend(probs_2d)
    plt.imshow(blended)
    plt.title("Soft blended segmentation (GMM)")
    plt.axis("off")
    plt.savefig(f"{out_prefix}_blended.png", dpi=150, bbox_inches="tight")
    plt.close()

    # --- 2) Per-cluster heatmaps ---
    for k in range(K):
        plt.imshow(probs_2d[..., k], vmin=0.0, vmax=1.0, cmap="viridis")
        plt.title(f"Soft membership — cluster {k}")
        plt.axis("off")
        plt.colorbar(fraction=0.046, pad=0.04)
        plt.savefig(f"{out_prefix}_cluster{k}.png", dpi=150, bbox_inches="tight")
        plt.close()

    # --- 3) Entropy map: H(p) = -Σ p_k log(p_k) ---
    eps = 1e-12
    ent = -np.sum(probs_2d * np.log(probs_2d + eps), axis=-1)
    plt.imshow(ent, cmap="magma")
    plt.title("Soft uncertainty (entropy)")
    plt.axis("off")
    plt.colorbar(fraction=0.046, pad=0.04)
    plt.savefig(f"{out_prefix}_entropy.png", dpi=150, bbox_inches="tight")
    plt.close()


# ---------------------------------------------------------------------
# 5. RESULTS SUMMARY
# ---------------------------------------------------------------------

def print_results_info(labels: np.ndarray, method: str, n_clusters: int,
                       probs: Optional[np.ndarray], H: int, W: int):
    """
    Print a concise summary of clustering results:
      - Method, number of clusters, image size
      - Cluster size histogram
      - (if GMM) average confidence and entropy
    """
    N = labels.size
    unique, counts = np.unique(labels, return_counts=True)
    hist = dict(zip(unique.tolist(), counts.tolist()))

    print(f"[OK] Saved: {Path(OUTPUT_FIG).resolve()}")
    if probs is not None:
        print("Also saved: soft_blended.png, soft_cluster{k}.png, soft_entropy.png")

    print(f"[RESULTS] method={method}, K={n_clusters}, image={W}×{H}, pixels={N}")
    print(f"[RESULTS] cluster sizes: {hist}")

    if probs is not None:
        # mean maximum probability and entropy = model certainty indicators
        K = probs.shape[1]
        maxp = probs.max(axis=1).mean()
        eps = 1e-12
        ent = -np.sum(probs * np.log(probs + eps), axis=1).mean()
        print(f"[RESULTS] GMM mean max-prob={maxp:.3f}, mean entropy={ent:.3f} (log(K)={np.log(K):.3f})")
    print()


# ---------------------------------------------------------------------
# 6. MAIN EXECUTION PIPELINE
# ---------------------------------------------------------------------

def main():
    """
    1. Load image (original resolution).
    2. Construct per-pixel feature matrix.
    3. Cluster using KMeans or GMM.
    4. Generate and save visualizations.
    5. Print numerical summary of results.
    """
    path = Path(IMAGE_PATH)
    if not path.is_file():
        print(f"[ERROR] Image not found: {path.resolve()}")
        return

    # --- Step 1: Load image ---
    img = load_image(path)
    H, W, _ = img.shape

    # --- Step 2: Build features ---
    X, _ = build_features(
        img,
        color_space=COLOR_SPACE,
        include_xy=INCLUDE_XY,
        xy_scale=XY_SCALE,
        standardize=STANDARDIZE,
    )

    # --- Step 3: Cluster ---
    labels, probs = run_clustering(X, CLUSTER_METHOD, N_CLUSTERS)
    labels_2d = labels.reshape(H, W)

    # --- Step 4: Visualizations ---
    save_hard_figure(img, labels_2d, CLUSTER_METHOD, OUTPUT_FIG)
    if probs is not None:
        save_soft_visualizations(probs, H, W, out_prefix="soft")

    # --- Step 5: Print summary ---
    print_results_info(labels, CLUSTER_METHOD, N_CLUSTERS, probs, H, W)


# ---------------------------------------------------------------------
# Run the script
# ---------------------------------------------------------------------

if __name__ == "__main__":
    main()
