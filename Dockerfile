FROM ubuntu:18.04

LABEL maintainer="sokolov-as-i@yandex.ru"

RUN apt-get -qq update
RUN apt-get -qqy install python3.7

WORKDIR /var/ftp/
ENV HW1_MODE=server
#ENV HW1_HOST=127.0.0.1
ENV HW1_PORT=8080
ENV HW1_QUIET=1
ENV HW1_DIRECTORY=/var/ftp
ENV HW1_USERS=/opt/andresokol-ftp/users.tsv
ENV HW1_AUTH_DISABLED=1

WORKDIR /opt/andresokol-ftp/
COPY main.py ./
COPY server.py ./
COPY tests.py ./
COPY utils.py ./
WORKDIR /opt/andresokol-ftp/static
COPY static/demo.txt ./
COPY static/orange_pixel.png ./
WORKDIR /opt/andresokol-ftp/

#USER ftpuser
ENTRYPOINT ["python3.7", "./main.py"]
