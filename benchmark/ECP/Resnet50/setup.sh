#!/bin/bash


kaggle datasets download -d deeptrial/miniimagenet
unzip miniimagenet.zip
wget -O ./ImageNet-Mini/synset_labels.txt \
https://raw.githubusercontent.com/tensorflow/models/master/research/slim/datasets/imagenet_2012_validation_synset_labels.txt
mv ./ImageNet-Mini/images ./ImageNet-Mini/train

python3 imagenet_to_gcs.py \
--raw_data_dir=./ImageNet-Mini/ \
--local_scratch_dir=./tf_records \
--nogcs_upload

# sudo mv ./tf_records/validation/* ./tf_records/train/
