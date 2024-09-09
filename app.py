import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Set the upload folder and allowed extensions
UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check if the file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    # Get the filenames from query parameters (if available)
    logo_filename = request.args.get('logo', 'default_logo.png')
    image_filename = request.args.get('image', 'default_image.png')

    return render_template('index.html', logo_filename=logo_filename, image_filename=image_filename)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'logo' not in request.files or 'image' not in request.files:
            return "No file part"

        logo = request.files['logo']
        image = request.files['image']

        if logo and allowed_file(logo.filename):
            logo_filename = secure_filename(logo.filename)
            logo.save(os.path.join(app.config['UPLOAD_FOLDER'], logo_filename))

        if image and allowed_file(image.filename):
            image_filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

        # Redirect to the home page and pass the uploaded filenames as query parameters
        return redirect(url_for('index', logo=logo_filename, image=image_filename))

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
