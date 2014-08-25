FROM ubuntu:trusty

MAINTAINER Thibault Cohen <titilambert@gmail.com>

ENV DEBIAN_FRONTEND noninteractive

### Init

RUN apt-get update

### Utils

RUN apt-get install -y git vim graphicsmagick nodejs phantomjs npm pkgconf libcairo2-dev libjpeg8-dev

### Installation

RUN cd /opt && git clone https://github.com/HabitRPG/habitrpg.git

#RUN cd /opt/habitrpg && git checkout -t origin/develop

RUN cd /opt/habitrpg && git pull

RUN cd /opt/habitrpg && npm install -g grunt-cli bower nodemon

RUN ln -s /usr/bin/nodejs /usr/bin/node

RUN cd /opt/habitrpg && npm install

RUN cd /opt/habitrpg && bower install --allow-root

# Add config file

ADD ./config.json /opt/habitrpg/

RUN mkdir -p /opt/habitrpg/build

# Run server

WORKDIR /opt/habitrpg

RUN /usr/local/bin/grunt build:prod 

CMD /usr/local/bin/grunt nodemon

# Install Black market

RUN apt-get install apache2 libapache2-mod-wsgi

WORKDIR /opt

RUN git clone https://github.com/titilambert/Habit-Black-Market.git habitblackmarket

RUN pip install -r requirements.txt

ADD ./settings.cfg /opt/habitblackmarket/habitblackmarket

WORKDIR /opt/habitblackmarket
