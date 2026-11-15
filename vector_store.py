
import uuid
import chromadb
import ollama

# Configuration
CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "pdf_documents"
EMBEDDING_MODEL = "nomic-embed-text"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
BATCH_SIZE = 32


# Connect to ChromaDB
def get_collection():

    client = chromadb.PersistentClient(
        path=CHROMA_PATH
    )

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )

    return collection


# Split PDF pages into smaller chunks
def split_pages_into_chunks(
    pages,
    source_name,
    chunk_size=CHUNK_SIZE,
    overlap=CHUNK_OVERLAP
):

    if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
        raise ValueError("Invalid chunk size or overlap.")

    chunks = []
    metadatas = []

    step = chunk_size - overlap

    for page_number, page_text in enumerate(
        pages, start=1
    ):

        text = " ".join((page_text or "").split())

        if not text:
            continue

        chunk_index = 0

        for start in range(0, len(text), step):

            chunk = text[start:start + chunk_size].strip()

            if chunk:

                chunks.append(chunk)

                metadatas.append({
                    "source": source_name,
                    "page": page_number,
                    "chunk_index": chunk_index
                })

                chunk_index += 1

    return chunks, metadatas


# Generate embeddings and store chunks
def store_chunks(chunks, metadatas):

    if not chunks:
        return 0

    if len(chunks) != len(metadatas):
        raise ValueError("Chunks and metadata counts do not match.")

    collection = get_collection()

    # Generate embeddings in batches
    all_embeddings = []

    for start in range(0, len(chunks), BATCH_SIZE):

        batch = chunks[start:start + BATCH_SIZE]

        response = ollama.embed(
            model=EMBEDDING_MODEL,
            input=batch
        )

        all_embeddings.extend(response["embeddings"])

    # Remove previous chunks from the same PDF
    source_name = metadatas[0]["source"]

    collection.delete(
        where={"source": source_name}
    )

    # Store chunks and embeddings
    ids = [str(uuid.uuid4()) for _ in chunks]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=all_embeddings,
        metadatas=metadatas
    )

    return len(chunks)

# Search for relevant PDF chunks
def search_chunks(question, n_results=4):

    collection = get_collection()

    total_records = collection.count()

    if total_records == 0:
        return []

    # Generate embedding for the question
    response = ollama.embed(
        model=EMBEDDING_MODEL,
        input=question
    )

    question_embedding = response["embeddings"][0]

    # Search ChromaDB
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=min(n_results, total_records),
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    matches = []

    for i, document in enumerate(results["documents"][0]):

        metadata = results["metadatas"][0][i]

        matches.append({
            "text": document,
            "source": metadata["source"],
            "page": metadata["page"],
            "distance": results["distances"][0][i]
        })

    return matches

# Search for relevant PDF chunks
def search_chunks(question, n_results=4, source_name=None):

    collection = get_collection()

    total_records = collection.count()

    if total_records == 0:
        return []

    # Generate question embedding
    response = ollama.embed(
        model=EMBEDDING_MODEL,
        input=question
    )

    question_embedding = response["embeddings"][0]

    # Prepare search parameters
    search_parameters = {
        "query_embeddings": [question_embedding],
        "n_results": min(n_results, total_records),
        "include": [
            "documents",
            "metadatas",
            "distances"
        ]
    }

    # Restrict search to the selected PDF
    if source_name:
        search_parameters["where"] = {
            "source": source_name
        }

    # Search ChromaDB
    results = collection.query(**search_parameters)

    matches = []

    for i, document in enumerate(results["documents"][0]):

        metadata = results["metadatas"][0][i]

        matches.append({
            "text": document,
            "source": metadata["source"],
            "page": metadata["page"],
            "distance": results["distances"][0][i]
        })

    return matches

# Search for relevant PDF chunks
def search_chunks(question, n_results=4, source_name=None):

    collection = get_collection()

    total_records = collection.count()

    if total_records == 0:
        return []

    # Generate question embedding
    response = ollama.embed(
        model=EMBEDDING_MODEL,
        input=question
    )

    question_embedding = response["embeddings"][0]

    # Prepare search parameters
    search_parameters = {
        "query_embeddings": [question_embedding],
        "n_results": min(n_results, total_records),
        "include": [
            "documents",
            "metadatas",
            "distances"
        ]
    }

    # Restrict search to the selected PDF
    if source_name:
        search_parameters["where"] = {
            "source": source_name
        }

    # Search ChromaDB
    results = collection.query(**search_parameters)

    matches = []

    for i, document in enumerate(results["documents"][0]):

        metadata = results["metadatas"][0][i]

        matches.append({
            "text": document,
            "source": metadata["source"],
            "page": metadata["page"],
            "distance": results["distances"][0][i]
        })

    return matches

# Search for relevant PDF chunks
def search_chunks(question, n_results=4, source_name=None):

    collection = get_collection()

    total_records = collection.count()

    if total_records == 0:
        return []

    # Generate question embedding
    response = ollama.embed(
        model=EMBEDDING_MODEL,
        input=question
    )

    question_embedding = response["embeddings"][0]

    # Prepare search parameters
    search_parameters = {
        "query_embeddings": [question_embedding],
        "n_results": min(n_results, total_records),
        "include": [
            "documents",
            "metadatas",
            "distances"
        ]
    }

    # Restrict search to the selected PDF
    if source_name:
        search_parameters["where"] = {
            "source": source_name
        }

    # Search ChromaDB
    results = collection.query(**search_parameters)

    matches = []

    for i, document in enumerate(results["documents"][0]):

        metadata = results["metadatas"][0][i]

        matches.append({
            "text": document,
            "source": metadata["source"],
            "page": metadata["page"],
            "distance": results["distances"][0][i]
        })

    return matches

