import os
from flask import Flask, render_template,request, redirect, url_for,flash
import urllib.request
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = 'static/uploads/'
app = Flask(__name__)
app.secret_key='xenon-key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024



ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_image():
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
        image_full_path = os.path.join(app.config['UPLOAD_FOLDER'],filename)
        file.save(image_full_path)
		#print('upload_image filename: ' + filename)
		flash('Image successfully uploaded and displayed')
		return render_template('index.html', filename=filename, full_path=image_full_path)
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)


if __name__ == '__main__':
    app.run()