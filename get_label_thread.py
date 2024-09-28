# Because of the nature of python3.8,
# multi-processing execution function must be written in another file

# Since the ICIAR2018 dataset annotation's area is too large
# We manually label the tumors with a more accurate boundary
# We rename the original boundary as metastases_org, and the new boundary as newmeta

import os
import multiresolutionimageinterface as mir
import shutil

def process_geration(ls, save_path):
    reader = mir.MultiResolutionImageReader()
    for pair in ls:
        img_paths, xml_paths = pair
        file_name = os.path.split(img_paths)[1]
        img = reader.open(img_paths)
        annotation_list = mir.AnnotationList()
        xml_repository = mir.XmlRepository(annotation_list)
        xml_repository.setSource(xml_paths)
        xml_repository.load()
        annotation_mask = mir.AnnotationToMask()
        # metastases: c17; _0,_1,Tumor: c16; newmeta: iciar18(manually)
        label_map = {'metastases': 1, '_0': 1, '_1': 1, 'Tumor': 1, 'newmeta': 1}
        output = os.path.join(save_path, 'temp' ,'label-tif', file_name[:-4] + '_labels.tif')
        annotation_mask.convert(annotation_list, output,
                                img.getDimensions(),
                                img.getSpacing(), label_map)
        shutil.move(output, os.path.join(save_path, 'temp', 'label-tif', output))
