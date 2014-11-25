WD = $(shell pwd)

build:
	sudo docker build  -t habit .

run:
	sudo docker run -i -p 6666:80 -v `pwd`/new-stuff.jade:/opt/habitrpg/views/shared/new-stuff.jade  -t habit
