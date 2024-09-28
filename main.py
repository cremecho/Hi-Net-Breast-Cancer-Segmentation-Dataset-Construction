# author: Tianxi Wen, Fengze Li
# Github: https://github.com/cremecho

import sys
from get_label import generates_labels_tif
from patched import generates_dataset
from normalization import nomalizing_imaging
from dataset_itegration import dataset_itergation

import os
from os.path import exists
from os.path import join
import argparse


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=str, default='./dataset',
                        help="root of dataset, including all slices and their labels")
    parser.add_argument("--save-path", type=str, default='./results',
                        help="path for saving convert results and intermediate imgs")
    parser.add_argument("--num-cpu", type=int, default=8,
                        help="number of cores, for deciding multi-threads amount")
    args = parser.parse_args()

    return args


def mk_dir(opt):
    save_path = opt.save_path
    if not exists(save_path):
        os.mkdir(save_path)
    if not exists(join(save_path, 'train')):
        os.mkdir(join(save_path, 'train'))
    if not exists(join(save_path, 'val')):
        os.mkdir(join(save_path, 'val'))
    if not exists(join(save_path, 'test')):
        os.mkdir(join(save_path, 'test'))

    if not exists(join(save_path, 'temp')):
        os.mkdir(join(save_path, 'temp'))
    if not exists(join(save_path, 'temp', 'label-tif')):
        os.mkdir(join(save_path, 'temp', 'label-tif'))
    if not exists(join(save_path, 'temp', 'patched')):
        os.mkdir(join(save_path, 'temp', 'patched'))
    if not exists(join(save_path, 'temp', 'normalized')):
        os.mkdir(join(save_path, 'temp', 'normalized'))

if __name__ == '__main__':
    opt = parse_opt()
    mk_dir(opt)
    generates_labels_tif(opt)
    generates_dataset(opt)
    nomalizing_imaging(opt)
    dataset_itergation(opt)