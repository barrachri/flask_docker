# Set the base image to Ubuntu
FROM tutum/nginx
# File Author / Maintainer
MAINTAINER Christian Barra <barrachri@gmail.com>

RUN rm /etc/nginx/sites-enabled/default
ADD sites-enabled/ /etc/nginx/sites-enabled/

VOLUME /etc/nginx/sites-enabled

