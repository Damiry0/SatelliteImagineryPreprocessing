import multiprocessing

import numpy as np
import matplotlib.pyplot as plt
import cv2
import time
import math

times = []

def glc_loop(i,levels,start_row,end_row,start_col,end_col,row_off,col_off,gl1,glcm):
    for j in range(levels):
        for x in range(start_row, end_row):
            for y in range(start_col, end_col):
                dx = x + row_off
                dy = y + col_off
                if gl1[x, y] == i and gl1[dx, dy] == j:
                    glcm[i, j, 0, 0] += 1


def glcm_parrarel(img, vmin=0, vmax=255, levels=256, distances=None, angles=None,num_processors=1):
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
            starttime = time.time()
            processes = []

            with multiprocessing.Pool(processes=num_processors) as pool:
                pool.starmap(glc_loop, [(i, levels, start_row, end_row, start_col, end_col, row_off, col_off, gl1,glcm) for i in range(levels)])

            print('That took {} ms'.format((time.time() - starttime)*1000))
            times.append((time.time() - starttime)*1000)
    return glcm

if __name__ == "__main__":
    imagin = plt.imread(r"ratter.jpg")
    img_gray = cv2.cvtColor(imagin, cv2.COLOR_BGR2GRAY)
    for num_processors in [1, 2, 3, 4, 5, 8, 16, 32]:
        print(f"Running with {num_processors} processors")
        glcm_parrarel(img_gray, levels=8, distances=[1], angles=[0], num_processors=num_processors)
    print(times)
