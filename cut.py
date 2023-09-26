import sys
import os
import cv2
import numpy as np
import random

def augment_image(image):

    augmentations = [cv2.flip, cv2.rotate]

    for augmentation in augmentations:
        if random.random() < 0.5:
            image = augmentation(image, random.choice([0, 1]))

    return image

def cut_image(input_image, M, N, save_dir):

    image = cv2.imread(input_image)

    height, width, _ = image.shape
    new_height = height // M * M
    new_width = width // N * N
    image = image[:new_height, :new_width]

    sub_images = []
    sub_height = new_height // M
    sub_width = new_width // N

    for i in range(M):
        for j in range(N):
            sub = image[i * sub_height:(i + 1) * sub_height, j * sub_width:(j + 1) * sub_width]
            sub = augment_image(sub)
            

            filename = os.path.join(save_dir, f'sub_{i:02d}_{j:02d}_{random.randint(0, 9999999999):010d}.jpg')
            cv2.imwrite(filename, sub)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("사용법: cut.py {input_image_name} {M(row_num)} {N(col_num)} {save_dir}")
        sys.exit(1)

    input_image = sys.argv[1]
    M = int(sys.argv[2])
    N = int(sys.argv[3])
    save_dir = sys.argv[4]


    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    else:
        for file in os.listdir(save_dir):
            os.remove(os.path.join(save_dir, file))

    cut_image(input_image, M, N, save_dir)
