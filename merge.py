import sys
import os
import cv2
import numpy as np
import random
import glob

def augment_image(image):
    augmentations = [cv2.flip, cv2.rotate]

    for augmentation in augmentations:
        if random.random() < 0.5:
            image = augmentation(image, random.choice([0, 1]))

    return image

def merge_images(input_dir, M, N, result_img_name):
    images = []

    for i in range(M):
        row_images = []
        for j in range(N):
            filename = os.path.join(input_dir, f'sub_{i:02d}_{j:02d}_*.jpg')
            sub_images = []

            for file in glob.glob(filename):
                sub_image = cv2.imread(file)
                sub_images.append(sub_image)

            augmented_sub_image = random.choice(sub_images)

            row_images.append(augmented_sub_image)


        min_height = min(image.shape[0] for image in row_images)
        row_images = [image[:min_height, :] for image in row_images]

        images.append(np.hstack(row_images))


    min_width = min(image.shape[1] for image in images)
    images = [image[:, :min_width] for image in images]

    result_image = np.vstack(images)

    cv2.imwrite(result_img_name, result_image)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("사용법: merge.py {input_dir} {M} {N} {result_img_name}")
        sys.exit(1)

    input_dir = sys.argv[1]
    M = int(sys.argv[2])
    N = int(sys.argv[3])
    result_img_name = sys.argv[4]

    merge_images(input_dir, M, N, result_img_name)
