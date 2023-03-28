import numpy as np
import cv2

def create_kernel(size, rodzaj):
    if size % 2 == 0:
        raise TypeError("Only odd integers are allowed")
    else:
        if rodzaj == "Gaussian":
            if size == 3:
                return np.array([[1, 2, 1],
                                [2, 4, 2],
                                [1, 2, 1]])
            elif size == 5:
                return np.array([[1, 4,  6 , 4, 1],
                                [4, 16, 24, 16, 4],
                                [6, 24, 36, 24, 6],
                                [4, 16, 24, 16, 4],
                                [1, 4, 6, 4, 1]])
        elif rodzaj == "Box":
            return np.ones((size,size))

def median_filtr(szum, kernel_size):
    height, width, dim = szum.shape
    padded = cv2.copyMakeBorder(szum, kernel_size//2, kernel_size//2, kernel_size//2, kernel_size//2, cv2.BORDER_REPLICATE)

    filtered = np.zeros((height, width, dim), dtype=np.uint8)

    for x in range(height):
        for y in range(width):
            area = padded[x:x+kernel_size, y:y+kernel_size, :]

            filtered[x, y, 0] = np.median(area[:,:,0])
            filtered[x, y, 1] = np.median(area[:,:,1])
            filtered[x, y, 2] = np.median(area[:,:,2])
    return filtered

def splot_filtr(szum, kernel_type, kernel_size):
    height, width, dim = szum.shape
    filtered = np.zeros((height, width, dim), dtype=np.uint8)
    kernel = create_kernel(kernel_size, kernel_type)
    suma = np.sum(kernel)
    padded = cv2.copyMakeBorder(szum, kernel_size//2, kernel_size//2, kernel_size//2, kernel_size//2, cv2.BORDER_REPLICATE)
    for x in range(height):
        for y in range(width):
            area = padded[x:x+kernel_size, y:y+kernel_size, :]
            for i in range(3):
                filtered[x, y, i] = np.sum(area[:,:,i] * kernel) / suma
    return filtered

def psnr_db(img1, img2):
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        return 100
    PIXEL_MAX = 255.0
    return round(10 * np.log10(PIXEL_MAX**2 / mse),5)


working_image = cv2.imread("Leopard-with-noise.jpg")
no_noise_image = cv2.imread("Leopard.jpg")

median_border_replicate_10 = median_filtr(working_image, 10)
cv2.imwrite(r"Wyniki\roznica_median_border_replicate_10.png", (no_noise_image - median_border_replicate_10) ** 2)

median_border_replicate_3 = median_filtr(working_image, 3)
median_border_replicate_5 = median_filtr(working_image, 5)
median_border_replicate_7 = median_filtr(working_image,7)

cv2.imwrite(r"Wyniki\roznica_median_border_replicate_3.png", (no_noise_image - median_border_replicate_3) ** 2)
cv2.imwrite(r"Wyniki\roznica_median_border_replicate_5.png", (no_noise_image - median_border_replicate_5) ** 2)
cv2.imwrite(r"Wyniki\roznica_median_border_replicate_7.png", (no_noise_image - median_border_replicate_7) ** 2)

# median 3x3
print("Kernel size: 3x3")
print("border_replicate: ", psnr_db(no_noise_image, median_border_replicate_3), "dB", "vs cv2", psnr_db(median_border_replicate_3, cv2.medianBlur(working_image, 3)))
cv2.imwrite(r"Wyniki\median_border_replicate_3.png", median_border_replicate_3)

# median 5x5
print("Kernel size: 5x5")
print("border_replicate: ", psnr_db(no_noise_image, median_border_replicate_5), "dB", "vs cv2", psnr_db(median_border_replicate_5, cv2.medianBlur(working_image, 5)))
cv2.imwrite(r"Wyniki\median_border_replicate_5.png", median_border_replicate_5)

# median 7x7
print("Kernel size: 7x7")
print("border_replicate: ", psnr_db(no_noise_image, median_border_replicate_7), "dB", "vs cv2", psnr_db(median_border_replicate_7, cv2.medianBlur(working_image, 7)))
cv2.imwrite(r"Wyniki\median_border_replicate_7.png", median_border_replicate_7)