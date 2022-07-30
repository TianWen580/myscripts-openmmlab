# Copyright (c) OpenMMLab. All rights reserved.
from argparse import ArgumentParser
import os
import cv2
from mmcls.apis import inference_model, init_model


def show_result_pyplot(model, img, result):
    if hasattr(model, 'module'):
        model = model.module
    img = model.show_result(img, result, show=False)
    return img


def main():
    # config文件
    config_file = 'configs/xxx/xxx.py'
    # 训练好的模型
    checkpoint_file = '~/xxx.pth'

    # model = init_detector(config_file, checkpoint_file)
    model = init_model(config_file, checkpoint_file, device='cuda:0')

    # 图片路径
    img_dir = r'~\data\classxxx'

    classes = os.listdir(r'~\data')
    classes.sort()

    test_list = os.listdir(img_dir)

    i = 0
    for test in test_list:
        test_list[i] = os.path.join(img_dir, test)
        i += 1

    count = 0
    for name in test_list:
        count += 1
        # print('model is processing the {}/{} images.'.format(count, len(test_list)))
        result = inference_model(model, name)
        # img = show_result_pyplot(model, name, result)
        pred_label = result['pred_label']
        pred_class = classes[pred_label]
        pred_score = result['pred_score']
        test = name.split('\\')[-1]
        save_name = test[:6] + '_' + str(pred_class) + '_' + str(pred_score) + test[-4:]
        save_to = os.path.join(os.path.dirname(name), save_name)
        os.rename(name, save_to)


if __name__ == '__main__':
    main()
