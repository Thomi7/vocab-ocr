FROM php:apache

COPY csv2xls/build/csv2xls /usr/bin/csv2xls

COPY process.sh /usr/bin/vocab-ocr.sh
COPY index.php /var/www/html/index.php

RUN apt-get update && apt-get install -y imagemagick tesseract-ocr tesseract-ocr-deu tesseract-ocr-eng tesseract-ocr-fra
