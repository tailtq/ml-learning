import os
import shutil
from os.path import isfile, join

os.chdir('dataset/train')

if not os.path.exists('cat'):
    os.mkdir('cat')
    
if not os.path.exists('dog'):
    os.mkdir('dog')

files = [f for f in os.listdir() if isfile(join(f))]

for file in files:
    if file[0:3] == 'cat':
        shutil.move(file, 'cat')
    else:
        shutil.move(file, 'dog')
