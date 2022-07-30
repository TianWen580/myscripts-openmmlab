from PIL import Image
from tqdm import tqdm

imageDir = '~/picture.jpg'
saveDir = '~/save_dir/'
targetWid = 5472
targetHei = 3648
format = '.jpg'

Image.MAX_IMAGE_PIXELS = None

rowIndex = []
colIndex = []
image = Image.open(imageDir)
for i in range(0, image.width, targetWid):
    colIndex.append(i)
for i in range(0, image.height, targetHei):
    rowIndex.append(i)

iterName = 0
print('请等候，图片正在裁剪中...')
tbar = tqdm(rowIndex)
for row in tbar:
    for col in colIndex:
        roi = image.crop([col, row, col + targetWid, row + targetHei])  # 切剪图片
        roi.save(saveDir + str(iterName) + format)  # 保存图片
        iterName += 1




