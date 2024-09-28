# step1: put all WSIs and their annotations in one folder
# this step will generates their labels in tif format
# p.s. if the WSI you want to convert does not belongs to Camelyon16,17 or ICIAR2018
# you need to rewrite the label_map in convert2label_thread manually

import glob
import multiprocessing
import os
import get_label_thread


def find_matching_files(path):
    '''
    find all slices that contains both data and annotation
    '''

    file_dict = {}

    for file in os.listdir(path):
        file_name, file_ext = os.path.splitext(file)
        if file_name in file_dict:
            file_dict[file_name].append(file_ext.lower())
        else:
            file_dict[file_name] = [file_ext.lower()]

    matched_files_tif = [os.path.join(path, file_name + '.tif')
                        for file_name, exts in file_dict.items()
                        if '.xml' in exts and '.tif' in exts]
    matched_files_svs = [os.path.join(path, file_name + '.svs')
                        for file_name, exts in file_dict.items()
                        if '.xml' in exts and '.svs' in exts]
    matched_files = matched_files_tif + matched_files_svs

    return matched_files


def generates_labels_tif(opt):
    path = opt.root
    cpu_num = opt.num_cpu
    save_path = opt.save_path

    matched_files = find_matching_files(path)
    img_paths = matched_files
    xml_paths = [filename[:-4]+'.xml' for filename in img_paths]

    pool = multiprocessing.Pool(processes=cpu_num)
    mp_list = [[] for _ in range(cpu_num)]
    for j in range(len(img_paths)):
        mod = j % cpu_num
        mp_list[mod].append((img_paths[j], xml_paths[j]))

    for sub_ls in mp_list:
        if len(sub_ls) != 0 :
            pool.apply_async(get_label_thread.process_geration, (sub_ls, save_path,))

    print('pool close')
    pool.close()
    pool.join()
    print('----- all sub-process finished, label generating down -----')