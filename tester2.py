# Download all the 3 python files and the tester.sh files and run the shell script by - ./tester.sh
# data_processing, indexing download_LLM
# tests the data_processing and prints the details on the repository used
#tests indexing and prints the chunk ID that is generated for test_index.db
# tests the download_LLM for the model and the tokenizer
# prints the model and the tokenizer 

def test_data_processing():
    try:
        from data_processing import RepositoryCollector
        print("------------------------------------------------------------------------")
        print("Testing Data_processing...")
        #print("------------------------------------------------------------------------")
        collector = RepositoryCollector()
        #print("------------------------------------------------------------------------")
        print(f"Pass - RepositoryCollector initialized with base_dir: {collector.base_dir}")
        print("------------------------------------------------------------------------")
    except Exception as e:
        print("------------------------------------------------------------------------")
        print(f"Fail - Data_processing: {e}")
        print("------------------------------------------------------------------------")

def test_indexing():
    try:
        from indexing import CodeIndexer, generate_chunk_id
        print("------------------------------------------------------------------------")
        print("Testing Indexing...")
        #print("------------------------------------------------------------------------")

        # Initialize CodeIndexer with a proper file path
        db_path = "./test_index.db"
        indexer = CodeIndexer(db_path)
        test_chunk_id = generate_chunk_id()
        #print("------------------------------------------------------------------------")
        print(f"Pass - CodeIndexer initialized, and chunk ID generated: {test_chunk_id}")
        print("------------------------------------------------------------------------")

        # Clean up
        indexer.close()
        import shutil
        shutil.rmtree(db_path)  # Ensure cleanup of RocksDB directory
    except Exception as e:
        print("------------------------------------------------------------------------")
        print(f"Fail - Indexing: {e}")
        print("------------------------------------------------------------------------")

def test_download_llm():
    try:
        from download_LLM import model, tokenizer
        print("------------------------------------------------------------------------")
        print("Testing download_LLM...")
        #print("------------------------------------------------------------------------") 

        model_name = model.name_or_path if hasattr(model, "name_or_path") else "Unknown"
        tokenizer_name = tokenizer.name_or_path if hasattr(tokenizer, "name_or_path") else "Unknown"

        print(f"Pass - Model and tokenizer initialized successfully.")
        print(f"Model: {model_name}")
        print(f"Tokenizer: {tokenizer_name}")
        print("------------------------------------------------------------------------")
    except Exception as e:
        print("------------------------------------------------------------------------")
        print(f"Fail - download_LLM: {e}")
        print("------------------------------------------------------------------------")

if __name__ == "__main__":
    test_data_processing()
    test_indexing()
    test_download_llm()

