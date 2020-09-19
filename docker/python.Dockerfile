FROM ubuntu:20.04

RUN apt-get update
RUN apt-get install python3.8 -y
RUN apt-get -y install python3-pip
RUN pip3 install pdf2image
RUN apt-get install poppler-utils -y
RUN pip3 install pytesseract
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get -y install tesseract-ocr tesseract-ocr-por
RUN pip3 install opencv-python
RUN apt-get install -y libgl1-mesa-glx
