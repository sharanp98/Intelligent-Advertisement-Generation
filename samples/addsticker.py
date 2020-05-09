from PIL import Image 
import math
data = open('reqd_stickers.txt').read().splitlines()
filename = "api/static/img/offers/offer"+ str(data[0])+".png"

def calc_size(l,b):
    nx = ((l[0]-b[0])*100)/l[0]
    ny = ((l[1]-b[1])*100)/l[1]
    n = max(max(nx,0),max(ny,0))
    n = math.ceil(n)
    l[0] = int(l[0] - n*l[0]*0.01)
    l[1] = int(l[1] - n*l[1]*0.01)
    return l

# open the image 
main = Image.open("api/static/final.png")  
logo = Image.open(filename)  


width, height = logo.size
l=[]
l.append(width)
l.append(height)

width, height = main.size
b=[]
b.append(width)
b.append(height)

n = calc_size(l,b)
K = 0.5
n = list(map(lambda x : x * K, n)) 
n = list(map(lambda x : int(x),n)) 

lx = n[0]
ly = n[1]
logo = logo.resize((lx,ly))

transparent = Image.new('RGBA', (width, height), (0,0,0,0))
transparent.paste(main, (0,0))

if(data[1]=='01'):
    #Position logo at left top
    bx = int(0.1*lx)
    by = int(0.1*ly)

if(data[1]=='03'):
    #Position logo at right top
    bx = int(b[0]) - int(1.1*lx)
    by = int(0.1*ly)

if(data[1]=='05'):
    #Position logo at center
    bx = int(b[0]/2)-int((0.5*lx))
    by = int(b[1]/2)-int((0.5*ly))

if(data[1]=='07'):    
    #Position logo at left bottom
    bx = int(0.1*lx)
    by = int(b[1]) - int(1.1*ly)

    
if(data[1]=='09'):
    #Position logo at right bottom
    bx = int(b[0]) - int(1.1*lx) 
    by = int(b[1]) - int(1.1*ly)


 



position=(bx,by)

transparent.paste(logo, position, mask=logo)
transparent=transparent.convert("RGB")

transparent.save('api/static/final2.png')




# from PIL import Image 
  
# # open the image 
# main = Image.open("api/static/final.png") 
# logo = Image.open('api/static/img/offers/offer5.png')  

# logo = logo.resize((300,300))

# width, height = main.size
# transparent = Image.new('RGBA', (width, height), (0,0,0,0))
# transparent.paste(main, (0,0))

# position=(400,0)

# transparent.paste(logo, position, mask=logo)
# transparent=transparent.convert("RGB")

# transparent.save('api/static/final2.png')



