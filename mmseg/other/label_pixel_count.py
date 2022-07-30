import os
import random
import cv2 as cv
from tqdm import tqdm
from matplotlib import pyplot as plt

labels_path = 'data/xxx/annotations/training'
imgs_path = 'data/xxx/images/training'
randomKey = int(input('是否开启随机质检（是:1 否:-1）'))

files = os.listdir(labels_path)
counter = []


def pixels_counter(img):
    for row in range(img.shape[0]):
        for col in range(img.shape[1]):
            current_pixel = img[row][col]
            if current_pixel not in counter:
                counter.append(current_pixel)


# 随机质检
if randomKey == 1:
    for i in tqdm(range(len(files))):
        file = random.choice(files)
        label = cv.imread(os.path.join(labels_path, file), cv.IMREAD_GRAYSCALE)
        pixels_counter(label)
        label = label * 30
        img = cv.imread(os.path.join(imgs_path, file[:-4] + '.jpg'))

        plt.subplot(3, 2, 1)
        plt.imshow(img, cmap='gray')
        plt.title(str(counter))
        plt.subplot(3, 2, 2)
        plt.imshow(label, cmap='gray')
        plt.title(str(counter))

        plt.ion()
        plt.pause(2)
        plt.close()

        counter = []
else:
    for file in tqdm(files):
        label = cv.imread(os.path.join(labels_path, file), cv.IMREAD_GRAYSCALE)
        pixels_counter(label)
        label = label * 30
        cv.imshow(str(counter), label)
        cv.waitKey()

