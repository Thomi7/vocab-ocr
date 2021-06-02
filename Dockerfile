FROM php:apache

RUN apt-get update && apt-get install -y tesseract-ocr tesseract-ocr-deu tesseract-ocr-eng tesseract-ocr-fra tesseract-ocr-spa

RUN sed -e 's/post_max_size = 8M/post_max_size = 100M/' -e 's/upload_max_filesize = 2M/upload_max_filesize = 100M/' /usr/local/etc/php/php.ini-production > /usr/local/etc/php/php.ini

RUN apt-get update && apt-get install -y vim
RUN apt-get install -y python3-minimal
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-opencv
RUN pip3 install pytesseract cv2-tools cv
# RUN pip3 install opencv-python-headless


# install vocab-ocr files
COPY index.html /var/www/html/index.html
COPY upload.php /var/www/html/upload.php
COPY processing.py /usr/bin/vocab-ocr
