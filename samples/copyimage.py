import shutil
import os

print('Shutil:'+os.getcwd())
try:
    shutil.copy('./segmented_images/final.png','./api/static')
    print('Copied Final successfully')
except OSError as err:
    print ("Shutil Error:"+err)