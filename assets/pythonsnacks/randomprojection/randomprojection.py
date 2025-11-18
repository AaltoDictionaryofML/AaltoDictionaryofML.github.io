#!/usr/bin/env python3
"""
Generate PNGs for the TeX figure:
  randomprojection_original.png
  randomprojection_masked.png
(and additionally: randomprojection_reconstructed.png)

Installs:
    pip install numpy pillow matplotlib
"""

from pathlib import Path
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt  # <-- NEW

# ---------------- CONFIG ---------------- #
INPUT_FILE    = Path("dachstein.png")   # your image
KEEP_PERCENT  = 5.0                     # % of pixels to KEEP
SEED          = 0                       # RNG seed

# Reconstruction params (simple convolutional inpainting)
N_ITERS       = 100                     # iterations
KERNEL_SIZE   = 5                       # 3 or 5

OUT_ORIG      =  "randomprojection_original.png"
OUT_MASKED    = "randomprojection_masked.png"
OUT_RECON     = "randomprojection_reconstructed.png"  # optional
# ---------------------------------------- #

# ---- small helpers ----
INIT_BG_DARK  = np.array([0.1, 0.1, 0.1], dtype=np.float32)
INIT_BG_LIGHT = np.array([0.9, 0.9, 0.9], dtype=np.float32)

def to_uint8(img01: np.ndarray) -> np.ndarray:
    return (np.clip(img01, 0.0, 1.0) * 255.0 + 0.5).astype(np.uint8)

def auto_contrasting_color(img: np.ndarray) -> np.ndarray:
    """Light bg if image is dark; dark bg if image is bright."""
    avg = img.mean(axis=(0, 1))
    lum = 0.299*avg[0] + 0.587*avg[1] + 0.114*avg[2]
    return INIT_BG_LIGHT if lum < 0.5 else INIT_BG_DARK

def gaussian_like_kernel(size: int = 5) -> np.ndarray:
    if size == 3:
        v = np.array([1, 2, 1], dtype=np.float32)
    elif size == 5:
        v = np.array([1, 4, 6, 4, 1], dtype=np.float32)
    else:
        raise ValueError("KERNEL_SIZE must be 3 or 5")
    k = np.outer(v, v).astype(np.float32)
    k /= k.sum()
    return k

def conv2d_single(img2d: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    kh, kw = kernel.shape
    ph, pw = kh // 2, kw // 2
    padded = np.pad(img2d, ((ph, ph), (pw, pw)), mode="reflect")
    out = np.zeros_like(img2d, dtype=np.float32)
    for i in range(kh):
        for j in range(kw):
            out += kernel[i, j] * padded[i:i+img2d.shape[0], j:j+img2d.shape[1]]
    return out

def conv2d_rgb(img: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    out = np.empty_like(img, dtype=np.float32)
    for c in range(3):
        out[..., c] = conv2d_single(img[..., c], kernel)
    return out

def apply_random_mask(h: int, w: int, keep_percent: float, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    keep2d = rng.random((h, w)) < (keep_percent / 100.0)
    return np.repeat(keep2d[..., None], 3, axis=2)  # (H,W,3) boolean

def reconstruct_by_convolution(img: np.ndarray, mask3: np.ndarray,
                               n_iters: int, ksize: int) -> np.ndarray:
    bg = auto_contrasting_color(img)
    x = np.where(mask3, img, bg)
    k = gaussian_like_kernel(ksize)
    for _ in range(n_iters):
        blurred = conv2d_rgb(x, k)
        x = np.where(mask3, img, blurred)  # enforce known pixels
    return x

def main():
    if not INPUT_FILE.is_file():
        raise FileNotFoundError(f"Image not found: {INPUT_FILE}")

    # Load RGB in [0,1]
    img = np.asarray(Image.open(INPUT_FILE).convert("RGB"), np.float32) / 255.0
    H, W, _ = img.shape

    # Build mask and masked visualization
    mask3 = apply_random_mask(H, W, KEEP_PERCENT, SEED)
    bg = auto_contrasting_color(img)
    masked_vis = np.where(mask3, img, bg)

    # Reconstruct (optional third file)
    recon = reconstruct_by_convolution(img, mask3, N_ITERS, KERNEL_SIZE)
    
    diff = recon - img

    num = np.linalg.norm(diff)
    den = np.linalg.norm(img)

    rel_error = num / den
    print("Relative error:", rel_error)

    # Save exactly what the TeX figure expects
    Image.fromarray(to_uint8(img)).save(OUT_ORIG)
    Image.fromarray(to_uint8(masked_vis)).save(OUT_MASKED)
    Image.fromarray(to_uint8(recon)).save(OUT_RECON)

    print(f"Saved:\n - {OUT_ORIG}\n - {OUT_MASKED}\n - {OUT_RECON} (optional)")

    # --------- ALSO SHOW IMAGES IN SPYDER --------- #
    # This will appear in the Plots pane if Spyder is set to "Automatic" or "Inline" graphics
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    axs = np.atleast_1d(axes)

    axs[0].imshow(img)
    axs[0].set_title("Original")
    axs[0].axis("off")

    axs[1].imshow(masked_vis)
    axs[1].set_title(f"Masked ({KEEP_PERCENT:.1f}%)")
    axs[1].axis("off")

    axs[2].imshow(recon)
    axs[2].set_title("Reconstructed")
    axs[2].axis("off")

    plt.tight_layout()
    plt.show()
    # ----------------------------------------------- #

if __name__ == "__main__":
    main()
