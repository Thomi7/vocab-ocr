FROM php:apache

RUN apt update && apt install -y tesseract-ocr python3-minimal python3-pip python3-opencv

RUN pip3 install pytesseract
RUN apt purge -y python3-pip && apt autoremove -y

RUN apt install -y tesseract-ocr-deu tesseract-ocr-eng tesseract-ocr-fra tesseract-ocr-spa

# increase maximum file upload size
RUN sed -e 's/post_max_size = 8M/post_max_size = 100M/' -e 's/upload_max_filesize = 2M/upload_max_filesize = 100M/' /usr/local/etc/php/php.ini-production > /usr/local/etc/php/php.ini

# install vocab-ocr files
COPY index.html /var/www/html/index.html
COPY images /var/www/html/images
COPY upload.php /var/www/html/upload.php
COPY processing.py /usr/bin/vocab-ocr
