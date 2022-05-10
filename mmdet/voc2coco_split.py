# -*- coding=utf-8 -*-
# !/usr/bin/python

import sys
import os
import shutil
import numpy as np
import json
import xml.etree.ElementTree as ET

# 检测框的ID起始值
START_BOUNDING_BOX_ID = 1
# 类别列表无必要预先创建，程序中会根据所有图像中包含的ID来创建并更新
PRE_DEFINE_CATEGORIES = {"living": 0}


# If necessary, pre-define category and its id
#  PRE_DEFINE_CATEGORIES = {"aeroplane": 1, "bicycle": 2, "bird": 3, "boat": 4,
#  "bottle":5, "bus": 6, "car": 7, "cat": 8, "chair": 9,
#  "cow": 10, "diningtable": 11, "dog": 12, "horse": 13,
#  "motorbike": 14, "person": 15, "pottedplant": 16,
#  "sheep": 17, "sofa": 18, "train": 19, "tvmonitor": 20}


def get(root, name):
    vars = root.findall(name)
    return vars


def get_and_check(root, name, length):
    vars = root.findall(name)
    if len(vars) == 0:
        raise NotImplementedError('Can not find %s in %s.' % (name, root.tag))
    if length > 0 and len(vars) != length:
        raise NotImplementedError('The size of %s is supposed to be %d, but is %d.' % (name, length, len(vars)))
    if length == 1:
        vars = vars[0]
    return vars


def convert(xml_list, xml_dir, json_file):
    '''
    :param xml_list: 需要转换的XML文件列表
    :param xml_dir: XML的存储文件夹
    :param json_file: 导出json文件的路径
    :return: None
    '''
    list_fp = xml_list
    image_id = 1
    # 标注基本结构
    json_dict = {"images": [],
                 "type": "instances",
                 "annotations": [],
                 "categories": []}
    categories = PRE_DEFINE_CATEGORIES
    bnd_id = START_BOUNDING_BOX_ID
    for line in list_fp:
        line = line.strip()
        print(" Processing {}".format(line))
        # 解析XML
        xml_f = os.path.join(xml_dir, line)
        tree = ET.parse(xml_f)
        root = tree.getroot()
        filename = root.find('filename').text
        if '/' in filename:
            filename = filename.split('/')[1] # 实例：张三/haoisdhsaubdjasodias.jpg => haoisdhsaubdjasodias.jpg
        # 取出图片名字
        image_id += 1
        size = get_and_check(root, 'size', 1)
        # 图片的基本信息
        width = int(get_and_check(size, 'width', 1).text)
        height = int(get_and_check(size, 'height', 1).text)
        image = {'file_name': filename,
                 'height': height,
                 'width': width,
                 'id': image_id}
        json_dict['images'].append(image)
        # 处理每个标注的检测框
        for obj in get(root, 'object'):
            # 取出检测框类别名称
            category = get_and_check(obj, 'name', 1).text
            # 更新类别ID字典
            if category not in categories:
                new_id = len(categories)
                categories[category] = new_id
            category_id = categories[category]
            bndbox = get_and_check(obj, 'bndbox', 1)
            xmin = get_and_check(bndbox, 'xmin', 1).text
            ymin = get_and_check(bndbox, 'ymin', 1).text
            xmax = get_and_check(bndbox, 'xmax', 1).text
            ymax = get_and_check(bndbox, 'ymax', 1).text
            if xmin == 0 and ymin == 0 and xmax == 0 and ymax == 0:
                continue
            else:
                xmin = round(float(xmin)) - 1
                ymin = round(float(ymin)) - 1
                xmax = round(float(xmax))
                ymax = round(float(ymax))
            assert (xmax > xmin)
            assert (ymax > ymin)
            o_width = abs(xmax - xmin)
            o_height = abs(ymax - ymin)
            annotation = dict()
            annotation['area'] = o_width * o_height
            annotation['iscrowd'] = 0
            annotation['image_id'] = image_id
            annotation['bbox'] = [xmin, ymin, o_width, o_height]
            annotation['category_id'] = category_id
            annotation['id'] = bnd_id
            annotation['ignore'] = 0
            # 设置分割数据，点的顺序为逆时针方向
            annotation['segmentation'] = [[xmin, ymin, xmin, ymax, xmax, ymax, xmax, ymin]]

            json_dict['annotations'].append(annotation)
            bnd_id = bnd_id + 1

    # 写入类别ID字典
    for cate, cid in categories.items():
        cat = {'supercategory': 'none', 'id': cid, 'name': cate}
        json_dict['categories'].append(cat)
    # 导出到json
    # mmcv.dump(json_dict, json_file)
    print(type(json_dict))
    json_data = json.dumps(json_dict)
    with  open(json_file, 'w') as w:
        w.write(json_data)


if __name__ == '__main__':
    root_path = 'data'

    if not os.path.exists(os.path.join(root_path, 'coco/annotations')):
        os.makedirs(os.path.join(root_path, 'coco/annotations'))
    if not os.path.exists(os.path.join(root_path, 'coco/train2017')):
        os.makedirs(os.path.join(root_path, 'coco/train2017'))
    if not os.path.exists(os.path.join(root_path, 'coco/val2017')):
        os.makedirs(os.path.join(root_path, 'coco/val2017'))
    xml_dir = os.path.join(root_path, 'VOCAnnotations')  # 已知的VOC2012的标注

    xml_labels = os.listdir(xml_dir)
    np.random.shuffle(xml_labels)
    split_point = int(len(xml_labels) / 20)

    # validation data
    xml_list = xml_labels[0:split_point]
    json_file = os.path.join(root_path, 'coco/annotations/detections_val2017.json')
    convert(xml_list, xml_dir, json_file)
    for xml_file in xml_list:
        img_name = xml_file[:-4] + '.jpg'
        shutil.copy(os.path.join(root_path, 'JPEGImages', img_name),
                    os.path.join(root_path, 'coco/val2017', img_name))
    # train data
    xml_list = xml_labels[split_point:]
    json_file = os.path.join(root_path, 'coco/annotations/detections_train2017.json')
    convert(xml_list, xml_dir, json_file)
    for xml_file in xml_list:
        img_name = xml_file[:-4] + '.jpg'
        shutil.copy(os.path.join(root_path, 'JPEGImages', img_name),
                    os.path.join(root_path, 'coco/train2017', img_name))
