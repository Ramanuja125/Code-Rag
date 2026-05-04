from data_processing import get_and_save_chunks
from indexing import index_and_store_code_chunks
from vectorstorage import run_semantic_search
from LLM import run_model

def data_chunk_and_save():
    print("Getting chunks and saving to code_chunks.json file...")
    get_and_save_chunks()
    print("Saving to code_chunks.json file complete\n")

    print("Indexing and storing code chunks...")
    index_and_store_code_chunks()
    print("Indexing and storing complete")

def main():
    data_chunk_and_save()
    while True:
        query = input("\nPlease enter a query (or type 'exit' to quit): ")
        if query.lower() == 'exit':
            print("Exiting the program.")
            break  # Exit the loop and end the program

        print("Running semantic search...")
        semantic_search, result_string = run_semantic_search(query)
        print(result_string)
        print("Semantic search complete\n")

        print("Running LLM model...")
        response = run_model(semantic_search, query)
        print("LLM model finished\n")
        print("Response:", response)

if __name__ == "__main__":
    main()