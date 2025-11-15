#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Live Multitaper Spectrogram for Opera — Real-Time, No Video Encoding

- Shows live multitaper spectrogram (0–8 kHz).
- Zooms vocal band (200–1500 Hz) + crude f0 trace.
- Records:
    * opera_multitaper_audio.wav        (mono mic audio)
    * opera_multitaper_spectrogram.npz  (all spectrogram columns)

You can convert the saved spectrogram to MP4/AVI offline later.
"""

import queue
import sys
import os

import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.signal.windows import dpss
from scipy.io import wavfile

# ---------- CONFIG ----------
SAMPLE_RATE     = 44_100
BLOCK_SIZE      = 4_096        # ~10.8 blocks/sec
N_FFT           = 4_096        # same as BLOCK_SIZE (no overlap for simplicity)
HISTORY_SEC     = 5.0
MAX_DISPLAY_HZ  = 8_000

VOICE_MIN_HZ    = 200.0
VOICE_MAX_HZ    = 1_500.0

# Multitaper
K_TAPERS = 3
NW       = 2.0

# Output files
AUDIO_FILE = "opera_multitaper_audio.wav"
SPEC_FILE  = "opera_multitaper_spectrogram.npz"

# ---------- DERIVED SIZES ----------
N_TIME_BINS = int(HISTORY_SEC * SAMPLE_RATE / BLOCK_SIZE)

freqs   = np.fft.rfftfreq(N_FFT, d=1.0 / SAMPLE_RATE)
max_bin = np.searchsorted(freqs, MAX_DISPLAY_HZ)
N_FREQ_BINS = max_bin

voice_min_bin = np.searchsorted(freqs, VOICE_MIN_HZ)
voice_max_bin = np.searchsorted(freqs, VOICE_MAX_HZ)
voice_max_bin = min(voice_max_bin, N_FREQ_BINS)
N_VOICE_BINS  = voice_max_bin - voice_min_bin

audio_queue  = queue.Queue()
audio_blocks = []       # raw audio blocks
spec_cols    = []       # store each full-band spectrogram column for offline use

fft_buffer = np.zeros(N_FFT, dtype=np.float32)

# Base window + DPSS tapers
base_window   = np.hanning(N_FFT).astype(np.float32)
tapers        = dpss(N_FFT, NW, K_TAPERS).astype(np.float32)
multi_windows = tapers * base_window[None, :]

# Time axis & f0 history for display (only last HISTORY_SEC)
t_axis = np.linspace(0, HISTORY_SEC, N_TIME_BINS)
f0_hist = np.full(N_TIME_BINS, np.nan, dtype=np.float32)


def audio_callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    audio_queue.put(indata[:, 0].copy())


# ---------- PLOTTING SETUP ----------
plt.close("all")
fig, (ax_full, ax_zoom) = plt.subplots(
    2, 1, figsize=(9, 6), sharex=True, gridspec_kw={"height_ratios": [2, 1]}
)

spec_full = np.full((N_FREQ_BINS, N_TIME_BINS), -120.0, dtype=np.float32)

extent_full = [0, HISTORY_SEC, 0, MAX_DISPLAY_HZ]
img_full = ax_full.imshow(
    spec_full,
    origin="lower",
    aspect="auto",
    extent=extent_full,
    vmin=-120,
    vmax=0,
    cmap="magma",
)
ax_full.set_ylabel("Freq [Hz]")
ax_full.set_title("Live Opera Spectrogram (Multitaper, Live Only)")

extent_zoom = [0, HISTORY_SEC, VOICE_MIN_HZ, VOICE_MAX_HZ]
img_zoom = ax_zoom.imshow(
    spec_full[voice_min_bin:voice_max_bin, :],
    origin="lower",
    aspect="auto",
    extent=extent_zoom,
    vmin=-120,
    vmax=0,
    cmap="magma",
)
ax_zoom.set_xlabel("Time [s]")
ax_zoom.set_ylabel("Freq [Hz]")
ax_zoom.set_title(f"Vocal Band Zoom ({int(VOICE_MIN_HZ)}–{int(VOICE_MAX_HZ)} Hz)")

(line_f0,) = ax_zoom.plot(t_axis, f0_hist, linewidth=1.2)

fig.colorbar(img_full, ax=[ax_full, ax_zoom], label="Magnitude [dB]")
plt.tight_layout()
plt.show(block=False)

# Select mic device
sd.default.device = (0, None)  # MacBook Air mic as input (adjust if needed)

# ---------- MAIN LOOP (NO VIDEO ENCODING) ----------
try:
    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        blocksize=BLOCK_SIZE,
        channels=1,
        dtype="float32",
        callback=audio_callback,
    ):
        print("Streaming… press Ctrl+C in the console to stop.")
        print(f"Audio will be saved to: {AUDIO_FILE}")
        print(f"Spectrogram frames to: {SPEC_FILE}")

        while True:
            try:
                block = audio_queue.get(timeout=1.0)
            except queue.Empty:
                continue

            audio_blocks.append(block.copy())

            # No overlap: fft_buffer == block
            fft_buffer[:] = block

            # Multitaper FFT
            segment = fft_buffer[None, :]
            tapered = multi_windows * segment
            X = np.fft.rfft(tapered, axis=1)
            psd = (np.abs(X) ** 2).mean(axis=0)
            psd = psd[:N_FREQ_BINS]

            mag_db = 10 * np.log10(psd + 1e-12)
            mag_db = np.clip(mag_db, -120, 0)

            # Store for offline video later
            spec_cols.append(mag_db.astype(np.float32))

            # Slide display window
            spec_full[:, :-1] = spec_full[:, 1:]
            spec_full[:, -1] = mag_db

            # crude f0 in vocal band
            mag_voice = mag_db[voice_min_bin:voice_max_bin]
            if np.any(np.isfinite(mag_voice)):
                peak_idx = np.argmax(mag_voice)
                f0_freq = float(freqs[voice_min_bin + peak_idx])
            else:
                f0_freq = np.nan
            f0_hist[:-1] = f0_hist[1:]
            f0_hist[-1] = f0_freq

            # Update plot (no grab_frame, no encoding)
            img_full.set_data(spec_full)
            img_full.set_extent(extent_full)

            img_zoom.set_data(spec_full[voice_min_bin:voice_max_bin, :])
            img_zoom.set_extent(extent_zoom)

            line_f0.set_ydata(f0_hist)

            fig.canvas.draw()
            fig.canvas.flush_events()
            plt.pause(0.0001)

except KeyboardInterrupt:
    print("\nStopped by user.")
except Exception as e:
    print("Error:", e)
finally:
    # ---------- SAVE AUDIO ----------
    if audio_blocks:
        audio = np.concatenate(audio_blocks)
        audio = np.clip(audio, -1.0, 1.0)
        audio_int16 = (audio * 32767).astype(np.int16)
        wavfile.write(AUDIO_FILE, SAMPLE_RATE, audio_int16)
        print(f"Audio saved to: {AUDIO_FILE}")
    else:
        print("No audio captured; not writing WAV.")

    # ---------- SAVE SPECTROGRAM FRAMES ----------
    if spec_cols:
        spec_cols_arr = np.stack(spec_cols, axis=1)  # shape (N_FREQ_BINS, n_frames)
        np.savez(
            SPEC_FILE,
            spec_cols=spec_cols_arr,
            freqs=freqs[:N_FREQ_BINS],
            sample_rate=SAMPLE_RATE,
            block_size=BLOCK_SIZE,
            voice_min_bin=voice_min_bin,
            voice_max_bin=voice_max_bin,
        )
        print(
            f"Spectrogram columns saved to: {SPEC_FILE} "
            f"(shape: {spec_cols_arr.shape})"
        )
    else:
        print("No spectrogram frames captured; not writing NPZ.")
