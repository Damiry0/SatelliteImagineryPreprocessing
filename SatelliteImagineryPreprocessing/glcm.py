import numpy as np
import matplotlib.pyplot as plt
import cv2
from skimage.feature import graycomatrix, graycoprops
import PIL
import time
import math

PIL.Image.MAX_IMAGE_PIXELS = 200000000

def slow_glcm(img, vmin=0, vmax=255, levels=256, distances=None, angles=None):
    if distances is None:
        distances = [1]
    h, w = img.shape
    glcm = np.zeros((levels, levels, len(distances), len(angles)), dtype=np.uint32)
    bins = np.linspace(vmin, vmax + 1, levels + 1)
    gl1 = np.digitize(img, bins) - 1

    for angle in angles:
        for distance in distances:
            row_off = round(math.sin(angle) * distance)
            col_off = round(math.cos(angle) * distance)
            start_row = max(0, -row_off)
            end_row = min(h, h - row_off)
            start_col = max(0, -col_off)
            end_col = min(w, w - col_off)
            for i in range(levels):
                for j in range(levels):
                    for x in range(start_row, end_row):
                        for y in range(start_col, end_col):
                            dx = x + row_off
                            dy = y + col_off
                            if gl1[x, y] == i and gl1[dx, dy] == j:
                                glcm[i, j, 0, 0] += 1
    return glcm


def glcm_mean(glcm_matrix, levels=8):
    mean = 0.0
    for i in range(levels):
        for j in range(levels):
            mean += glcm_matrix[i, j] * i / (levels) ** 2

    return mean


def glcm_normalize(glcm_matrix, levels=8):
    glcm_sums = np.sum(glcm_matrix, axis=(0, 1), keepdims=True)
    glcm_sums[glcm_sums == 0] = 1
    glcm_matrix = glcm_matrix / glcm_sums
    return glcm_matrix


def glcm_contrast(glcm_matrix, levels=8):
    contrast = 0.0
    glcm = glcm_matrix.astype(np.float64)
    glcm_norm = glcm_normalize(glcm, levels)
    for i in range(levels):
        for j in range(levels):
            contrast += np.sum(glcm_norm[i, j] * (i - j) ** 2)

    return contrast


def glcm_homogeneity(glcm_matrix, levels=8):
    homo = 0.0
    glcm = glcm_matrix.astype(np.float64)
    glcm_norm = glcm_normalize(glcm, levels)
    for i in range(levels):
        for j in range(levels):
            homo += np.sum(glcm_norm[i, j] * (1./1. + (np.abs(i - j)**2)))
    return homo


def glcm_energy(glcm_matrix, levels=8):
    glcm = glcm_matrix.astype(np.float64)
    glcm_norm = glcm_normalize(glcm, levels)
    asm = np.sum(glcm_norm ** 2, axis=(0, 1))
    results = np.sqrt(asm)

    return results


imagin = plt.imread(r"Examples/rat.jpg")
img_gray = cv2.cvtColor(imagin, cv2.COLOR_BGR2GRAY)
bins = np.linspace(0, 255 + 1, 8 + 1)
gl1 = np.digitize(img_gray, bins) - 1
# image = np.array([[0, 0, 1, 1],
#                   [0, 0, 1, 1],
#                   [0, 2, 2, 2],
#                   [2, 2, 3, 3]], dtype=np.uint8)
start_time = time.time()
result = graycomatrix(gl1, [1], [0], levels=8)
contrast_1 = graycoprops(result, 'contrast')
end_time = time.time()
res = end_time - start_time
final_res = res * 1000
print('Execution time:', final_res, 'milliseconds')
start_time_2 = time.time()
glcm = slow_glcm(img_gray, levels=8, distances=[1], angles=[0])
contrast = glcm_contrast(glcm)
end_time_2 = time.time()
res_2 = end_time_2 - start_time_2
final_res_2 = res_2 * 1000
print('Execution time:', final_res_2, 'milliseconds')
