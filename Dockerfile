FROM ubuntu:14.04
RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get -y install python3-dev build-essential git libpython3-dev libpq-dev wget
RUN ln -s /usr/bin/python3.4 /usr/bin/python
RUN wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py && python get-pip.py
ADD ./ /app
RUN pip install -r /app/requirements.txt
