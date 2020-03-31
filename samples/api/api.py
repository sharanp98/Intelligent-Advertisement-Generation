from flask import Flask, redirect, url_for,render_template, request, send_from_directory,send_file
import os
import json
import re
# from flask_jsglue import JSGlue
from werkzeug import secure_filename

app = Flask(__name__)
# jsglue = JSGlue(app)

UPLOAD_FOLDER = '/home/sharan/Desktop/Personal Projects/Mask_RCNN/samples/'      
DOWNLOAD_FOLDER = '/home/sharan/Desktop/Personal Projects/Mask_RCNN/samples/api/static'                                  ##

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
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
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print('Image Uploaded')
            return redirect('/final')
    return render_template("upload_image.html") 

@app.route('/final')
def hello_admin():

    print('In final')
    os.chdir('/home/sharan/Desktop/Personal Projects/Mask_RCNN/samples/')
    os.system("python3 pt1.py")
    data = open('labels.txt').read().splitlines()
    return render_template("ListCategories.html",data=json.dumps(data))

@app.route('/reqjson',methods=['POST'])
def pass_val():
    name=request.form['canvas_data']
    print(name)
    os.chdir('/home/sharan/Desktop/Personal Projects/Mask_RCNN/samples/')
    f = open("reqd_images.txt","w")
    x = re.findall(r'[\w\d%!_ ]+', name)
    for i in x:
        f.write(i)
        f.write("\n")                                                          
    f.close()
    os.system("python3 pt2.py")    
    os.system("python3 copyimage.py") 
    return redirect('/disp')

@app.route('/disp')
def disp():
    return render_template("displayimage.html")


@app.route('/download',methods=['GET', 'POST'])
def download():
    return send_from_directory(directory= DOWNLOAD_FOLDER, filename='final.png')

if __name__ == '__main__':
   app.run()