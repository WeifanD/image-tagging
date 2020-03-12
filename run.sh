#!/bin/bash -x
#
# NAME: content-generation
THIS_DIR=$(DIRNAME=$(dirname "$0"); cd "$DIRNAME"; pwd)
THIS_FILE=$(basename "$0")
THIS_PATH="$THIS_DIR/$THIS_FILE"
echo "`date` Info: This file $THIS_FILE start running on $THIS_DIR..."

cd /home/admin/projects/image-tagging
source env/bin/activate
echo "`date` run main_text.py for text"
#python main_text.py

echo "`date` run main.py for img"
python main.py 

echo "`date` done"
