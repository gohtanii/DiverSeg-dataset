#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# This implementation is based on the following paper:
# 
# Bhardwaj, Dinesh, and Vinod Pankajakshan. "A JPEG blocking artifact detector for image forensics."
# Signal Processing: Image Communication 68 (2018): 155-161.
#
# If you use this code or find it helpful in your research, please consider citing the original paper.
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# coding: utf-8
import numpy as np
import cv2
from tqdm import tqdm
import os
import argparse
from basicsr.utils import scandir

BLOCK_SIZE = 8

class DCT:
    """
    Discrete Cosine Transform (DCT) class.

    Original code reference:
    https://gist.github.com/TonyMooori/661a2da7cbb389f0a99c     
    """

    def __init__(self, N=BLOCK_SIZE):
        self.N = N
        self.phi_1d = np.array([self._phi(i) for i in range(self.N)])
        self.phi_2d = np.zeros((N, N, N, N))
        for i in range(N):
            for j in range(N):
                phi_i, phi_j = np.meshgrid(self.phi_1d[i], self.phi_1d[j])
                self.phi_2d[i, j] = phi_i * phi_j

    def dct2(self, data):
        reshaped_data = data.reshape(self.N * self.N)
        reshaped_phi_2d = self.phi_2d.reshape(self.N * self.N, self.N * self.N)
        dct_result = np.dot(reshaped_phi_2d, reshaped_data)
        return dct_result.reshape(self.N, self.N)

    def _phi(self, k):
        if k == 0:
            return np.ones(self.N) / np.sqrt(self.N)
        else:
            return np.sqrt(2.0 / self.N) * np.cos((k * np.pi / (2 * self.N)) * (np.arange(self.N) * 2 + 1))

def calc_margin(height, width):
    h_margin = height % BLOCK_SIZE
    w_margin = width % BLOCK_SIZE
    cal_height = height - (h_margin if h_margin >= 4 else h_margin + BLOCK_SIZE)
    cal_width = width - (w_margin if w_margin >= 4 else w_margin + BLOCK_SIZE)
    h_margin = (h_margin + BLOCK_SIZE) if h_margin < 4 else h_margin
    w_margin = (w_margin + BLOCK_SIZE) if w_margin < 4 else w_margin
    return cal_height, cal_width, h_margin, w_margin

def calc_DCT(img, dct, h_block_num, w_block_num):
    dct_img = np.zeros((h_block_num * BLOCK_SIZE, w_block_num * BLOCK_SIZE))
    for h_block in range(h_block_num):
        for w_block in range(w_block_num):
            dct_img[h_block*BLOCK_SIZE:(h_block+1)*BLOCK_SIZE, w_block*BLOCK_SIZE:(w_block+1)*BLOCK_SIZE] = \
                dct.dct2(img[h_block*BLOCK_SIZE:(h_block+1)*BLOCK_SIZE, w_block*BLOCK_SIZE:(w_block+1)*BLOCK_SIZE])
    return dct_img

def calc_V(dct_img, h_block_num, w_block_num):
    V_average = np.zeros((BLOCK_SIZE, BLOCK_SIZE))
    for j in range(BLOCK_SIZE):
        for i in range(BLOCK_SIZE):
            V_sum = 0
            for h_block in range(1, h_block_num-2):
                for w_block in range(1, w_block_num-2):
                    w_idx = BLOCK_SIZE + w_block*BLOCK_SIZE + i
                    h_idx = BLOCK_SIZE + h_block*BLOCK_SIZE + j
                    a = dct_img[h_idx, w_idx]
                    b = dct_img[h_idx, w_idx-BLOCK_SIZE]
                    c = dct_img[h_idx, w_idx+BLOCK_SIZE]
                    d = dct_img[h_idx-BLOCK_SIZE, w_idx]
                    e = dct_img[h_idx+BLOCK_SIZE, w_idx]
                    V = np.sqrt((b+c-2*a)**2 + (d+e-2*a)**2)
                    V_sum += V
            V_average[j, i] = V_sum / ((h_block_num-2) * (w_block_num-2))
    return V_average

def process_image(img, dct):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    height, width = gray_img.shape
    cal_height, cal_width, h_margin, w_margin = calc_margin(height, width)
    h_block_num, w_block_num = cal_height // BLOCK_SIZE, cal_width // BLOCK_SIZE

    dct_img = calc_DCT(gray_img, dct, h_block_num, w_block_num)
    dct_cropped_img = calc_DCT(gray_img[4:, 4:], dct, h_block_num, w_block_num)

    V_average = calc_V(dct_img, h_block_num, w_block_num)
    Vc_average = calc_V(dct_cropped_img, h_block_num, w_block_num)
    D = np.abs((Vc_average - V_average) / V_average)

    return np.sum(D)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detect JPEG blocking artifacts in images and save them.")
    parser.add_argument('--rootpath', type=str, required=True, help="Root directory containing the images.")
    parser.add_argument('--savefile', type=str, required=True, help="File to save the results.")
    parser.add_argument('--suffix', default='png', type=str, help="File extension of the images to process.")
    parser.add_argument("--target_idx_former", type=int, default=0, help="Starting index of the images to process.")
    parser.add_argument("--target_idx_latter", type=int, default=100000000, help="Ending index of the images to process.")
    args = parser.parse_args()

    dct = DCT()

    paths = sorted(list(scandir(args.rootpath, suffix=args.suffix, recursive=True)))
    paths = paths[args.target_idx_former:args.target_idx_latter]

    with open(args.savefile, mode='w') as f:
        for path in tqdm(paths):
            img = cv2.imread(os.path.join(args.rootpath, path))
            D_value = process_image(img, dct)
            f.write(os.path.join(args.rootpath, path) + '\t' + str(D_value) + '\n')
