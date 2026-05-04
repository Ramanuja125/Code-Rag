import faiss
from sentence_transformers import SentenceTransformer
import json


class SimpleVectorStorage:
    def __init__(self, model_name='sentence-transformers/all-MiniLM-L6-v2'):
        # Load pre-trained model for code embeddings
        self.model = SentenceTransformer(model_name)

        # Dimension of embeddings from the model
        self.dim = self.model.get_sentence_embedding_dimension()

        # Create Faiss index (L2 distance)
        self.index = faiss.IndexFlatL2(self.dim)

        # Store original code chunks for reference
        self.code_chunks = []


    def add_code_chunks(self, chunks):
        # Generate embeddings for the chunks' content
        embeddings = self.model.encode([chunk["content"] for chunk in chunks], convert_to_tensor=False).astype('float32')

        # Add embeddings to Faiss index
        self.index.add(embeddings)

        # Store full chunk details
        self.code_chunks.extend(chunks)

    def search_code_chunks(self, query, top_k=3):
        query_embedding = self.model.encode([query], convert_to_tensor=False).astype('float32')

        distances, indices = self.index.search(query_embedding, top_k * 2)  # Search more to allow for duplicates

        results = []
        seen_ids = set()
        for dist, idx in zip(distances[0], indices[0]):
            similar_chunk = self.code_chunks[idx]

            # Skip if we've already seen this chunk's ID
            if similar_chunk['id'] in seen_ids:
                continue

            similarity = 1 / (1 + dist)
            results.append((similar_chunk, similarity))
            seen_ids.add(similar_chunk['id'])

            if len(results) == top_k:
                break

        return results


def load_chunks_from_json(file_path):
    """Load code chunks from a JSON file."""
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Assuming the JSON contains a list of objects with 'id', 'content', and 'filepath'
    return [{"id": chunk["id"], "content": chunk["content"], "filepath": chunk["filepath"]} for chunk in data]


def run_semantic_search(query):
    vector_search = SimpleVectorStorage()

    # Load code chunks from a JSON file
    file_path = "query_results.txt"  # Path to your JSON file
    code_chunks = load_chunks_from_json(file_path)


    # Print the sample code chunks for the user
    '''
    print("The code chunks currently stored in the system are the following:")
    for chunk in code_chunks:
        print(f"ID: {chunk['id']}")
        print(f"Content:\n{chunk['content']}")
        print(f"Filepath: {chunk['filepath']}")
        print("--------------------------------------------------------------------")
    '''


    # Create embeddings for the code chunks
    vector_search.add_code_chunks(code_chunks)

    # Search query
    results = vector_search.search_code_chunks(query)

    # Get the results as a string
    results_string = "Similar chunks:\n"
    for chunk, similarity in results:
        results_string += f"ID: {chunk['id']}\n"
        results_string += f"Content:\n{chunk['content']}\n"
        results_string += f"Filepath: {chunk['filepath']}\n"
        results_string += f"Similarity Score: {similarity:.4f}\n"
        results_string += "--------------------------------------------------------------------\n"

    return results, results_string


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--query", type=str, required=True, help="The query to run semantic search on")

    args = parser.parse_args()
    run_semantic_search(args.query)
