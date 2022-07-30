# -*- coding: utf-8 -*-
import numpy as np
import cv2
import random
import os

# calculate means and std  注意换行\n符号
path = '~/images_id.txt' # 先生成记录图片数据路径的txt文件
means = [0, 0, 0]
stdevs = [0, 0, 0]

index = 1
num_imgs = 0
print('计算中，这可能会花费一两分钟...')
with open(path, 'r') as f:
    lines = f.readlines()
    # random.shuffle(lines)
    times = 1.5  # 计算量倍数
    for index in range((int)(len(lines) * times)):
        x = random.randint(0, len(lines) - 1)
        line = lines[x]
        # print(line)
        # print('{}/{}'.format(index, len(lines)))
        index += 1
        a = os.path.join(line)
        # print(a[:-1])
        num_imgs += 1
        img = cv2.imread(a[:-1])
        img = np.asarray(img)
        img = img.astype(np.float32) / 255.
        for i in range(3):
            means[i] += img[:, :, i].mean()
            stdevs[i] += img[:, :, i].std()

means.reverse()
stdevs.reverse()

means = np.asarray(means) / num_imgs
stdevs = np.asarray(stdevs) / num_imgs

print("normMean = {}".format(means))
print("normStd = {}".format(stdevs))
print('transforms.Normalize({},{})'.format(means, stdevs))
