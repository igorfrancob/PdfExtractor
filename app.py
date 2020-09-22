import os
from flask import Flask, request, render_template, jsonify
from reader import Pdf

app = Flask(__name__, template_folder='client')
app.debug = True


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        data = request.files['file']
        data.save('/home/pdf/images.pdf')
        return 'ok'


@app.route('/test', methods=['POST'])
def test():
    if request.method == 'POST':
        data = request.json
        pdf = Pdf(data['pdf']['path'])
        result = []
        for extract in data['extract']:
            pdf.transformPdfImage()
            pdf.cutImage(extract['width'], extract['height'], extract['x'], extract['y'])
            result.append({"fieldName": extract['fieldName'], "values": pdf.imageToArray()})
        return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
