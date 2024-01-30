import cupy
import numpy as np
import matplotlib.pyplot as plt
import cv2
import PIL
import math
import cupy as cp
import time

PIL.Image.MAX_IMAGE_PIXELS = 200000000


def gpu_glcm(img, vmin=0, vmax=255, levels=256, distances=None, angles=None):
    start_time = time.time()
    if distances is None:
        distances = [1]
    h, w = img.shape
    glcm = cp.zeros((levels, levels, len(distances), len(angles)), dtype=cp.uint32)
    bins = cp.linspace(vmin, vmax + 1, levels + 1)
    img = cupy.array(img)
    gl1 = cp.digitize(img, bins) - 1

    for angle in angles:
        for distance in distances:
            row_off = int(cp.round(cp.sin(angle) * distance))
            col_off = int(cp.round(cp.cos(angle) * distance))
            start_row = max(0, -row_off)
            end_row = min(h, h - row_off)
            start_col = max(0, -col_off)
            end_col = min(w, w - col_off)
            for i in range(levels):
                for j in range(levels):
                    dx = cp.arange(start_row, end_row) + row_off
                    dy = cp.arange(start_col, end_col) + col_off
                    dx_grid, dy_grid = cp.meshgrid(dx, dy, indexing='ij')
                    mask = (gl1[start_row:end_row, start_col:end_col] == i) & (gl1[dx_grid, dy_grid] == j)
                    glcm[i, j, 0, 0] += int(cp.sum(mask))
    end_time = time.time()
    res = end_time - start_time
    final_res = res * 1000
    print('Execution time GPU:', final_res, 'milliseconds, Number of levels: ', levels)
    return glcm


def slow_glcm(img, vmin=0, vmax=255, levels=256, distances=None, angles=None):
    print("Running glcm")
    if distances is None:
        distances = [1]
    h, w = img.shape
    glcm = np.zeros((levels, levels, len(distances), len(angles)), dtype=np.uint32)
    # bins = np.linspace(vmin, vmax + 1, levels + 1)
    # gl1 = np.digitize(img, bins) - 1

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
                            if (img[x, y] == i) and (img[dx, dy] == j):
                                glcm[i, j, 0, 0] += 1
    return glcm




if __name__ == "__main__":
    imagin = plt.imread(r"ratter.jpg")
    img_gray = cv2.cvtColor(imagin, cv2.COLOR_BGR2GRAY)
    result = gpu_glcm(img_gray, vmin=0, vmax=255, levels=32, distances=[1], angles=[0])

