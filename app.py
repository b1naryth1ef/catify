from flask import Flask, render_template, send_file, request
from StringIO import StringIO
import os, sys, time, base64

import Image
from face_detect import catify

app = Flask(__name__)
app.secret_key = "change_me"

@app.route('/')
def routeRoot():
    return render_template("index.html")

@app.route("/catify", methods=["POST"])
def routeCatify():
    if request.method == 'POST':
        f = request.files['file']
        if f and f.filename.rsplit('.', 1)[1] in ["png", "jpg"]:
            out = catify(Image.open(f))
            img_io = StringIO()
            out.save(img_io, 'JPEG', quality=70)
            img_io.seek(0)
            img_data = base64.b64encode(img_io.read())
            return render_template("index.html", imgdata=img_data)#send_file(img_io, mimetype='image/jpeg')
        else:
            print f.filename.rsplit('.', 1)[1]
            return "Error #1"
    return "Error #2"

if __name__ == '__main__':
    app.run(debug=True)
