import os
import subprocess
import json
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

class RepositoryCollector:
    def __init__(self, base_dir: str = './repositories'):
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)
        
        # Comprehensive repository collection
        self.repositories = {
             'Python': [
                'https://github.com/tensorflow/tensorflow',
                'https://github.com/django/django',
                'https://github.com/numpy/numpy',
                'https://github.com/pandas-dev/pandas',
                'https://github.com/scikit-learn/scikit-learn',
                'https://github.com/python/cpython',  
                'https://github.com/pallets/flask',  
                'https://github.com/psf/requests',    
                'https://github.com/pytorch/pytorch'
            ] 
            #'Python': ['https://github.com/psf/requests']
        }

    def clone_repository(self, repo_url: str, max_depth: Optional[int] = None) -> str:
        """
        Clone a repository with optional shallow clone to reduce data volume

        """
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        local_path = os.path.join(self.base_dir, repo_name)
        
        if os.path.exists(local_path):
            #print(f"Repository {repo_name} already exists. Pulling latest changes.")
            subprocess.run(['git', '-C', local_path, 'pull'], check=True)
        else:
            #print(f"Cloning {repo_url}")
            clone_cmd = ['git', 'clone', repo_url, local_path]
            
            # Add shallow clone option if max_depth is specified
            if max_depth:
                clone_cmd.extend(['--depth', str(max_depth)])
            
            subprocess.run(clone_cmd, check=True)
        
        return local_path

    def extract_code_chunks(self, 
                             repo_path: str, 
                             file_extensions: List[str] = ['.py']) -> List[Dict]:
        """
        Enhanced code chunk extraction with more sophisticated filtering
        """
        code_chunks = []
        
        # Define directories to exclude
        excluded_dirs = [
            '.git', 'node_modules', 'venv', '__pycache__', 
            'test', 'tests', 'examples', 'docs', 'benchmarks', 'build', 'dist', 'assets', 'logs'
        ]
        
        for root, dirs, files in os.walk(repo_path):
            # Filter out excluded directories
            dirs[:] = [d for d in dirs if d not in excluded_dirs]
            
            for file in files:
                if any(file.endswith(ext) for ext in file_extensions):
                    full_path = os.path.join(root, file)
                    
                    try:
                        with open(full_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                             # Enhanced chunking with language detection
                            chunks = self._split_into_chunks(content, full_path)
                            code_chunks.extend(chunks)
                    except Exception as e:
                        print(f"Error processing {full_path}: {e}")
        
        return code_chunks

    def _split_into_chunks(self, content: str, filepath: str) -> List[Dict]:
        """
        More sophisticated chunking strategy
        """
        chunks = []
        language = filepath.split('.')[-1]
        
        # Minimum chunk size and complexity thresholds
        min_chunk_size = 100  # Increased from previous 50
        max_chunk_size = 1000
        
        # Simple splitting with language awareness
        if language in ['py', 'java', 'js', 'ts']:
            import re
            
            # Regex patterns for different languages
            patterns = {
                'py': r'(def\s+\w+|class\s+\w+)',
                'java': r'(public|private|protected)\s+.*?\{',
                'js': r'function\s+\w+|\w+\s*=\s*\([^)]*\)\s*=>',
                'ts': r'function\s+\w+|\w+\s*=\s*\([^)]*\)\s*=>|class\s+\w+'
            }
            
            if language in patterns:
                func_matches = list(re.finditer(patterns[language], content))
                
                for i in range(len(func_matches)):
                    start = func_matches[i].start()
                    end = func_matches[i+1].start() if i+1 < len(func_matches) else len(content)
                    
                    chunk = content[start:end].strip()
                    
                    if min_chunk_size < len(chunk) < max_chunk_size:
                        chunks.append({
                            'id': f"{filepath}_{i}",
                            'content': chunk,
                            'filepath': filepath,
                            'language': language,
                            'type': 'function' if 'def' in chunk or 'function' in chunk else 'class'
                        })
        
        # Fallback for languages without specific parsing
        if not chunks:
            # Basic chunking
            for idx, chunk in enumerate(content.split('\n\n'), 1):
                if min_chunk_size < len(chunk.strip()) < max_chunk_size:
                    chunks.append({
                        'id': f"{filepath}_{idx}",
                        'content': chunk.strip(),
                        'filepath': filepath,
                        'language': language
                    })
        
        return chunks

    def save_chunks(self, chunks: List[Dict], output_file: str = 'code_chunks.json'):
        """
        Save extracted chunks to a JSON file with more detailed metadata
        """
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(chunks, f, indent=2, ensure_ascii=False)

    def process_repository(self, repo_url: str) -> List[Dict]:
        try:
            repo_path = self.clone_repository(repo_url, max_depth=1)
            return self.extract_code_chunks(repo_path)
        except Exception as e:
            print(f"Failed to process {repo_url}: {e}")
            return []

def get_and_save_chunks():
    collector = RepositoryCollector()
    
    all_chunks = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        for language, repos in collector.repositories.items():
            for repo_url in repos:
                futures.append(executor.submit(collector.process_repository, repo_url))
        
        for future in as_completed(futures):
            chunks = future.result()
            all_chunks.extend(chunks)
            #print(f"Successfully collected {len(chunks)} chunks.")
    
    # Save and analyze chunks
    collector.save_chunks(all_chunks)
    print(f"\nTotal code chunks collected: {len(all_chunks)}")

    # Detailed language and repository statistics
    language_stats = {}
    repo_stats = {}
    for chunk in all_chunks:
        language = chunk['language']
        repo = chunk['filepath'].split('/repositories/')[-1].split('/')[0]
        
        language_stats[language] = language_stats.get(language, 0) + 1
        repo_stats[repo] = repo_stats.get(repo, 0) + 1
    
    print("\nChunk Distribution by Language:")
    for lang, count in sorted(language_stats.items(), key=lambda x: x[1], reverse=True):
        print(f"{lang}: {count} chunks")
    
    print("\nChunk Distribution by Repository:")
    for repo, count in sorted(repo_stats.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"{repo}: {count} chunks")

if __name__ == '__main__':
    get_and_save_chunks()
