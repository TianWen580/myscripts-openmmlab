import os, sys
import glob
from PIL import Image
import argparse


def txtLabel_to_xmlLabel(classes_file, source_img_path, save_xml_path):
    if not os.path.exists(save_xml_path):
        os.makedirs(save_xml_path)
    classes = open(classes_file).read().splitlines()
    print(classes)

    img_name = os.listdir(source_img_path)
    img_file = Image.open(os.path.join(source_img_path, img_name[0]))
    xml_file = open(os.path.join(save_xml_path, img_name[0][:-3] + 'xml'), "w")
    width, height = img_file.size
    xml_file.write('<annotation>\n')
    xml_file.write('\t<folder>simple</folder>\n')
    xml_file.write('\t<filename>' + "out.xml" + '</filename>\n')
    xml_file.write('\t<size>\n')
    xml_file.write('\t\t<width>' + str(width) + ' </width>\n')
    xml_file.write('\t\t<height>' + str(height) + '</height>\n')
    xml_file.write('\t\t<depth>' + str(3) + '</depth>\n')
    xml_file.write('\t</size>\n')

    obj_num = int(input('多少个目标:'))
    for i in range(obj_num):
        x_min = float(input("x_min:"))
        y_min = float(input("y_min:"))
        w = float(input("w:"))
        h = float(input("h:"))
        xmax = int(x_min * width + width * w)
        xmin = int(x_min * width)
        ymax = int(y_min * height + height * h)
        ymin = int(y_min * height)

        xml_file.write('\t<object>\n')
        xml_file.write('\t\t<name>' + str(classes[0]) + '</name>\n')
        xml_file.write('\t\t<name>' + str(classes[0]) + '</name>\n')
        xml_file.write('\t\t<pose>Unspecified</pose>\n')
        xml_file.write('\t\t<truncated>0</truncated>\n')
        xml_file.write('\t\t<difficult>0</difficult>\n')
        xml_file.write('\t\t<bndbox>\n')
        xml_file.write('\t\t\t<xmin>' + str(xmin) + '</xmin>\n')
        xml_file.write('\t\t\t<ymin>' + str(ymin) + '</ymin>\n')
        xml_file.write('\t\t\t<xmax>' + str(xmax) + '</xmax>\n')
        xml_file.write('\t\t\t<ymax>' + str(ymax) + '</ymax>\n')
        xml_file.write('\t\t</bndbox>\n')
        xml_file.write('\t</object>\n')
    xml_file.write('</annotation>')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--classes_file', type=str, default="data/classes.names")
    parser.add_argument('--source_img_path', type=str,
                        default="data/temp_img")
    parser.add_argument('--save_xml_path', type=str,
                        default="data/temp_xml")
    opt = parser.parse_args()

    txtLabel_to_xmlLabel(opt.classes_file, opt.source_img_path, opt.save_xml_path)
