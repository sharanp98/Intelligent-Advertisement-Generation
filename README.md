# Intelligent Advertisement generation for e-commerce websites.

Technology used : Image segmentation model built on top of Tensorflow Keras : [Mask RCNN](https://github.com/matterport/Mask_RCNN) and Python Image Processing. A website was built to demo the code using Python Flask.

## Create a virtual environment with the dependencies :
$ conda create --name <env> --file requirements.txt
  
There are other system dependent tools that need to be installed globally. That is beyond the scope of this README but active Googling will solve these extra dependencies.

## Run the website
$ cd samples/api
$ python3 api.py

## Use the code
The code is divided into two parts : pt1.py and pt2.py

- pt1.py (part 1) is the neural network part as all the images detected are extracted and saved in the *segmented_images* directory.

- pt2.py (part 2) is the image processing part. The segmented images are trimmed off their backgrounds, combined and added a common background. (Additional features include a custom text, adding stickers etc).

These files should be run in sequence as :
python3 pt1.py
python3 pt2.py

## Sample input and output

