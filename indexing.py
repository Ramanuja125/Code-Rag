from rocksdict import Rdict, Options
import json
import uuid
import codechunksHelper as cc

class CodeIndexer:
    def __init__(self, db_path):
        opt = Options()
        opt.create_if_missing(True)
        self.db = Rdict(db_path, options=opt)

    def store_chunk(self, chunk):
        chunk_id = chunk['chunk_id']
        
        # Store the full chunk
        self.db[f"chunk:{chunk_id}"] = json.dumps(chunk)
        
        # Store the full chunk
        self.db[f"chunk:{chunk_id}"] = json.dumps(chunk)
        
        # Function name index
        function_name = cc.extract_function_name(chunk['content'])
        if function_name:
            self.db[f"function:{function_name}:{chunk_id}"] = chunk_id
        
        if 'type' in chunk:
           self.db[f"functiontype:{chunk['type']}:{chunk_id}"] = chunk_id
        
        # Module name index
        if 'filepath' in chunk:
            self.db[f"module:{chunk['filepath']}:{chunk_id}"] = chunk_id
        
        # Parameter type index
        # for param_type in cc.extract_param_types(chunk['content']):
        #     self.db[f"param_type:{param_type}:{chunk_id}"] = chunk_id
        
        # Return type index
        # return_type = cc.extract_return_type(chunk['content'])
        # self.db[f"return_type:{return_type}:{chunk_id}"] = chunk_id
        
        # Language index
        self.db[f"language:{chunk['language']}:{chunk_id}"] = chunk_id

    def query(self, **kwargs):
        results = set()
        for key, value in kwargs.items():
            prefix = f"{key}:{value}:"
            for db_key, db_value in self.db.items():
                if db_key.startswith(prefix):
                    results.add(db_value)
        
        return [json.loads(self.db[f"chunk:{chunk_id}"]) for chunk_id in results]

    def close(self):
        self.db.close()



def generate_chunk_id():
    return str(uuid.uuid4())

def load_chunks_from_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# def create_code_chunks():
#     chunks = [
#         {
#             'code': '''
# def add(a: int, b: int) -> int:
#     """Returns the sum of a and b."""
#     return a + b
# ''',
#             'function_name': 'add',
#             'module_name': 'math_utils',
#             'tags': ['addition', 'math', 'integer']
#         },
#         {
#             'code': '''
# @staticmethod
# def say_hello(name: str) -> str:
#     """Greets the person by their name."""
#     return f"Hello, {name}!"
# ''',
#             'function_name': 'say_hello',
#             'module_name': 'greeter',
#             'tags': ['greeting', 'strings']
#         },
#         {
#             'code': '''
# def multiply(x, y):
#     """Multiplies two values."""
#     return x * y
# ''',
#             'function_name': 'multiply',
#             'module_name': 'operations',
#             'tags': ['multiplication', 'math']
#         }
#     ]
#     return chunks

def process_code_chunks(chunks):
    for chunk in chunks:
        chunk['chunk_id'] = generate_chunk_id()
    return chunks

def index_and_store_code_chunks():
    indexer = CodeIndexer("cchunks.db")

    chunks = load_chunks_from_json("code_chunks.json")
    processed_chunks = process_code_chunks(chunks)
    
    # Store code chunks
    for chunk in processed_chunks:
        indexer.store_chunk(chunk)

    result1 = indexer.query(function="validate")
    result2 = indexer.query(language="py")

    print(f"Number of code chunks with VALIDATE: {len(result1)}")
    print(f"Number of code chunks with all python repos: {len(result2)}")
    
    # print("Query result for type 'function':")
    # print(result1)
    # print("\nQuery result for language 'py':")
    # print(result2)

    ######TESTING######
    # Write the query result to a text file
    with open("query_results.txt", "w") as file:
        file.write(json.dumps(result1, indent=4))
    ###################

    # Close the database
    indexer.close()

if __name__ == "__main__":
    index_and_store_code_chunks()
