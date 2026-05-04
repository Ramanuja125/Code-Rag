# Project-6-Group-06

## To run this program
First build a docker image with the command:\
docker build -t group-project-image .\
Then create a docker container with the command:\
docker run -d -p 3306:3306 --name group-project group-project-image\
Once the container is created, open a shell inside the container with the command:\
docker exec -it group-project bash


### To run the testing script, use the following:
./tester.sh


### To run the program, use the following command:
python3 Code_RAG.py


Once that is done, you will be prompted to enter a query. Enter your query and wait until the
LLM generates a response. Then, you will be prompted to enter a new query or exit system.

Note: The build takes lot of time, because of the amount of libraries and code files that are imported
Be prepared for the code to take 25+ minutes to build, depending on system configuration.
