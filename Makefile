build:
	sudo docker.io build  -t habit .

run:
	sudo docker.io run -i -p 6666:80 -v `pwd`/new-stuff.jade:/opt/habitrpg/views/shared/new-stuff.jade  -t habit
