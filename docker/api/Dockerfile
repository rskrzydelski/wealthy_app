# base image
FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# install system dependencies
RUN apt-get update
RUN apt-get install -y build-essential
RUN apt-get install -y python3
RUN apt-get install -y python3-setuptools
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-dev
RUN apt-get install -y python3-venv
RUN apt-get install -y git
RUN apt-get install -y vim
RUN apt-get install -y wget
RUN apt-get install -y libpq-dev

# install mongodb
RUN wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | apt-key add -
RUN echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-4.4.list
RUN apt-get update
RUN apt-get install -y mongodb-org

# create and set working directory
WORKDIR /app

# add current directory code to working directory
COPY ./wealthy_api /app/wealthy_api
COPY ./docker /app/docker

# create default mongodb data directory
RUN mkdir -p /data/db
# create log file for mongodb
RUN touch /var/log/mongod.log

# set project enviroment variables
ENV PORT=8000

# set default enviroment variables
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8

# install enviroment dependencies
RUN pip3 install --upgrade pip

# install requirements.txt
RUN pip3 install -r wealthy_api/requirements.txt

# install custom python libs
# mongomarket lib
RUN cd wealthy_api/mongomarket-lib/ && python3 setup.py sdist bdist_wheel && pip install dist/mongomarket-lib-0.0.1.tar.gz
# coinmarketcapscrapper lib
RUN cd wealthy_api/coinmarketcapscrapper-lib/ && python3 setup.py sdist bdist_wheel && pip install dist/coinmarketcapscrapper-lib-0.0.1.tar.gz
# alphavantage lib
RUN cd wealthy_api/alphavantage-lib/ && python3 setup.py sdist bdist_wheel && pip install dist/alphavantage-lib-0.0.1.tar.gz

