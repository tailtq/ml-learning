#!/bin/bash
git clone https://github.com/tailtq/tf_unet.git
cd tf_unet
pip install -r requirements.txt
python setup.py install --user
