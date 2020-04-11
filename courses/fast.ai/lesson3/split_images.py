import numpy as np
import shutil
import os

from pathlib import Path

path = Path('../../../../datasets/camvid')
label_path = path / 'codes.txt'
valid_path = path / 'valid.txt'

(path/'train/images').mkdir(parents=True, exist_ok=True)
(path/'train/labels').mkdir(parents=True, exist_ok=True)

(path/'test/images').mkdir(parents=True, exist_ok=True)
(path/'test/labels').mkdir(parents=True, exist_ok=True)

validation_filenames = np.loadtxt(valid_path, dtype=str)

get_y_fn = lambda x: path/'labels/{0}_P{1}'.format(x.stem, x.suffix)

for filename in validation_filenames:
    file_path = path/'images'/filename
    label_path = get_y_fn(file_path)
    
    shutil.copyfile(str(file_path), str(path/'test/images'/filename))
    shutil.copyfile(str(label_path), str(path/'test/labels'/(label_path.stem + label_path.suffix)))
    
training_filenames = os.listdir(str(path/'images'))
training_filenames = list(set(training_filenames) - set(validation_filenames))

for filename in training_filenames:
    file_path = path/'images'/filename
    label_path = get_y_fn(file_path)
    
    shutil.copyfile(str(file_path), str(path/'train/images'/filename))
    shutil.copyfile(str(label_path), str(path/'train/labels'/(label_path.stem + label_path.suffix)))
    