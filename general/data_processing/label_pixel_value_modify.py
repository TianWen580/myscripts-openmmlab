import os
import cv2
from tqdm import tqdm

labels_path = r'D:\shshsh'
target_value = 1

files = os.listdir(labels_path)
files.sort()

for f in tqdm(files):
    lbl_path = os.path.join(labels_path, f)
    label = cv2.imread(lbl_path, cv2.IMREAD_GRAYSCALE)
    label[label > 0] = target_value
    cv2.imwrite(lbl_path, label)
