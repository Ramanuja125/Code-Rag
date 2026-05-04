# Code - Rag
## Overview
 
Code RAG is a Retrieval-Augmented Generation (RAG) system specifically designed for coding tasks. It combines semantic code retrieval with a large language model to help developers efficiently access relevant code snippets, documentation, and context-aware code suggestions.
 
Unlike general-purpose RAG systems — which handle broad natural language tasks like articles or Q&A — Code RAG focuses exclusively on code-related tasks such as code generation, documentation, completion, and refactoring.
 
---

## System Architecture
 
The pipeline flows as follows:
 
```
GitHub Repository → Code Chunking → RocksDB (Indexing)

                                          ↓
User Prompt → Semantic Search (Faiss) → LLM (Qwen2.5-Coder) → Response
```

### Key Components
 
| Component | Technology | Role |
|---|---|---|
| **Data Processing** | Custom Parser | Extracts code chunks, filters irrelevant data |
| **Object Storage / Indexing** | RocksDB (LSM-tree) | Organizes and stores code chunks |
| **Vector Storage** | Faiss | Stores and retrieves semantic embedding vectors |
| **Language Model** | Qwen2.5-Coder-1.5B | Generates context-aware code suggestions and explanations |



## To run this program
Clone the repo and inside the Dockerfile on line 40 - create a personal access token and add the value there -
it would look something like this 
```
https://ghp_fdifiweorqwproqiejqwujeqweiwqjeioqwj@github.com
```
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
