import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
import copy


def lowPassFiltering(work_img, size):
    img = copy.deepcopy(work_img)
    h, w = img.shape[0:2]
    h1, w1 = int(h / 2), int(w / 2)
    img[0:h, 0:w1 - int(size / 2)] = 0
    img[0:h, w1 + int(size / 2):w] = 0
    img[0:h1 - int(size / 2), 0:w] = 0
    img[h1 + int(size / 2):h, 0:w] = 0
    return img

def highPassFiltering(work_img, size):
    img = copy.deepcopy(work_img)
    h, w = img.shape[0:2]
    h1, w1 = int(h / 2), int(w / 2)
    img[h1 - size:h1 + size, w1 - size:w1 + size] = 0
    return img



image = cv2.imread('Lenna.png')
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


dft = np.fft.fft2(gray_image)
dft_shift = np.fft.fftshift(dft)

filtered_img_high = highPassFiltering(dft_shift, size=20)
filtered_img_low = lowPassFiltering(dft_shift, size=20)

idft_shift_high = np.fft.ifftshift(filtered_img_high)
ifimg_high = np.fft.ifft2(idft_shift_high)
ifimg_high = np.abs(ifimg_high).astype(np.uint8)
idft_shift_low = np.fft.ifftshift(filtered_img_low)
ifimg_low = np.fft.ifft2(idft_shift_low)
ifimg_low = np.abs(ifimg_low).astype(np.uint8)
cv2.imwrite('original.jpg', gray_image)
cv2.imwrite('high_pass_filtered.jpg', ifimg_high)
cv2.imwrite('low_pass_filtered.jpg', ifimg_low)