# TO RUN THIS DOCKER FILE
# First build a docker image with the command:
# docker build -t group-project-image .
# Then create a docker container with the command:
# docker run -d -p 3306:3306 --name group-project group-project-image
# Once the container is created, open a shell inside the container with the command:
# docker exec -it group-project bash
# Once you are in the bash terminal, run:
# python3 Code_RAG.py
# Once that is done, you will be prompted to enter a query. Enter your query and wait until the
# LLM generates a response. Then, you will be prompted to enter a new query or exit system.
# The build takes lot of time, because we have transformers and torch which takes lot of time.
# Be prepared for the code to take 25+ minutes to build, depending on system configuration.

# ----------------- code starts from here -------------------------- above has the Dockerfile version and how to run the docker file as container
# Use Ubuntu 22.04 as the base image
FROM ubuntu:22.04

# Set non-interactive mode to suppress apt prompts
ENV DEBIAN_FRONTEND=noninteractive

# Create a working directory
WORKDIR /cse511

# Install tools, Percona Server with RocksDB, and Python3 with pip
RUN apt update && apt install -y git-all \
    curl gnupg2 lsb-release software-properties-common python3 python3-pip nano vim && \
    curl -O https://repo.percona.com/apt/percona-release_latest.generic_all.deb && \
    apt install -y ./percona-release_latest.generic_all.deb && \
    percona-release enable-only ps-84-lts release && \
    percona-release enable tools release && \
    apt update && \
    apt install -y percona-server-server percona-server-rocksdb && \
    apt clean

# Remove existing contents of /cse511 if any
RUN rm -rf /cse511/*

# Copy requirements.txt from the main branch repository
RUN git clone --branch integration https://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@github.com/Fall-24-CSE511-Data-Processing-at-Scale/Project-6-Group-06.git /cse511

# Install Python libraries listed in the requirements.txt file
RUN pip3 install --no-cache-dir -r /cse511/requirements.txt

# Set permissions for the /cse511 directory
RUN chmod -R 777 /cse511/*

# Expose MySQL port
EXPOSE 3306

# Configure MySQL to run as root and allow MyRocks plugin
CMD ["mysqld_safe", "--user=root", "--plugin-load-add=ha_rocksdb.so"]

RUN python3 download_LLM.py

#CMD ["python3", "Code_RAG.py"]
