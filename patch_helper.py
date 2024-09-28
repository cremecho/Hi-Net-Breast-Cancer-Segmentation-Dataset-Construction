import numpy as np
import math
from PIL import Image

def get_num_of_patches(slide, patch_size, dlevel = 2):
    w, h = slide.level_dimensions[dlevel]
    num_w = math.ceil(w / patch_size)
    res_w = w - (num_w - 1) * patch_size
    num_h = math.ceil(h / patch_size)
    res_h = h - (num_h - 1) * patch_size
    return dlevel, num_w, num_h, res_w, res_h

# get a patch with window padding
def get_patch_image_expand(slide, pw, ph, num_w, num_h, res_w, res_h, dlevel, args):
    startX = int((pw - 0.5) * args.patch_size)
    startY = int((ph - 0.5) * args.patch_size)
    window_size_w = window_size_h = 2 * args.patch_size
    padding_w_l = padding_w_r = padding_h_t = padding_h_b = 0

    if pw == 0:  # left-end, window padding
        startX = 0
        padding_w_l = int(0.5 * args.patch_size)
        window_size_w = int(1.5 * args.patch_size)
    if ph == 0: # top
        startY = 0
        padding_h_t = int(0.5 * args.patch_size)
        window_size_h = int(1.5 * args.patch_size)
    if pw == num_w - 2:  # right-end, slide padding + window padding
        if res_w < 0.5 * args.patch_size:
            window_size_w = int(1.5 * args.patch_size + res_w)
            padding_w_r = int(0.5 * args.patch_size - res_w)
    elif pw == num_w - 1:
        window_size_w = int(0.5 * args.patch_size + res_w)
        padding_w_r = int(1.5 * args.patch_size - res_w)
    if ph == num_h - 2: # bottom
        if res_h < 0.5 * args.patch_size:
            window_size_h = int(1.5 * args.patch_size + res_h)
            padding_h_b = int(0.5 * args.patch_size - res_h)
    elif ph == num_h - 1:
        window_size_h = int(0.5 * args.patch_size + res_h)
        padding_h_b = int(1.5 * args.patch_size - res_h)
    patch = slide.getUCharPatch(startX, startY, window_size_w, window_size_h, dlevel)
    patch = np.pad(patch, ((padding_h_t, padding_h_b), (padding_w_l, padding_w_r), (0, 0)), 'constant', constant_values=(0, 0))
    return patch


# get a normal patch
def get_patch_image(slide, pw, ph, num_w, num_h, res_w, res_h, dlevel, type, patch_size):
    startX = int(pw * patch_size)
    startY = int(ph * patch_size)
    window_size_w = window_size_h = patch_size
    padding_w_r = padding_h_b = 0

    if pw == num_w - 1:
        window_size_w = int(res_w)
        padding_w_r = int(patch_size - res_w)
    if ph == num_h - 1:
        window_size_h = int(res_h)
        padding_h_b = int(patch_size - res_h)
    patch = slide.read_region(
        (int(startX * slide.level_downsamples[dlevel]), int(startY * slide.level_downsamples[dlevel])),
        dlevel, (window_size_w, window_size_h))
    if type=='slide':
        patch = patch.convert('RGB')
        patch = np.pad(patch, ((0, padding_h_b), (0, padding_w_r), (0, 0)), 'constant', constant_values=(0, 0))
    else:
        patch = patch.convert('L')
        patch = np.pad(patch, ((0, padding_h_b), (0, padding_w_r)), 'constant', constant_values=(0, 0))
    return patch


def _not_empty_test(tensor, value):
    shape = tensor.shape
    length = len(shape)
    if length == 2:
        a, b = tensor.shape
        for aa in range(a):
            for bb in range(b):
                element = tensor[aa][bb]
                if not element == value:
                    print('not empty: %f' % element)
    if length == 3:
        a, b, c = tensor.shape
        for aa in range(a):
            for bb in range(b):
                for cc in range(c):
                    element = tensor[aa][bb][cc]
                    if not element == value:
                        print('not empty: %f' % element)
    if length == 4:
        a, b, c, d = tensor.shape
        for aa in range(a):
            for bb in range(b):
                for cc in range(c):
                    for dd in range(d):
                        element = tensor[aa][bb][cc][dd]
                        if not element == value:
                            print('not empty: %f' % element)

