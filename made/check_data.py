import os


def check_data(imgs_path, labels_path):
    imgs_list = os.listdir(imgs_path)
    labels_list = os.listdir(labels_path)

    no_labels = []
    no_images = []

    for img_name in imgs_list:
        if img_name[:-4] + '.xml' not in labels_list:
            no_labels.append(img_name)
    for label_name in labels_list:
        if label_name[:-4] + '.JPG' not in imgs_list:
            no_images.append(label_name)

    print(no_labels)
    print(no_images)
    print(len(no_images))
    print(len(no_labels))


if __name__ == '__main__':
    imgs_path = 'data/JPEGImages'
    labels_path = 'data/VOCAnnotations'
    check_data(imgs_path, labels_path)
