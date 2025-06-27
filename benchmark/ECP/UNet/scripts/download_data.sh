#!/bin/bash

USERNAME="zhongzheng0522"
APIKEY="0674d6f705e296db9c502b41e9dfce8e"

mkdir -p ~/.kaggle
echo "{\"username\":\"$USERNAME\",\"key\":\"$APIKEY\"}" > ~/.kaggle/kaggle.json
chmod 600 ~/.kaggle/kaggle.json

pip install kaggle --upgrade
export PATH=$PATH:/home/cc/.local/bin

kaggle competitions download -c carvana-image-masking-challenge -f train_hq.zip
unzip train_hq.zip
mkdir data
cd data
mkdir imgs
mkdir masks
cd ..
mv train_hq/* data/imgs/
rm -d train_hq
rm train_hq.zip

kaggle competitions download -c carvana-image-masking-challenge -f train_masks.zip
unzip train_masks.zip

mv train_masks/* data/masks/
rm -d train_masks
rm train_masks.zip
