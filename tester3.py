# Download all the 3 python files and the tester.sh files and run the shell script by - ./tester.sh
# code rag
# tests code RAG
# Tests data_chunk_and_save and prints chunk distribution by individual repos

import os
import json

def test_code_rag():
    try:
        from Code_RAG import data_chunk_and_save
        print("------------------------------------------------------------------------")
        print("Testing Code_RAG...")

        # Redirect stdout and stderr to suppress unnecessary output
        with open(os.devnull, 'w') as fnull:
            original_stdout = os.dup(1)
            original_stderr = os.dup(2)
            os.dup2(fnull.fileno(), 1)
            os.dup2(fnull.fileno(), 2)

            try:
                data_chunk_and_save()
            finally:
                # Restore stdout and stderr
                os.dup2(original_stdout, 1)
                os.dup2(original_stderr, 2)

        # Load chunk distribution dynamically from `code_chunks.json`
        with open("code_chunks.json", "r") as file:
            chunks = json.load(file)

        # Calculate chunk distribution by repository
        chunk_distribution = {}
        for chunk in chunks:
            repo = chunk["filepath"].split('/')[2]  # Extract repository name from filepath
            chunk_distribution[repo] = chunk_distribution.get(repo, 0) + 1

        # Print meaningful output
        #print("------------------------------------------------------------------------")
        print("Pass - Code_RAG processed and saved chunks.")
        print("------------------------------------------------------------------------")
        print("Chunk Distribution by Repository:")
        for repo, count in sorted(chunk_distribution.items(), key=lambda x: x[1], reverse=True):
            print(f"{repo}: {count} chunks")
        print("------------------------------------------------------------------------")
    except Exception as e:
        print(f"Fail - Code_RAG: {e}")

if __name__ == "__main__":
    test_code_rag()
