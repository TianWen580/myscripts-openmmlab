 # -*- coding: utf-8 -*-
import os
import shutil
from PIL import Image

path = '~/json_folder/data/' # 先把labelme_json_to_datasets.py生成的文件夹从json_folder移到一起


def reName(path):
    files = os.listdir(path)
    # 对文件夹进行遍历
    for j in files:
        file_name, file_extend = os.path.splitext(j)  # 取出图片的名称为new_name
        new_name = file_name.split('j')[0]
        new_name = new_name[0:-1]
        dirpath = path + '\\' + j
        if (os.path.isdir(dirpath)):
            dirpaths = os.listdir(dirpath)
            for i in dirpaths:  # 去除label.png图片，并存放起来
                if (i == 'label.png'):
                    scr = os.path.join(os.path.abspath(dirpath), i)
                    scr = Image.open(scr)  # .convert('LA')，如果加上就是转成灰度图，我们这里不需要使用灰度图
                    dst = os.path.join(os.path.abspath(dirpath), 'label.png')
                    scr.save(dst)
                    filepath = dst
                    mask = 'C:\\Users\\布鲁瓦丝甜甜文\\Desktop\\ttttt\\label2\\' + new_name + '.png'
                    shutil.copy(filepath, mask)  # 将所取图片复制到mask中去


if __name__ == '__main__':
    reName(path)
