
from vector_store import (
    split_pages_into_chunks,
    store_chunks,
    search_chunks,
    get_collection
)

# Sample document pages
pages = [
    "Artificial Intelligence enables computers "
    "to perform tasks that normally require human intelligence.",

    "Machine Learning is a branch of Artificial Intelligence. "
    "It allows computers to learn from data and improve performance.",

    "Deep Learning uses neural networks with multiple layers "
    "to learn complex patterns from large amounts of data."
]

source_name = "semantic_test.pdf"

# Split document into chunks
chunks, metadatas = split_pages_into_chunks(
    pages,
    source_name
)

print("Chunks created:", len(chunks))

# Store chunks in ChromaDB
store_chunks(chunks, metadatas)

print("Chunks stored successfully!")

# Search using a question
question = "What is Machine Learning?"

print("\nSearch question:", question)

results = search_chunks(question, n_results=2)

print("\nRelevant search results:")

for result in results:
    print("\nPage:", result["page"])
    print("Source:", result["source"])
    print("Content:", result["text"])
    print("Distance:", result["distance"])

# Clean up test records
collection = get_collection()

collection.delete(
    where={"source": source_name}
)

print("\nTest completed successfully!")
