import os
import shutil
from tqdm import tqdm


class ImageNetDivider(object):
    def __init__(self, path, ratio, gene_txt=True):
        super().__init__()
        self.path = path
        self.ratio = ratio
        self.gene_txt = gene_txt
        self.classes = os.listdir(self.path)

    def writing_txt(self, workspace, filename, content):
        txt_file = os.path.join(workspace, filename)
        with open(txt_file, 'a+') as txt:
            for value in content:
                txt.write(value + '\n')
        txt.close()

    def data_dividing(self):
        if self.gene_txt is True:
            self.writing_txt(self.path, 'classes.txt', self.classes)

        train_dir = os.path.join(self.path, 'train')
        val_dir = os.path.join(self.path, 'val')
        if not os.path.exists(train_dir): os.mkdir(train_dir)
        if not os.path.exists(val_dir): os.mkdir(val_dir)

        bar = tqdm(enumerate(self.classes))
        for label, classname in bar:
            target_traindir = os.path.join(train_dir, classname)
            target_valdir = os.path.join(val_dir, classname)
            if not os.path.exists(target_traindir): os.mkdir(target_traindir)
            if not os.path.exists(target_valdir): os.mkdir(target_valdir)
            train_list = []
            val_list = []

            folder = os.path.join(self.path, classname)
            count = len(os.listdir(folder))
            for idx, file in enumerate(os.listdir(folder)):
                cur_dir = classname + '/' + str(file) + ' ' + str(label)

                if idx < int(self.ratio * count):
                    train_list.append(cur_dir)
                    shutil.move(os.path.join(folder, file), target_traindir)
                else:
                    val_list.append(cur_dir)
                    shutil.move(os.path.join(folder, file), target_valdir)

            shutil.rmtree(folder)

            if self.gene_txt is True:
                self.writing_txt(self.path, 'train.txt', train_list)
                self.writing_txt(self.path, 'val.txt', val_list)
        bar.close()


def main():
    imagenetdivider = ImageNetDivider('garbage_classification', ratio=0.8, gene_txt=True)
    imagenetdivider.data_dividing()


if __name__ == '__main__':
    main()
