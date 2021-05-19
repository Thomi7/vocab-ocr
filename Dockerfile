FROM php:apache

RUN apt-get update && apt-get install -y imagemagick tesseract-ocr tesseract-ocr-deu tesseract-ocr-eng tesseract-ocr-fra tesseract-ocr-spa


RUN apt-get update && apt-get install -y vim

# install vocab-ocr files
COPY vocab-ocr.sh /usr/bin/vocab-ocr
COPY vocab-ocr-multiple.sh /usr/bin/vocab-ocr-multiple

COPY index.php /var/www/html/index.php
COPY index.html /var/www/html/index.html
# COPY info.php /var/www/html/info.php
# COPY .htaccess /var/www/html/.htaccess

RUN sed -e 's/post_max_size = 8M/post_max_size = 100M/' -e 's/upload_max_filesize = 2M/upload_max_filesize = 100M/' /usr/local/etc/php/php.ini-production > /usr/local/etc/php/php.ini
