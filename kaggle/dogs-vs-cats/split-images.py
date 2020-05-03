import os
import shutil
from os.path import isfile, join

os.chdir('dataset/train')

os.mkdir('cat')
os.mkdir('dog')

files = [f for f in os.listdir() if isfile(join(f))]

for file in files:
    if file[0:3] == 'cat':
        shutil.move(file, 'cat')
    else:
        shutil.move(file, 'dog')
