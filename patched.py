# Step2: get the patched images
# You need to first download openslide-win64-20171122 from release
# and fill the OPENSLIDE_PATH with path of bin folder

OPENSLIDE_PATH = r''

from get_label import find_matching_files
import glob
from tqdm import tqdm, trange
import numpy as np
import patch_helper
from PIL import Image
import os

if hasattr(os, 'add_dll_directory'):
    # Python >= 3.8 on Windows
    with os.add_dll_directory(OPENSLIDE_PATH):
        import openslide
else:
    import openslide


def generates_dataset(opt):
    # generates usable dataset from WSI and their labels in [path]
    path = opt.root
    save_path = opt.save_path

    images = find_matching_files(path)
    anns = glob.glob(os.path.join(save_path, 'temp', 'label-tif', '*.tif'))
    save_path = os.path.join(save_path, 'temp', 'patched')

    patch_size = 512
    for img_path, lbl_path in tqdm(zip(images, anns)):
        img = openslide.open_slide(img_path)
        lbl = openslide.open_slide(lbl_path)
        dlevel, num_w, num_h, res_w, res_h = patch_helper.get_num_of_patches(img, patch_size, 2)
        for pw in trange(num_w):
            for ph in range(num_h):
                image = patch_helper.get_patch_image(img, pw, ph, num_w, num_h, res_w, res_h, dlevel, 'slide', patch_size)
                target = patch_helper.get_patch_image(lbl, pw, ph, num_w, num_h, res_w, res_h, dlevel, 'label', patch_size)
                if np.max(target) == 0 or np.min(target) == 1:
                    continue
                mean = np.mean(target)
                if mean < 0.05 or mean > 0.995:
                    continue
                image = np.array(image).astype(np.float32)

                index = 0
                dataset = ''
                if 'svs' in img_path.lower():
                    dataset = 'iciar18'
                elif 'patient' in img_path.lower():
                    dataset = 'c17'
                else:
                    dataset = 'c16'
                while os.path.exists(os.path.join(save_path, '%s_%d.png' % (dataset, index))):
                    index += 1
                f_name_img = os.path.join(save_path, '%s_%d.png' % (dataset, index))
                f_name_lbl = os.path.join(save_path, '%s_%d_label.png' % (dataset, index))
                try:
                    Image.fromarray(np.uint8(image)).save(f_name_img)
                    # Image.fromarray(target).save(f_name_lbl)   # 0/1 label

                    target *= 255
                    # f_name_lbl = os.path.join(save_path, 'check','%d_label.png' % index)
                    Image.fromarray(np.uint8(target)).save(f_name_lbl)
                except:
                    pass
    print("----- image patching finished -----")