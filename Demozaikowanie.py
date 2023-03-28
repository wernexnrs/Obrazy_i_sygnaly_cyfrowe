import numpy as np
import time
import cv2
import copy
from math import log10, sqrt


def nearest_neightbor(matrix, pattern):
    height, width, _ = matrix.shape

    working_image = copy.deepcopy(matrix)

    for x in range(height):
        for y in range(width):
            for ii in range(max(0, x - 1), min(height, x + 2)):
                for jj in range(max(0, y - 1), min(width, y + 2)):

                    if pattern[x][y] == pattern[ii][jj]:
                        continue
                    elif any(subpixel == 0 for subpixel in working_image[x][y]):
                        match pattern[x][y]:
                            case 0:
                                if pattern[ii][jj] == 1:
                                    working_image[x][y][1] = working_image[ii][jj][1]
                                elif pattern[ii][jj] == 2:
                                    working_image[x][y][2] = working_image[ii][jj][2]

                            case 1:
                                if pattern[ii][jj] == 0:
                                    working_image[x][y][0] = working_image[ii][jj][0]
                                elif pattern[ii][jj] == 2:
                                    working_image[x][y][2] = working_image[ii][jj][2]

                            case 2:
                                if pattern[ii][jj] == 0:
                                    working_image[x][y][0] = working_image[ii][jj][0]
                                elif pattern[ii][jj] == 1:
                                    working_image[x][y][1] = working_image[ii][jj][1]
    return working_image


def bilinear(matrix, pattern):
    height, width, _ = matrix.shape

    working_image = copy.deepcopy(matrix)

    for x in range(height):
        for y in range(width):

            red = []
            green = []
            blue = []

            for ii in range(max(0, x - 1), min(height, x + 2)):
                for jj in range(max(0, y - 1), min(width, y + 2)):
                    if pattern[x][y] == pattern[ii][jj]:
                        continue
                    else:
                        match pattern[x][y]:
                            case 0:
                                if pattern[ii][jj] == 1:
                                    green.append(working_image[ii][jj][1])
                                elif pattern[ii][jj] == 2:
                                    blue.append(working_image[ii][jj][2])

                            case 1:
                                if pattern[ii][jj] == 0:
                                    red.append(working_image[ii][jj][0])
                                elif pattern[ii][jj] == 2:
                                    blue.append(working_image[ii][jj][2])

                            case 2:
                                if pattern[ii][jj] == 0:
                                    red.append(working_image[ii][jj][0])
                                elif pattern[ii][jj] == 1:
                                    green.append(working_image[ii][jj][1])
            if red:
                working_image[x][y][0] = round(sum(red) / len(red), 0)
            if green:
                working_image[x][y][1] = round(sum(green) / len(green), 0)
            if blue:
                working_image[x][y][2] = round(sum(blue) / len(blue), 0)
    return working_image


'''
Chyba nie działa nie pamietam
def biqubic(matrix, pattern):
    height, width, _ = matrix.shape

    working_image = copy.deepcopy(matrix)

    for x in range(height):
        for y in range(width):

            red = []
            green = []
            blue = []

            zakres = 2
            for ii in range(max(0, x - zakres), min(height, x + zakres + 1)):
                for jj in range(max(0, y - zakres), min(width, y + zakres + 1)):
                    if pattern[x][y] == pattern[ii][jj]:
                        continue
                    else:
                        match pattern[x][y]:
                            case 0:
                                if pattern[ii][jj] == 1:
                                    green.append(working_image[ii][jj][1]*0.5)
                                elif pattern[ii][jj] == 2:
                                    blue.append(working_image[ii][jj][2]*0.5)

                            case 1:
                                if pattern[ii][jj] == 0:
                                    red.append(working_image[ii][jj][0]*0.5)
                                elif pattern[ii][jj] == 2:
                                    blue.append(working_image[ii][jj][2]*0.5)

                            case 2:
                                if pattern[ii][jj] == 0:
                                    red.append(working_image[ii][jj][0]*0.5)
                                elif pattern[ii][jj] == 1:
                                    green.append(working_image[ii][jj][1]*0.5)
            if red:
                working_image[x][y][0] = round((sum(red)/ len(red)) , 0)
            if green:
                working_image[x][y][1] = round((sum(green) / len(green)), 0)
            if blue:
                working_image[x][y][2] = round((sum(blue)/ len(blue)), 0)

    return working_image
'''


