from PIL import Image 
import shutil

data = open('api/reqd_backgrounds.txt').read().splitlines()
filename = "api/static/img/backgrounds/bg"+ str(data[0])+".jpg"
print(filename)

shutil.copy(filename,'segmented_images/background.jpg')

