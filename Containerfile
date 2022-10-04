FROM python:3.10
ENV TERM xterm-256color

# Insall apache and php
RUN apt update && apt upgrade --yes && apt install apache2 php php-gd --yes

COPY requirements.txt /solar-protocol/requirements.txt
WORKDIR /solar-protocol
RUN pip install --no-cache-dir --requirement requirements.txt
COPY . /solar-protocol


# Configure apache2 to use our root directory
RUN sed --in-place \
  --expression='s|^DocumentRoot /var/www/|^DocumentRoot /solar-protocol/frontend/|' \
  /etc/apache2/sites-available/000-default.conf

RUN sed --in-place \
  --expression='$ a/\
<Directory /solar-protocol/frontend>\
Options Indexes FollowSymLinks\
AllowOverride All\
Require all granted\
Header set Access-Control-Allow-Origin "*"\
</Directory>\
' /etc/apache2/apache2.conf

# Enable server status interface
RUN sed --in-place \
  --expression='/<\/VirtualHost>/s|^|\
<Location /server-status>\
SetHandler server-status\
Require all granted\
</Location>\
|' /etc/apache2/sites-enabled/000-default.conf

RUN echo 'www-data ALL=(ALL:ALL) NOPASSWD: ALL' >> /etc/sudoers

# Enable CORS and redirection
RUN a2enmod headers && a2enmod rewrite

EXPOSE 80

# Generate frontend (jinja) templates
RUN python backend/createHTML/create_html.py DEV

CMD bash
