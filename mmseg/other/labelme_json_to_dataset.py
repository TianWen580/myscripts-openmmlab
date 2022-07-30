#-*- coding : utf-8 -*-
# coding: utf-8
"""
json数据转成可用json文件所需环境配置：
1、在dos命令窗口输入：pip install pyqt5
2、在dos命令窗口输入：pip install pyside2
3、在dos命令窗口输入：pip install labelme
4、在dos命令窗口输入：labelme
"""
import os
from tqdm import tqdm

path = '~/json_label_folder/'
# path是你存放json的路径
json_file = os.listdir(path)
for file in tqdm(json_file):
    os.system("python "~\\Anaconda3\\Scripts\\labelme_json_to_dataset.exe %s" % (path + file))  # 遍历所有画好json文件，转换json文件

