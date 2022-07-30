import os
from cv2 import cv2
form tqdm import tqdm
import numpy as np
from PIL import Image
from mmseg.apis import inference_segmentor, init_segmentor, show_result_pyplot
from mmseg.core.evaluation import get_palette

test_dir = ''
windowSize = 512 # 预测滑窗大小

config_dir = 'configs/xxx/xxx.py'
checkpoint_dir = '~/xxx.pth'
device = 'cuda:0'


def sliding_pred(img_dir, crop_size=256):
          img = cv2.imread(img_dir, flags=-1)
    h, w = img.shape[:2]
    num_h = h // crop_size
    num_w = w // crop_size
    img = np.array(img)
    img_crop = np.zeros((crop_size, crop_size, 3))

    model = init_segmentor(config_dir, checkpoint_dir, device=device)

    rows = []
    pred_png = np.zeros((0, 0), np.uint8)
    for h in range(num_h+1):
        pred_result0 = []
        a_row = None
        for w in range(num_w+1):
            img_crop = img[h * crop_size:(h + 1) * crop_size, w * crop_size:(w + 1) * crop_size]
            result = inference_segmentor(model, img_crop)
            pred_result0.append(result[0])  # 横向拼接

            if w >= num_w:  # 横向拼接到头，换行
                a_row = np.concatenate(pred_result0, axis=1)
                pred_result0 = []
            pass
        rows.append(a_row)
        pass
    pred_png = np.concatenate(rows, axis=0)
    pred_png = pred_png[:3821,:3752]

    a_list = [pred_png]
    
    # 在线展示
    show_result_pyplot(
        model,
        img,
        a_list)


if __name__ == "__main__":
    files = os.listdir(test_dir)

                for f in tqdm(files):
                    sliding_pred(os.path.join(test_dir, f), crop_size=windowSize)
