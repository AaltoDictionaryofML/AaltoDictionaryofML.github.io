#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Offline MP4 generator with audio for opera spectrogram (YouTube Shorts format)

Input (from live capture script):
    - opera_multitaper_spectrogram.npz
        * spec_cols : (N_FREQ_BINS, n_frames) power (dB) per block
        * freqs     : (N_FREQ_BINS,) frequency axis
        * sample_rate
        * block_size
    - opera_multitaper_audio.wav

Output:
    - opera_multitaper_with_audio.mp4  (vertical video + audio, durations matched)

Requires:
    - ffmpeg on PATH
    - numpy, matplotlib, scipy
"""

import os
import subprocess

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter
from scipy.io import wavfile

# ---------- FILE NAMES ----------
SPEC_FILE        = "opera_multitaper_spectrogram.npz"
AUDIO_FILE       = "opera_multitaper_audio.wav"
VIDEO_NO_AUDIO   = "opera_multitaper_video_no_audio.mp4"
VIDEO_WITH_AUDIO = "opera_multitaper_with_audio.mp4"

# ---------- DISPLAY / TIMING SETTINGS ----------
# Must match what you used in the live script (e.g. HISTORY_SEC = 5.0)
HISTORY_SEC = 5.0

# Colormap and dB limits (should match live view)
DB_MIN = -120.0
DB_MAX = 0.0

# ---------- LOAD DATA ----------
print(f"Loading spectrogram from {SPEC_FILE} ...")
data = np.load(SPEC_FILE)
spec_cols   = data["spec_cols"]       # shape (N_FREQ_BINS, n_frames)
freqs       = data["freqs"]
sample_rate = int(data["sample_rate"])
block_size  = int(data["block_size"])

N_FREQ_BINS, n_frames = spec_cols.shape
blocks_per_sec = sample_rate / block_size
seconds_per_block = block_size / sample_rate

# Video FPS chosen so that video duration matches audio duration
FPS = blocks_per_sec  # n_frames / FPS == n_frames * block_size / sample_rate

print(f"N_FREQ_BINS = {N_FREQ_BINS}, n_frames = {n_frames}")
print(f"sample_rate = {sample_rate}, block_size = {block_size}")
print(f"blocks_per_sec = {blocks_per_sec:.2f}, FPS = {FPS:.2f}")

# History window in frames
N_TIME_BINS = int(HISTORY_SEC * blocks_per_sec)
if N_TIME_BINS < 1:
    raise ValueError("HISTORY_SEC too small given block size / sample rate.")

print(f"History length: {HISTORY_SEC:.2f} s ({N_TIME_BINS} frames)")

# ---------- LOAD AUDIO ----------
print(f"Loading audio from {AUDIO_FILE} ...")
audio_sr, audio = wavfile.read(AUDIO_FILE)
if audio_sr != sample_rate:
    raise ValueError(
        f"Audio sample rate {audio_sr} != spectrogram sample rate {sample_rate}"
    )

audio_duration = audio.shape[0] / audio_sr
video_duration = n_frames * seconds_per_block
print(f"Audio duration ≈ {audio_duration:.2f} s, "
      f"video (by design) ≈ {video_duration:.2f} s")

# ---------- SET UP FIGURE (VERTICAL FOR YOUTUBE SHORTS) ----------
plt.close("all")
# Make the figure portrait-oriented for a natural 9:16 feel
fig, ax = plt.subplots(figsize=(4, 7))  # was (8, 4) -> now tall instead of wide

# --- Custom time axis: right = "now", left = negative seconds ---
# We want ticks at integer seconds: 0, 1, 2, ..., HISTORY_SEC
# But displayed from left to right as: -HISTORY_SEC ... -1 ... now

n_ticks = int(HISTORY_SEC) + 1
tick_positions = np.linspace(0, HISTORY_SEC, n_ticks)

tick_labels = []
for t in reversed(range(n_ticks)):  # reverse so rightmost is first element
    if t == 0:
        tick_labels.append("now")
    else:
        tick_labels.append(f"-{t}s")

# Assign ticks
ax.set_xticks(tick_positions)
ax.set_xticklabels(tick_labels)


# Display buffer: like in live view, sliding window of last N_TIME_BINS columns
spec_display = np.full((N_FREQ_BINS, N_TIME_BINS), DB_MIN, dtype=np.float32)

extent = [0, HISTORY_SEC, 0, float(freqs[-1])]
img = ax.imshow(
    spec_display,
    origin="lower",
    aspect="auto",
    extent=extent,
    vmin=DB_MIN,
    vmax=DB_MAX,
    cmap="magma",
)

ax.set_xlabel("Time [s]")
ax.set_ylabel("Frequency [Hz]")
ax.set_title("Spectrogram")

cbar = fig.colorbar(img, ax=ax, label="Magnitude [dB]")
plt.tight_layout()

# ---------- CREATE VIDEO (NO AUDIO YET) ----------
print(f"Creating video-only file: {VIDEO_NO_AUDIO}")

writer = FFMpegWriter(
    fps=FPS,
    metadata={"title": "Spectrogram", "artist": "n/a"},
)

with writer.saving(fig, VIDEO_NO_AUDIO, dpi=150):
    for frame_idx in range(n_frames):
        # New column (full-band, already in dB)
        col = spec_cols[:, frame_idx]
        col = np.clip(col, DB_MIN, DB_MAX)

        # Slide left, append new column on the right
        spec_display[:, :-1] = spec_display[:, 1:]
        spec_display[:, -1] = col

        img.set_data(spec_display)
        # Time axis is always 0..HISTORY_SEC for the sliding window
        img.set_extent(extent)

        writer.grab_frame()

plt.close(fig)
print("Video-only rendering complete.")

# ---------- MUX AUDIO + VIDEO WITH FFMPEG (SCALE TO 9:16) ----------
print(f"Muxing audio into {VIDEO_WITH_AUDIO} with ffmpeg (9:16 scaling)...")

# Scale and pad to 1080x1920 (9:16) for YouTube Shorts
ffmpeg_cmd = [
    "ffmpeg",
    "-y",                # overwrite output
    "-i", VIDEO_NO_AUDIO,
    "-i", AUDIO_FILE,
    # scale to fit into 1080x1920 while preserving aspect, then pad
    "-filter:v",
    "scale=1080:1920:force_original_aspect_ratio=decrease,"
    "pad=1080:1920:(ow-iw)/2:(oh-ih)/2",
    "-c:v", "libx264",
    "-preset", "medium",
    "-crf", "18",
    "-c:a", "aac",
    "-b:a", "192k",
    "-pix_fmt", "yuv420p",   # good compatibility for web/YouTube
    "-shortest",             # cut off extra audio or video if mismatch
    VIDEO_WITH_AUDIO,
]

try:
    subprocess.run(ffmpeg_cmd, check=True)
    print(f"Created {VIDEO_WITH_AUDIO}")
except FileNotFoundError:
    print("Error: ffmpeg not found. Please install ffmpeg and ensure it is on PATH.")
except subprocess.CalledProcessError as e:
    print("ffmpeg failed:", e)

print("Done.")
