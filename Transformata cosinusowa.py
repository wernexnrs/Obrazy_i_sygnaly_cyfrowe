from scipy.fftpack import dct, idct
# import math
from skimage.io import imread
from skimage.color import rgb2gray
import numpy as np
import matplotlib.pylab as plt
from matplotlib.pyplot import imsave


def dct2(a):
    return dct(dct(a.T, norm='ortho').T, norm='ortho')


def idct2(a):
    return idct(idct(a.T, norm='ortho').T, norm='ortho')

im = rgb2gray(imread('Lenna.png'))
imF = dct2(im)
im1 = idct2(imF)

imsave('original.jpg', im, cmap='gray')
imsave('dct_image.jpg', im1, cmap='gray')
eps = 1e-12
imF_log = np.log(np.abs(imF) + eps)
imF_log = imF_log / np.max(np.abs(imF_log))
imsave('imf_image.jpg', imF_log, cmap='jet')
