# base image
FROM python:3.8

# install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        tzdata \
        python3-setuptools \
        python3-pip \
        python3-dev \
        python3-venv \
        git \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# install mongodb
RUN wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | apt-key add -
RUN echo "deb http://repo.mongodb.org/apt/debian buster/mongodb-org/4.4 main" | tee /etc/apt/sources.list.d/mongodb-org-4.4.list
RUN apt-get update
RUN apt-get install -y mongodb-org

# create and set working directory
#RUN mkdir /wealthy_api
#WORKDIR /wealthy_api
WORKDIR /app

# add current directory code to working directory
COPY ./wealthy_api /app/wealthy_api
COPY ./docker /app/docker

# set project enviroment variables
ENV PORT=8000

# set default enviroment variables
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

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