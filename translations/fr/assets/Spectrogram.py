import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram

# Set global font size for plots
plt.rcParams.update({'font.size': 14})  # Change font size as needed

# Parameters for the first Gaussian pulse
fs = 1000  # Sampling frequency (Hz)
t = np.arange(0, 1, 1/fs)  # Time vector from 0 to 1 second
center_freq1 = 50  # Center frequency of modulation (Hz)
sigma1 = 0.05  # Standard deviation of the Gaussian envelope

# Parameters for the second Gaussian pulse
center_freq2 = 150  # Center frequency of modulation (Hz)
sigma2 = 0.1  # Standard deviation of the Gaussian envelope

# Generate first Gaussian pulse
gaussian_pulse1 = np.exp(-0.5 * ((t - 0.3) / sigma1) ** 2)  # Gaussian envelope centered at t=0.3s
modulated_pulse1 = gaussian_pulse1 * np.cos(2 * np.pi * center_freq1 * t)  # Modulated pulse

# Generate second Gaussian pulse
gaussian_pulse2 = np.exp(-0.5 * ((t - 0.7) / sigma2) ** 2)  # Gaussian envelope centered at t=0.7s
modulated_pulse2 = gaussian_pulse2 * np.cos(2 * np.pi * center_freq2 * t)  # Modulated pulse

# Combine the two pulses
combined_pulse = modulated_pulse1 + modulated_pulse2

# Compute the spectrogram
f, t_spec, Sxx = spectrogram(combined_pulse, fs, nperseg=256, noverlap=128)

# Plot the Gaussian pulses and their spectrogram
plt.figure(figsize=(12, 6))

# Plot the combined Gaussian pulses
plt.subplot(1, 2, 1)
plt.plot(t, combined_pulse, label='Combined Modulated Gaussian Pulses')
plt.xlabel('t (s)', fontsize=16)  # Larger font size for labels
plt.ylabel('x(t)', fontsize=16)  # Larger font size for labels
plt.title('Time Signal', fontsize=18)  # Larger font size for title
plt.grid(True)

# Plot the spectrogram
plt.subplot(1, 2, 2)
plt.pcolormesh(t_spec, f, 10 * np.log10(Sxx), shading='gouraud')
plt.ylabel('f (Hz)', fontsize=16)  # Larger font size for labels
plt.xlabel('t (s)', fontsize=16)  # Larger font size for labels
plt.title('Spectrogram', fontsize=18)  # Larger font size for title
cbar = plt.colorbar(label='Intensity (dB)')
cbar.ax.tick_params(labelsize=14)  # Font size for colorbar ticks
cbar.set_label('Intensity (dB)', fontsize=16)  # Font size for colorbar label

# Adjust layout

plt.subplots_adjust(wspace=0.4)  # Increase horizontal space between subplots


# Save and display the plot
plt.savefig("spectrogram.png")
plt.show()
