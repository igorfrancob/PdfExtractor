import os
from flask import Flask, request, render_template, jsonify,send_file
from reader import Pdf
import  base64
import re    

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
            if (extract['blanks'] == '1'):
                result.append({"fieldName": extract['fieldName'], "values": pdf.imageToArrayPreserve(), "blanks": extract['blanks']})
            else:
                result.append({"fieldName": extract['fieldName'], "values": pdf.imageToArray(), "blanks": extract['blanks']})
        lines = pdf.imageToArray().split('\n')
        i = 0
        lists = []
        for line in lines:
            listIntermediate = []
            tokens = re.findall('\s+', line)
            words = line.split('  ')
            words[:] = [x for x in words if x]
            newLine = line
            #newLine = re.sub(r'[^A-Za-z0-9 ]+', '', line)
            for wordInt in words:
                word = wordInt.strip()
                #word = re.sub(r'[^A-Za-z0-9 ]+', '', word)
                if len(word) > 0:
                    listIntermediate.append([newLine.find(word), word])
                    newLine = newLine.replace(word, " "*len(word), 1)
            lists.append(listIntermediate)

        columns = []
        for listColumn in lists:
            for lcol in listColumn:
                if not columns:
                    columns.append(lcol[0])
                else:
                    b = True
                    for c in columns:
                        minor = c + 6
                        major = c - 6
                        if lcol[0] < minor and lcol[0] > major:
                            b = False
                            break
                    if (b):
                        columns.append(lcol[0])
        result = []
        for listColumn in lists:
            inermediateResult = []
            for c in columns:
                minor = c - 6
                major = c + 6
                b = True
                for lcol in listColumn:
                    if lcol[0] > minor and lcol[0] < major:
                        inermediateResult.append(lcol[1])
                        b = False
                if b:
                    inermediateResult.append(' ')
            result.append(inermediateResult)
        return jsonify(result)

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
