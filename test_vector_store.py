
from vector_store import (
    split_pages_into_chunks,
    store_chunks,
    get_collection
)

# Sample PDF page content
pages = [
    "Artificial Intelligence is a technology "
    "that enables machines to perform tasks "
    "that normally require human intelligence.",

    "Machine Learning is a branch of Artificial "
    "Intelligence that allows computers to learn "
    "from data and improve their performance."
]

source_name = "week14_test.pdf"

# Split text into chunks
chunks, metadatas = split_pages_into_chunks(
    pages,
    source_name
)

print("Total chunks created:", len(chunks))

# Store chunks in ChromaDB
stored_count = store_chunks(chunks, metadatas)

print("Chunks stored successfully:", stored_count)

# Verify ChromaDB storage
collection = get_collection()

print("ChromaDB total records:", collection.count())

# Remove test data
collection.delete(
    where={"source": source_name}
)

print("Test data cleaned successfully!")
