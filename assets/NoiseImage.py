#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 12 18:00:59 2025

@author: junga1
"""

import numpy as np
from PIL import Image

# --- configuration ---
INPUT_IMAGE  = "imagedenautoenc.png"
OUTPUT_IMAGE = "imagedenautoenc_noisy.png"
SIGMA = 0.5   # noise level (0.05–0.2 typical)

# --- load image ---
img = Image.open(INPUT_IMAGE).convert("RGB")
x = np.asarray(img, dtype=np.float32) / 255.0

# --- add Gaussian noise ---
noise = SIGMA * np.random.randn(*x.shape)
x_noisy = np.clip(x + noise, 0.0, 1.0)

# --- save noisy image ---
img_noisy = Image.fromarray((255 * x_noisy).astype(np.uint8))
img_noisy.save(OUTPUT_IMAGE)

print(f"Noisy image saved as '{OUTPUT_IMAGE}' (sigma={SIGMA})")