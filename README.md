@'
# PDF Question Answering System

## Project Overview
This project is an AI-powered PDF Question Answering System. Users can upload PDF documents and ask questions. The application retrieves relevant information from the PDF and generates answers using a local Large Language Model.

## Features
- Upload PDF documents.
- Extract text from PDF pages.
- Split text into smaller chunks.
- Generate embeddings using Ollama.
- Store embeddings in ChromaDB.
- Perform semantic search.
- Generate answers using Llama 3.2.
- Display source pages and retrieved content.
- Maintain conversation history.
- Clear chat history.

## Technologies Used
- Python
- Streamlit
- Ollama
- Llama 3.2
- nomic-embed-text
- ChromaDB
- PyPDF

## Installation and Execution

1. Install Python and Ollama.
2. Download the required Ollama models:

   ollama pull llama3.2
   ollama pull nomic-embed-text

3. Install project dependencies:

   pip install -r requirements.txt

4. Run the application:

   python -m streamlit run app.py

5. Open the local URL displayed in the terminal.

## Project Structure

- app.py - Streamlit application
- vector_store.py - Text chunking, embeddings and vector storage
- qa_chain.py - AI question-answering logic
- test_vector_store.py - Vector storage testing
- test_semantic_search.py - Semantic search testing
- test_qa_chain.py - Question-answering testing
- requirements.txt - Project dependencies
- .gitignore - Files excluded from GitHub

## AI Models
- Language Model: Llama 3.2
- Embedding Model: nomic-embed-text
- Vector Database: ChromaDB
'@ | Set-Content -Encoding UTF8 README.md