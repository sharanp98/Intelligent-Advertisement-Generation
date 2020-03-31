from PIL import Image
import os

fi = open("labels.txt","w")

inpath = '../api/uploads'
outpath = '../api/output/'

f = []

for entry in os.listdir(inpath):
    if entry.endswith(".jpg"):
        for entry in os.listdir(outpath):
            if entry.endswith(".jpg"):
                f.append(entry)
                fi.write(entry)
                fi.write("  ")



print(f)
fi.close()



