import sys
import io
import tempfile
from pdf2image import convert_from_path
from PIL import Image
import pytesseract  # Módulo para a utilização da tecnologia OCR


class Pdf:
    def __init__(self, name):
        self.name = name

    def improvment(self):
        img = Image.open('/home/pdf/cropped.jpg')
        new_size = tuple(2*x for x in img.size)
        img = img.resize(new_size, Image.ANTIALIAS)
        print('TETSE')
        print(pytesseract.image_to_string(img))

    def transformPdfImage(self):
        with tempfile.TemporaryDirectory() as path:
            images_from_path = convert_from_path(self.name, 200)
            for page in images_from_path:
                page.save('/home/pdf/image' + ".jpg", 'PNG')

    def cutImage(self, x1, y1, x2, y2):
        imageObject = Image.open('/home/pdf/image' ".jpg")
        w, h = imageObject.size
        cropped = imageObject.crop((x1,y1,x1+x2,y1+y2))
        cropped.save('/home/pdf/cropped.jpg', 'PNG')

    def imageToText(self, filename):
        img = Image.open('/home/pdf/out' ".jpg")
        result = pytesseract.image_to_string('/home/pdf/cropped' ".jpg", config='--psm 6 --oem 3 -c preserve_interword_spaces=1x1 tessedit_char_whitelist=|_0123456789ABCDEFGHIJKLMNOPQRSTUVXZÇ./,abcdefghijklmnopqrstuvxzç')
        with open(filename, mode='w') as file:
            file.write(result)
        print(result)

    def imageToArray(self):
        img = Image.open('/home/pdf/image' ".jpg")
        result = pytesseract.image_to_string('/home/pdf/cropped' ".jpg", config='--psm 6 --oem 3 -c preserve_interword_spaces=1x1 tessedit_char_whitelist=|_0123456789ABCDEFGHIJKLMNOPQRSTUVXZÇ./,abcdefghijklmnopqrstuvxzç')
        return result

if __name__ == '__main__':
    pdf = Pdf('/home/60751689-Modelo-Contra-Cheque.pdf')
    pdf.transformPdfImage()
    pdf.cutImage(100, 83, 88, 63)
    pdf.imageToText('/home/pdf/codigo.txt')

    pdf = Pdf('/home/60751689-Modelo-Contra-Cheque.pdf')
    pdf.transformPdfImage()
    pdf.cutImage(87, 83, 58, 63)
    pdf.imageToText('/home/pdf/descricao.txt')

    pdf = Pdf('/home/60751689-Modelo-Contra-Cheque.pdf')
    pdf.transformPdfImage()
    pdf.cutImage(57, 83, 47, 63)
    pdf.imageToText('/home/pdf/referencia.txt')

    pdf = Pdf('/home/60751689-Modelo-Contra-Cheque.pdf')
    pdf.transformPdfImage()
    pdf.cutImage(47, 83, 30, 63)
    pdf.imageToText('/home/pdf/vencimentos.txt')

    pdf = Pdf('/home/60751689-Modelo-Contra-Cheque.pdf')
    pdf.transformPdfImage()
    pdf.cutImage(29, 83, 13.3, 63)
    pdf.imageToText('/home/pdf/descontos.txt')

    pdf.improvment()