from setup_ingestion_pipeline import create_or_load_pipeline
from llama_index.core import SimpleDirectoryReader
from engine_create import interact_with_llm, create_chat_engine
import os
from llama_index.readers.file import MarkdownReader
from typing import List
from flair.splitter import SegtokSentenceSplitter

# Function to split the content into chunks
def split_into_chunks(text, chunk_size=200):
    # Split the text into chunks of specified size
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def semantic_splitter(text: str, chunk_size: int = 1000, chunk_overlap: int = 10) -> List[str]:
    splitter = SegtokSentenceSplitter()
    
    # Split text into sentences
    sentences = splitter.split(text)

    chunks = []
    current_chunk = ""

    for sentence in sentences:
        # Add sentence to the current chunk
        if len(current_chunk) + len(sentence.to_plain_string()) <= chunk_size:
            current_chunk += " " + sentence.to_plain_string()
        else:
            # If adding the next sentence exceeds max size, start a new chunk
            chunks.append(current_chunk.strip())
            current_chunk = sentence.to_plain_string()

    # Add the last chunk if it exists
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def data_ingestion(query):
    #processed_files_file = 'processed_files.txt'
    input_file = "marker-output/BS_2_table/BS_2_table.md"

    # Check if the processed files list exists, if not create it
    """
    if not os.path.exists(processed_files_file):
        open(processed_files_file, 'w').close()  # Create an empty file

    # Read the list of processed files
    with open(processed_files_file, 'r') as f:
        processed_files = f.read().splitlines()

    # If the file has already been processed, skip it
    if input_file in processed_files:
        print(f"{input_file} has already been processed. Skipping ingestion.")
        return
    else:
    """
    parser = MarkdownReader()
    file_extractor = {".md": parser}
    reader = SimpleDirectoryReader(
                input_files=[input_file],
                file_extractor=file_extractor
            )

        # Load the content from the file
    documents = reader.load_data()

        # Initialize pipeline
    

    for document in documents:
            # Split document into chunks
        chunks = semantic_splitter(document.text)

            # Process each chunk through the pipeline
        for i, chunk in enumerate(chunks):
            print(f"Processing chunk {i+1} of file {input_file}...")
            print(f"Chunk {i+1} content:\n{chunk}\n")
                # Convert the chunk into a document format (create a new Document object or text block)
            chunk_document = type(document)(text=chunk)
            pipeline = create_or_load_pipeline()
                # Pass the chunked document through the pipeline
            nodes = pipeline.run(documents=[chunk_document])
            print(f"Ingested {len(nodes)} Nodes from chunk {i+1}")

                # Interact with LLM for the processed chunk
            print(f"Running query on chunk {i+1}...")
            output = interact_with_llm(query)
            print(f"Response for chunk {i+1}: {output}")

        # Add the file to the list of processed files
    """
    with open(processed_files_file, 'a') as f:
        f.write(input_file + '\n')
    """

"""
from setup_ingestion_pipeline import create_or_load_pipeline
#from load_gdrive_files import load_data_from_gdrive
from llama_index.core import SimpleDirectoryReader
import os
from llama_index.readers.file import MarkdownReader

def data_ingestion():
    processed_files_file = 'processed_files.txt'
    input_file = "marker-output\BS_2_table\BS_2_table.md"

    # Check if the processed files list exists, if not create it
    if not os.path.exists(processed_files_file):
        open(processed_files_file, 'w').close()  # Create an empty file

    # Read the list of processed files
    with open(processed_files_file, 'r') as f:
        processed_files = f.read().splitlines()

    # If the file has already been processed, skip it
    if input_file in processed_files:
        print(f"{input_file} has already been processed. Skipping ingestion.")
        return
    else:
        parser = MarkdownReader()
        file_extractor = {".md": parser}
        reader = SimpleDirectoryReader(
                    input_files=[input_file],
                    file_extractor=file_extractor
                )

        documents = reader.load_data()

        pipeline = create_or_load_pipeline()

        # Process the documents using the pipeline
        nodes = pipeline.run(documents=documents)
        print(f"Ingested {len(nodes)} Nodes")

        # Add the file to the list of processed files
        with open(processed_files_file, 'a') as f:
            f.write(input_file + '\n')
"""