build:
	sudo docker.io build  -t habit .

run:
	sudo docker.io run -i -p 6666:80 -t habit
