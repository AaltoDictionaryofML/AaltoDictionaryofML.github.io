import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from torchvision.datasets import MNIST
from torchvision import transforms
from torchvision.transforms import functional as TF
import torch
from torch.utils.data import DataLoader
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

# Parameters
angles = np.linspace(-30, 30, 25)
num_digits = 2
inlay_step = 6  # Add image inlay every 6 rotations

# Load MNIST
mnist = MNIST(root="./data", download=True, train=False, transform=transforms.ToTensor())
loader = DataLoader(mnist, batch_size=len(mnist))
images, labels = next(iter(loader))

# Select two distinct digits
selected_digits = []
selected_labels = []
for digit in range(10):
    idx = (labels == digit).nonzero()[0]
    if len(idx) > 0:
        selected_digits.append(images[idx[0]])
        selected_labels.append(digit)
    if len(selected_digits) == num_digits:
        break

# Rotate images and collect data
rotated_images = []
original_images = []
color_labels = []

for i, img in enumerate(selected_digits):
    for angle in angles:
        rotated = TF.rotate(img, angle, interpolation=TF.InterpolationMode.BILINEAR)
        rotated_images.append(rotated.view(-1).numpy())
        original_images.append(rotated.squeeze().numpy())
        color_labels.append(i)

rotated_images = np.array(rotated_images)

# Reduce to 2D using PCA
pca = PCA(n_components=2)
embedding = pca.fit_transform(rotated_images)
offset_xybox = (400, 400)  # offset in display points

# Plot
fig, ax = plt.subplots(figsize=(10, 8))
colors = ['blue', 'green']
for i in range(num_digits):
    inds = [j for j, lbl in enumerate(color_labels) if lbl == i]
    ax.plot(embedding[inds, 0], embedding[inds, 1], 'o-', label=f'Digit {selected_labels[i]}', color=colors[i])

    # Add image inlays
    for k in range(0, len(inds), inlay_step):
        j = inds[k]
        emb_xy = embedding[j]
        imagebox = OffsetImage(original_images[j], cmap='gray', zoom=1.0)
        # Convert data coordinates to display (pixel) coordinates
        disp_xy = ax.transData.transform(emb_xy)

        # Add the offset
        offset_disp_xy = disp_xy + np.array(offset_xybox)

        # Convert back to data coordinates
        offset_data_xy = ax.transData.inverted().transform(offset_disp_xy)

        # Draw the line manually
        ax.plot([emb_xy[0], offset_data_xy[0]], [emb_xy[1], offset_data_xy[1]],
                color=colors[i], linewidth=0.5, linestyle='-')

        # Place the image
        ab = AnnotationBbox(
            imagebox,
            offset_data_xy,
            frameon=False,
            xycoords='data'
        )
      #  ab = AnnotationBbox(imagebox, embedding[j],  xybox=(20, 20),           # offset in screen/display points (x, y)
    #xycoords='data',
   # boxcoords='offset points',frameon=False)
        ax.add_artist(ab)

# Compute geometric center of all embedded points
center = embedding.mean(axis=0)

start = [0, 0]     # Start coordinates in data space
end = [-1, 4]     # End coordinates

# Draw a simple line
#ax.plot([start[0], end[0]], [start[1], end[1]], color='black', linewidth=2)
midpoint = [(start[0] + end[0]) / 2, (start[1] + end[1]) / 2]
ax.text(midpoint[0] + 0.1, midpoint[1], r"$\mathbf{n}$", fontsize=22)

# Draw the arrow
ax.annotate(
    '', 
    xy=end, 
    xytext=start,
    arrowprops=dict(
        arrowstyle='->',
        color='black',
        lw=2,
        mutation_scale=20  # controls arrowhead size
    )
)


#ax.set_title("2D PCA Embedding of Rotated MNIST Digits with Image Inlays")
ax.set_xlabel("x1")
ax.set_ylabel("x2")
#ax.legend()
ax.grid(True)
plt.tight_layout()
plt.savefig("nullspace.png", dpi=300, bbox_inches='tight')
plt.show()
