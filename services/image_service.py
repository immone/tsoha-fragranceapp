import app
import imghdr
import os
from flask import send_from_directory, request
from werkzeug.utils import secure_filename

# Inspired by https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask

class ImageService:
    def validate_image(stream):
        header = stream.read(512)
        stream.seek(0)
        format = imghdr.what(None, header)
        if not format:
            return None
        return '.' + (format if format != 'jpeg' else 'jpg')

    def post(self, id):
        img = request.files["file"]
        filename = secure_filename(img.name)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                    file_ext != self.validate_image(img.stream):
                return None
            img.save(os.path.join(app.config['UPLOAD_PATH'], str(id) + file_ext))
        return True

    def get(self, filename):
        return send_from_directory(app.config['UPLOAD_PATH'], filename)


img_service = ImageService()