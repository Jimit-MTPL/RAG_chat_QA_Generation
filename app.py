from llama_index.llms.ollama import Ollama
from llama_index.core import Settings
from load_file import data_ingestion

Settings.llm = Ollama(model="llama3.2:1b", request_timeout=1000)

query = """
Generate reponse based on provided prompt.
"""

def main():
    data_ingestion(query)
        
if __name__ == "__main__":
    main()
