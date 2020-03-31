import os
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   
os.environ["CUDA_VISIBLE_DEVICES"] = ""

import tensorflow as tf
import sys
import random
import math
import skimage.io
import matplotlib
import matplotlib.pyplot as plt
import warnings
import glob
import cv2
from PIL import Image, ImageChops,ImageDraw,ImageFont
import numpy as np


os.chdir('/home/sharan/Desktop/Personal Projects/Mask_RCNN/samples/')
print(os.getcwd())
ROOT_DIR = os.path.abspath("../")
print(ROOT_DIR)
warnings.filterwarnings("ignore")
sys.path.append(ROOT_DIR)  
from mrcnn import utils
import mrcnn.model as modellib
from mrcnn import visualize
sys.path.append(os.path.join(ROOT_DIR, "samples/coco/"))  
# import coco
from samples.coco import coco
os.getcwd()
MODEL_DIR = os.path.join(ROOT_DIR, "logs")
COCO_MODEL_PATH = os.path.join('', "mask_rcnn_coco.h5")
if not os.path.exists(COCO_MODEL_PATH):
    utils.download_trained_weights(COCO_MODEL_PATH)
IMAGE_DIR = os.path.join(ROOT_DIR, "images")
class InferenceConfig(coco.CocoConfig):
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
config = InferenceConfig()
model = modellib.MaskRCNN(mode="inference", model_dir='mask_rcnn_coco.hy', config=config)
model.load_weights('mask_rcnn_coco.h5', by_name=True)
class_names = ['BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane',
               'bus', 'train', 'truck', 'boat', 'traffic light',
               'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird',
               'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear',
               'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie',
               'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
               'kite', 'baseball bat', 'baseball glove', 'skateboard',
               'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
               'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
               'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
               'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed',
               'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote',
               'keyboard', 'cell phone', 'microwave', 'oven', 'toaster',
               'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
               'teddy bear', 'hair drier', 'toothbrush']
image = skimage.io.imread('sample.jpg')
results = model.detect([image], verbose=1)
r = results[0]
visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'], class_names, r['scores'])
mask = r['masks']
cls = list(r['class_ids'])
mask = mask.astype(int)
mask.shape
k=0
for i in range(mask.shape[2]):
    temp = skimage.io.imread('sample.jpg')
    for j in range(temp.shape[2]):
        temp[:,:,j] = temp[:,:,j] * mask[:,:,i]
    img_name = 'segmented_images/'+class_names[cls[i]]+'_'+str(k)+'.png'
    k+=1
    old_val = 0
    new_val = 255
    temp[temp==old_val]=new_val
    plt.figure(figsize=(8,8))
    plt.imshow(temp)
    plt.imsave(img_name,temp)

labels = []
for file in os.listdir('./segmented_images'):
    if file.endswith(".png"):
        labels.append(file.split('_')[0])
labels = list(set(labels))
print("Labels written to the file:\n",labels)

with open('labels.txt', 'w') as f:
    for item in labels:
        f.write("%s\n" % item)

print(os.getcwd())  