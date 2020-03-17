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
if os.getcwd().split('/')[-1] == 'segmented_images':
    os.chdir('../')
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
if os.getcwd().split('/')[-1] != 'segmented_images':
    os.chdir('./segmented_images')

labels = []
for file in os.listdir('./segmented_images'):
    if file.endswith(".png"):
        labels.append(file.split('_')[0])
labels = list(set(labels))

with open('labels.txt', 'w') as f:
    for item in labels:
        f.write("%s\n" % item)

def convert_bg(file):
    img=Image.open(file).convert('RGBA')
    arr=np.array(np.asarray(img))
    r,g,b,a=np.rollaxis(arr,axis=-1)
    mask=((r==255)&(g==255)&(b==255))
    arr[mask,3]=0
    img=Image.fromarray(arr,mode='RGBA')
    img.save('./'+file)
for file in glob.glob("*.png"):
    convert_bg(file)
os.getcwd()
imgs = []
for img in glob.glob('*.png'):
    temp = img.split('_')[0]
    imgs.append(img)

def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff,2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
for img in imgs:
    temp = img
    bg = Image.open(img) 
    new_im = trim(bg)
    new_im.save(temp)

images = [Image.open(x) for x in imgs]
widths, heights = zip(*(i.size for i in images))
total_width = sum(widths) + (len(imgs)*20)
max_height = max(heights)+80
new_im = Image.new('RGB', (total_width, max_height))
x_offset = 20
for i,im in enumerate(images):
    y_offset = max_height//2 - heights[i]//2
    new_im.paste(im, (x_offset,y_offset),im)
    x_offset += im.size[0]+20
new_im.save('./merged_black.png')
img=Image.open('./merged_black.png').convert('RGBA')
arr=np.array(np.asarray(img))
r,g,b,a=np.rollaxis(arr,axis=-1)
mask=((r==0)&(g==0)&(b==0))
arr[mask,3]=0
img=Image.fromarray(arr,mode='RGBA')
img.save('./merged_transparent.png')

img = Image.open("merged_transparent.png")
background = Image.open("background.jpeg")
size = img.size
background = background.resize(size,Image.ANTIALIAS)
background.paste(img, (0, 0), img)
background.save('merged_gradient.png',"PNG")

def process_img(img_src, title):
    img = Image.open(img_src, 'r')
    draw = ImageDraw.Draw(img)
    w, h = img.size
    font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", 50)
    text_w, text_h = w//2, h-h//10
    draw.text((text_w, text_h), title, (255,255,255),font=font)
    img_dest = img.save('final.png')
    return img_dest
process_img('merged_gradient.png','Flat 20% OFF!!')
print('Success!')
