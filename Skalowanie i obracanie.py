import numpy as np
import cv2
import math


def bl_resize(original_img, new_h, new_w):
    old_h, old_w, c = original_img.shape
    resized = np.zeros((new_h, new_w, c))
    w_scale_factor = old_w / new_w if new_h != 0 else 0
    h_scale_factor = old_h / new_h if new_w != 0 else 0

    for i in range(new_h):
        for j in range(new_w):
            x = i * h_scale_factor
            y = j * w_scale_factor
            x_floor = math.floor(x)
            y_floor = math.floor(y)
            x_ceil = min(old_h - 1, math.ceil(x))
            y_ceil = min(old_w - 1, math.ceil(y))

            if x_ceil == x_floor and y_ceil == y_floor:
                resized[i, j, :] = original_img[x_floor, y_floor, :]
            elif x_ceil == x_floor:
                q1 = original_img[x_floor, y_floor, :]
                q2 = original_img[x_floor, y_ceil, :]
                resized[i, j, :] = q1 * (y_ceil - y) + q2 * (y - y_floor)
            elif y_ceil == y_floor:
                q1 = original_img[x_floor, y_floor, :]
                q2 = original_img[x_ceil, y_floor, :]
                resized[i, j, :] = q1 * (x_ceil - x) + q2 * (x - x_floor)
            else:
                v1 = original_img[x_floor, y_floor, :]
                v2 = original_img[x_ceil, y_floor, :]
                v3 = original_img[x_floor, y_ceil, :]
                v4 = original_img[x_ceil, y_ceil, :]
                q1 = v1 * (x_ceil - x) + v2 * (x - x_floor)
                q2 = v3 * (x_ceil - x) + v4 * (x - x_floor)
                resized[i, j, :] = q1 * (y_ceil - y) + q2 * (y - y_floor)

    return resized


def rotate_image_test(image, angle):
    height, width = image.shape[:2]

    angle *= math.pi / 180

    new_width = int(abs(height * math.sin(angle)) + abs(width * math.cos(angle)))
    new_height = int(abs(height * math.cos(angle)) + abs(width * math.sin(angle)))

    center = (new_width // 2, new_height // 2)

    rotated_image = np.zeros((new_height, new_width, 4), dtype=np.uint8)

    for x in range(new_width):
        for y in range(new_height):
            old_x = int(math.cos(angle) * (x - center[0]) + math.sin(angle) * (y - center[1]) + width // 2)
            old_y = int(-math.sin(angle) * (x - center[0]) + math.cos(angle) * (y - center[1]) + height // 2)

            if (0 <= old_x < width) and (0 <= old_y < height):
                rotated_image[y, x, :3] = image[old_y, old_x]
                rotated_image[y, x, 3] = 255

    rotated_image.astype(np.uint8).shape = (new_width, new_height, 4)

    return rotated_image


image = cv2.imread("vangogh.png")

rotated45 = bl_resize(rotate_image_test(image, 45), 125, 125)
rotated90 = bl_resize(rotate_image_test(image, 90), 125, 125)
rotated120 = bl_resize(rotate_image_test(image, 120), 125, 125)
rotated180 = bl_resize(rotate_image_test(image, 180), 125, 125)

cv2.imwrite("rotated45.png", rotated45)
cv2.imwrite("rotated90.png", rotated90)
cv2.imwrite("rotated120.png", rotated120)
cv2.imwrite("rotated180.png", rotated180)

resized300x500 = bl_resize(image, 300, 500)

cv2.imwrite("resized300x500.png", resized300x500)
