import os
from PIL import Image, ImageChops,ImageDraw,ImageFont
import numpy as np
import glob 

with open(os.getcwd()+'/reqd_images.txt', 'r') as f:
    reqd = f.read().splitlines()
offer = reqd[-1]

for file in os.listdir('./segmented_images'):
    if file.endswith(".png"):
        if file.split('_')[0] not in reqd:
            os.remove('./segmented_images/'+file)

os.chdir('./segmented_images')
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
background = Image.open("background.jpg")
size = img.size
background = background.resize(size,Image.ANTIALIAS)
background.paste(img, (0, 0), img)
background.save('merged_gradient.png',"PNG")

def process_img(txt):
    image = Image.open('merged_gradient.png')
    draw = ImageDraw.Draw(image)
    w, h = image.size
    fontsize = 1  # starting font size

    # portion of image width you want text width to be
    img_fraction = 0.50
    font_path = "/usr/share/fonts/truetype/freefont/AmaticSC-Regular.ttf"
    font = ImageFont.truetype(font_path, fontsize)
    while font.getsize(txt)[0] < img_fraction*image.size[0]:
        # iterate until the text size is just larger than the criteria
        fontsize += 1
        font = ImageFont.truetype(font_path, fontsize)

    # optionally de-increment to be sure it is less than criteria
    fontsize -= 1
    font = ImageFont.truetype(font_path, fontsize)
    # text_w, text_h = w//2, h-h//20

    print ('final font size',fontsize)
    draw.text((10,25), txt, font=font) # put the text on the image
    image.save('final.png') # save it
process_img(offer)
print('Success!')