def create_bayer_pattern(original_image):
    """
    G B
    R G

    With BGR TO RGB conversion.
    """

    original_image = original_image[:, :, ::-1]  # BGR2RGB

    working_image_bayer = np.zeros(original_image.shape, dtype=np.uint8)

    working_image_bayer[::2, ::2, 1] = original_image[::2, ::2, 1]

    working_image_bayer[::2, 1::2, 0] = original_image[::2, 1::2, 2]
    working_image_bayer[1::2, ::2, 2] = original_image[1::2, ::2, 0]

    working_image_bayer[1::2, 1::2, 1] = original_image[1::2, 1::2, 1]

    bayer_pattern[::2, ::2] = 1
    bayer_pattern[::2, 1::2] = 0
    bayer_pattern[1::2, ::2] = 2
    bayer_pattern[1::2, 1::2] = 1

    return working_image_bayer


def create_fuji_pattern(original_image):
    """
    G B R G R B
    R G G B G G
    B G G R G G
    G R B G B R
    B G G R G G
    R G G B G G

    With BGR TO RGB conversion.
    """

    working_image_fuji = np.zeros(original_image.shape, dtype=np.uint8)

    working_image_fuji[::6, ::6, 1] = original_image[::6, ::6, 1]  # G
    working_image_fuji[::6, 1::6, 0] = original_image[::6, 1::6, 0]  # B
    working_image_fuji[::6, 2::6, 2] = original_image[::6, 2::6, 2]  # R
    working_image_fuji[::6, 3::6, 1] = original_image[::6, 3::6, 1]  # G
    working_image_fuji[::6, 4::6, 2] = original_image[::6, 4::6, 2]  # R
    working_image_fuji[::6, 5::6, 0] = original_image[::6, 5::6, 0]  # B

    for x in range(1, 6, 4):
        working_image_fuji[x::6, ::6, 2] = original_image[x::6, ::6, 2]  # R
        working_image_fuji[x::6, 1::6, 1] = original_image[x::6, 1::6, 1]  # G
        working_image_fuji[x::6, 2::6, 1] = original_image[x::6, 2::6, 1]  # G
        working_image_fuji[x::6, 3::6, 0] = original_image[x::6, 3::6, 0]  # B
        working_image_fuji[x::6, 4::6, 1] = original_image[x::6, 4::6, 1]  # G
        working_image_fuji[x::6, 5::6, 1] = original_image[x::6, 5::6, 1]  # G

    for x in range(2, 5, 2):
        working_image_fuji[x::6, ::6, 0] = original_image[x::6, ::6, 0]  # B
        working_image_fuji[x::6, 1::6, 1] = original_image[x::6, 1::6, 1]  # G
        working_image_fuji[x::6, 2::6, 1] = original_image[x::6, 2::6, 1]  # G
        working_image_fuji[x::6, 3::6, 2] = original_image[x::6, 3::6, 2]  # R
        working_image_fuji[x::6, 4::6, 1] = original_image[x::6, 4::6, 1]  # G
        working_image_fuji[x::6, 5::6, 1] = original_image[x::6, 5::6, 1]  # G

    working_image_fuji[3::6, ::6, 1] = original_image[3::6, ::6, 1]  # G
    working_image_fuji[3::6, 1::6, 2] = original_image[3::6, 1::6, 2]  # R
    working_image_fuji[3::6, 2::6, 0] = original_image[3::6, 2::6, 0]  # B
    working_image_fuji[3::6, 3::6, 1] = original_image[3::6, 3::6, 1]  # G
    working_image_fuji[3::6, 4::6, 0] = original_image[3::6, 4::6, 0]  # B
    working_image_fuji[3::6, 5::6, 2] = original_image[3::6, 5::6, 2]  # R

    fuji_pattern[::6, ::6] = 1  # "G"
    fuji_pattern[::6, 1::6] = 0  # "B"
    fuji_pattern[::6, 2::6] = 2  # "R"
    fuji_pattern[::6, 3::6] = 1  # "G"
    fuji_pattern[::6, 4::6] = 2  # "R"
    fuji_pattern[::6, 5::6] = 0  # "B"

    for x in range(1, 6, 4):
        fuji_pattern[x::6, ::6] = 2  # "R"
        fuji_pattern[x::6, 1::6] = 1  # "G"
        fuji_pattern[x::6, 2::6] = 1  # "G"
        fuji_pattern[x::6, 3::6] = 0  # "B"
        fuji_pattern[x::6, 4::6] = 1  # "G"
        fuji_pattern[x::6, 5::6] = 1  # "G"

    for x in range(2, 5, 2):
        fuji_pattern[x::6, ::6] = 0  # "B"
        fuji_pattern[x::6, 1::6] = 1  # "G"
        fuji_pattern[x::6, 2::6] = 1  # "G"
        fuji_pattern[x::6, 3::6] = 2  # "R"
        fuji_pattern[x::6, 4::6] = 1  # "G"
        fuji_pattern[x::6, 5::6] = 1  # "G"

    fuji_pattern[3::6, ::6] = 1  # "G"
    fuji_pattern[3::6, 1::6] = 2  # "R"
    fuji_pattern[3::6, 2::6] = 0  # "B"
    fuji_pattern[3::6, 3::6] = 1  # "G"
    fuji_pattern[3::6, 4::6] = 0  # "B"
    fuji_pattern[3::6, 5::6] = 2  # "R"

    return working_image_fuji


