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

RUN mkdir -p /opt/habitrpg/build

# Build server

WORKDIR /opt/habitrpg

RUN /usr/local/bin/grunt build:prod 

# Install Black market

RUN apt-get install -y lighttpd python-pip

WORKDIR /opt

RUN git clone https://github.com/titilambert/Habit-Black-Market.git habitblackmarket

WORKDIR /opt/habitblackmarket

RUN pip install -r requirements.txt

RUN pip install flup

# Aff config files

ADD ./settings.cfg /opt/habitblackmarket/habitblackmarket/

ADD ./config.sample/lighttpd.conf /etc/lighttpd/conf-enabled/habitrpg.conf

ADD ./config.json /opt/habitrpg/

# Patch habitrpg

ADD patches/menu.patch /opt/habitrpg/

WORKDIR /opt/habitrpg/

RUN patch -p1 < menu.patch

# RUN SERVER

RUN lighttpd-enable-mod fastcgi

CMD ip a && service lighttpd restart && cd /opt/habitrpg && /usr/local/bin/grunt nodemon
