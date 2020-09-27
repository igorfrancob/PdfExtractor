import os
from flask import Flask, request, render_template, jsonify,send_file
from reader import Pdf
import  base64

app = Flask(__name__, template_folder='client', static_url_path = "/static", static_folder = "client/static")
app.debug = True


@app.route("/")
def index():
    return render_template('index.html', user_image = "static/image.jpg")

def load_binary(file):
    data = open(file,'rb').read()
    return data


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        data = request.files['file']
        data.save('/home/pdf/images.pdf')
        pdf = Pdf('/home/pdf/images.pdf')
        pdf.transformPdfImage()
        with open("/home/pdf/image.jpg", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        return encoded_string


@app.route('/test', methods=['POST'])
def test():
    if request.method == 'POST':
        data = request.json
        pdf = Pdf(data['pdf']['path'])
        result = []
        for extract in data['extract']:
            pdf.transformPdfImage()
            pdf.cutImage(extract['x'], extract['y'], extract['width'], extract['height'])
            result.append({"fieldName": extract['fieldName'], "values": pdf.imageToArray()})
        return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