def psnr_db(original, demosaic):
    mse = np.mean((original - demosaic) ** 2)
    if mse == 0:
        return 100
    return round(20 * log10(255 / sqrt(mse)), 5)


start = time.time()

img = cv2.imread("4demosaicking.bmp")

image_shape = img.shape

bayer_pattern = np.zeros((image_shape[0], image_shape[1]), dtype=np.uint8)
fuji_pattern = np.zeros((image_shape[0], image_shape[1]), dtype=np.uint8)

img_bayer = create_bayer_pattern(img)
img_fuji = create_fuji_pattern(img)

cv2.imwrite(r"wyniki\Bayer_Pattern.png", img_bayer)
cv2.imwrite(r"wyniki\X-Trans_Pattern.png", img_fuji)

demosaic_bayer_bilinear = bilinear(img_bayer, bayer_pattern)
cv2.imwrite(r"wyniki\Demosaiced_Bayer_Bilinear.png", demosaic_bayer_bilinear)

demosaic_fuji_bilinear = bilinear(img_fuji, fuji_pattern)
cv2.imwrite(r"wyniki\Demosaiced_Fuji_Bilinear.png", demosaic_fuji_bilinear)

print("Bayer_bilinear: ", psnr_db(img, demosaic_bayer_bilinear), "dB")
print("Fuji_bilinear: ", psnr_db(img, demosaic_fuji_bilinear), "dB")

cv2.imwrite(r"wyniki\Bayer_Difference_Bilinear.png", (img - demosaic_bayer_bilinear) ** 2)
cv2.imwrite(r"wyniki\Fuji_Difference_Bilinear.png", (img - demosaic_fuji_bilinear) ** 2)

demosaic_bayer_nearest = nearest_neightbor(img_bayer, bayer_pattern)
demosaic_fuji_nearest = nearest_neightbor(img_fuji, fuji_pattern)

cv2.imwrite(r"wyniki\Demosaiced_Bayer_Nearest.png", demosaic_bayer_nearest)
cv2.imwrite(r"wyniki\Demosaiced_Fuji_Nearest.png", demosaic_fuji_nearest)

print("Bayer_Nearest: ", psnr_db(img, demosaic_bayer_nearest), "dB")
print("Fuji_Nearest: ", psnr_db(img, demosaic_fuji_nearest), "dB")

cv2.imwrite(r"wyniki\Bayer_Difference_Nearest.png", (img - demosaic_bayer_nearest) ** 2)
cv2.imwrite(r"wyniki\Fuji_Difference_Nearest.png", (img - demosaic_fuji_nearest) ** 2)

end = time.time()

print("Execute time: ", round(end - start, 2))
