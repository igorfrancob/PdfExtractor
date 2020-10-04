import os
import base64
import re
from flask import Flask, request, render_template, jsonify, send_file
from reader import Pdf
from table import Table


app = Flask(__name__, template_folder='client', static_url_path="/static", static_folder="client/static")
app.debug = True


@app.route("/")
def index():
    return render_template('index.html', user_image="static/image.jpg")


def load_binary(file):
    data = open(file, 'rb').read()
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


@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        data = request.json
        pdf = Pdf(data['pdf']['path'])
        #return jsonify(pdf.imageToData().split('\n'))
        result = []
        for extract in data['extract']:
            if extract['type'] == 'table':
                pdf.transformPdfImage()
                pdf.cutImage(extract['coordinates']['x'], extract['coordinates']['y'], extract['coordinates']['width'], extract['coordinates']['height'])
                test = []
                for f in extract['fields']:
                    test.append(f['index'] - 1)
                table = Table(pdf.imageToArray(),test)
                result.append({"fieldName": extract['fields'], "values": table.wordsSelected(7)})

        return jsonify(result)


@app.route('/table', methods=['POST'])
def htmlTable():
    data = request.json
    pdf = Pdf('/home/pdf/images.pdf')
    pdf.transformPdfImage()
    pdf.cutImage(data['x'], data['y'], data['width'], data['height'])
    table = Table(pdf.imageToArray())
    return jsonify(table.totalColumns(6))


def find_str(s, char):
    index = 0

    if char in s:
        c = char[0]
        for ch in s:
            if ch == c:
                if s[index:index+len(char)] == char:
                    return index

            index += 1

    return -1

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
