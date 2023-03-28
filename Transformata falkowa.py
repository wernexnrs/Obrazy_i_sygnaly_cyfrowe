import numpy as np
import matplotlib.pyplot as plt
import os
import pywt
from skimage.io import imsave, imread
from skimage.util import img_as_ubyte
from skimage.exposure import rescale_intensity


def dwt2d(data, max_level):
    LL = data
    for level in range(max_level):
        new_data = LL
        size = LL[1].size / 2
        size = int(size)
        LL = np.zeros((size, size))
        LH = np.zeros((size, size))
        HL = np.zeros((size, size))
        HH = np.zeros((size, size))
        for x in range(0, size * 2, 2):
            for y in range(0, size * 2, 2):
                LL[x // 2][y // 2] = (new_data[x][y] + new_data[x][y + 1] + new_data[x + 1][y] + new_data[x + 1][
                    y + 1]) / 4
                LH[x // 2][y // 2] = (new_data[x][y] + new_data[x][y + 1] - new_data[x + 1][y] - new_data[x + 1][
                    y + 1]) / 4
                HL[x // 2][y // 2] = (new_data[x][y] - new_data[x][y + 1] + new_data[x + 1][y] - new_data[x + 1][
                    y + 1]) / 4
                HH[x // 2][y // 2] = (new_data[x][y] - new_data[x][y + 1] - new_data[x + 1][y] + new_data[x + 1][
                    y + 1]) / 4
        return LL, (LH, HL, HH)


img_name = "lenna.png"
original = imread(os.getcwd() + "/" + img_name, as_gray=True)

LL, (LH, HL, HH) = pywt.dwt2(original, "haar")

fig = plt.figure(figsize=(12, 3))
titles = ['Approximation', ' Horizontal detail', 'Vertical detail', 'Diagonal detail']
for i, a in enumerate([LL, LH, HL, HH]):
    ax = fig.add_subplot(1, 4, i + 1)
    ax.imshow(a, interpolation="nearest", cmap=plt.cm.gray)
    ax.set_title(titles[i], fontsize=10)
    ax.set_xticks([])
    ax.set_yticks([])
fig.tight_layout()
plt.show()


original = rescale_intensity(original, out_range=(0, 1))
LL = rescale_intensity(LL, out_range=(0, 1))
LH = rescale_intensity(LH, out_range=(0, 1))
HL = rescale_intensity(HL, out_range=(0, 1))
HH = rescale_intensity(HH, out_range=(0, 1))

imsave("original.png", img_as_ubyte(original))
imsave("approximation.png", img_as_ubyte(LL))
imsave("horizontal_detail.png", img_as_ubyte(LH))
imsave("vertical_detail.png", img_as_ubyte(HL))
imsave("diagonal_detail.png", img_as_ubyte(HH))