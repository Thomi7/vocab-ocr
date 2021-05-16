FROM php:apache

RUN apt-get update && apt-get install -y imagemagick tesseract-ocr tesseract-ocr-deu tesseract-ocr-eng tesseract-ocr-fra

# install vocab-ocr files
COPY process.sh /usr/bin/vocab-ocr.sh
COPY index.php /var/www/html/index.php
