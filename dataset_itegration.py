# Step4: rename, shuffle and split the datset

import glob
import os
import random
import shutil
from natsort import natsorted
import re

def sort_file_paths(file_paths):
    def sort_key(path):
        match = re.search(r'c(\d+)_(\d+)', path)
        if match:
            return int(match.group(1)), int(match.group(2))
        return path

    return sorted(file_paths, key=sort_key)

def dataset_itergation(opt):
    path = opt.root
    save_path = opt.save_path

    img_paths = glob.glob(os.path.join(save_path, 'temp', 'normalized', '*.png'))
    lbl_paths = glob.glob(os.path.join(save_path, 'temp', 'patched', "*label.png"))
    img_paths = sort_file_paths(img_paths)
    lbl_paths = sort_file_paths(lbl_paths)

    for img_src, lbl_src in zip(img_paths, lbl_paths):
        rng = random.random()
        mode = ''
        if rng < 0.1:
            mode = 'val'
        elif rng >=0.1 and rng < 0.2:
            mode = 'test'
        else:
            mode = 'train'
        shutil.copy(img_src, os.path.join(save_path, mode))
        shutil.copy(lbl_src, os.path.join(save_path, mode))

        img_name = os.path.split(img_src)[-1]
        index = 0
        while os.path.exists(os.path.join(save_path, mode, img_name.split('_')[0] + '_%s_%d' % (mode, index) + '.png')):
            index += 1
        img_rename = img_name.split('_')[0] + '_%s_%d' % (mode, index) + '.png'
        lbl_name = os.path.split(lbl_src)[-1]
        lbl_rename = lbl_name.split('_')[0] + '_%s_%d' % (mode, index) + '_label.png'
        os.rename(os.path.join(save_path, mode, img_name), os.path.join(save_path, mode, img_rename))
        os.rename(os.path.join(save_path, mode, lbl_name), os.path.join(save_path, mode, lbl_rename))
    print('----- dataset split finished, all down -----')