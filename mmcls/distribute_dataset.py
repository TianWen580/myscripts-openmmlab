import os
import shutil
from tqdm import tqdm

data_dir = 'data/imagenet/train/'
val_save_dir = 'data/imagenet/val/'
val_rate = 0.3


def move_some_to_val(folder):
    this_save_dir = val_save_dir + folder.split('/')[-1]
    if not os.path.exists(this_save_dir):
        os.mkdir(val_save_dir + folder.split('/')[-1])
    files = os.listdir(folder)
    val_num = len(files) * val_rate
    index = 0
    for file in files:
        if index < val_num:
            shutil.move(folder + '/' + file, this_save_dir)
            index += 1


if __name__ == '__main__':
    f = open('data_path.txt', 'w+')  # 没有则创建txt文件
    fileList = os.listdir(data_dir)
    print('次序预览 >> ', fileList)
    for file in fileList:
        f.write(data_dir + str(file) + '\n')  # 保留文件后缀
    f.close()
    with open('data_path.txt', 'r') as f:
        folders = f.readlines()
        bar = tqdm(folders)
        for folder in bar:
            folder = folder.rstrip('\n')
            move_some_to_val(folder)
            bar.set_description('数据集分配中...')
        bar.close()

    os.remove('data_path.txt')
