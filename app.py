import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, flash
from predict import make_prediction

UPLOAD_FOLDER = 'static/uploads/'
app = Flask(__name__)
app.secret_key = 'xenon-key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.debug = False
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_image():
    if 'cdimage' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['cdimage']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        image_full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(image_full_path)
        image_result = make_prediction(image_full_path)
        return render_template('index.html', image_result=image_result)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)


if __name__ == '__main__':
    app.run()

