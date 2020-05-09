from flask import Flask, redirect, url_for,render_template, request, send_from_directory,send_file
import os
import json
import re
from werkzeug import secure_filename

app = Flask(__name__)


WORKING_FOLDER = os.path.dirname(os.getcwd()) #samples
UPLOAD_FOLDER =  WORKING_FOLDER
DOWNLOAD_FOLDER = os.path.join(WORKING_FOLDER,'api/static')                                 

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/no-need', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'sample.jpg'))
            print('Image Uploaded')
            return redirect('/final')
    return render_template("upload_image.html") 

@app.route('/final')
def hello_admin():

    print('In final')
    os.chdir(WORKING_FOLDER)
    #Delete previous output
    for file in os.listdir():
        if file in ['labels.txt','reqd_images.txt','reqd_stickers.txt']:
            os.remove(file)
   
    
    for file in os.listdir('segmented_images'):
        if file != 'background.jpeg':
            os.remove(os.path.join('segmented_images',file))
    os.system("python3 pt1.py")
    data = open('labels.txt').read().splitlines()
    return render_template("ListCategories.html",data=json.dumps(data))

@app.route('/reqjson',methods=['POST'])
def pass_val():
    name=request.form['canvas_data']
    print(name)
    os.chdir(WORKING_FOLDER)
    f = open("reqd_images.txt","w")
    x = re.findall(r'[\w\d%!_ ]+', name)
    for i in x:
        f.write(i)
        f.write("\n")                                                          
    f.close()
    os.system("python3 pt2.py")
    try:
        os.remove("api/static/final.png")  
    except:
        print("final.png does not exist")  
    os.system("python3 copyimage.py") 
    return redirect('/disp')

@app.route('/disp')
def disp():
    return render_template("displayimage.html")


@app.route('/download',methods=['GET', 'POST'])
def download():
    return send_from_directory(directory= DOWNLOAD_FOLDER, filename='final.png')

@app.route('/',methods=['GET', 'POST'])
def demo():
    
    os.chdir(DOWNLOAD_FOLDER)
    for file in os.listdir():
        if file in ['final.png']:
            os.remove(file)
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            #flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            #flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'sample.jpg'))
            print('Image Uploaded')
            return redirect('/background')
    return render_template("upload2.html") 

@app.route('/sticker',methods=['GET', 'POST'])
def sticker():
    return render_template('stickers.html')

@app.route('/demo',methods=['GET', 'POST'])
def demo1():
    return render_template('stickdemo.html')


@app.route('/reqSticker',methods=['POST'])
def reqSticker():
    name = request.form.get('canvas_data')
    print(name)
    f = open("reqd_stickers.txt","w")
    x = re.findall(r'[\d]+', name)
    for i in x:
        f.write(i)
        f.write("\n")                                                        
    f.close()
    os.chdir(WORKING_FOLDER)
    os.system("python3 addsticker.py") 


@app.route('/dispSticker')
def dispSticker():
    return render_template("displaysticker.html")

@app.route('/background',methods=['GET', 'POST'])
def backgrounds():
    return render_template('backgrounds.html')

@app.route('/reqBackground',methods=['POST'])
def reqBackground():
    name = request.form.get('canvas_data')
    print(name)
    f = open("reqd_backgrounds.txt","w")
    x = re.findall(r'[\d]+', name)
    for i in x:
        f.write(i)
        f.write("\n")                                                        
    f.close()
    os.chdir(WORKING_FOLDER)
    os.system("python3 addbackground.py") 

if __name__ == '__main__':
   app.run()