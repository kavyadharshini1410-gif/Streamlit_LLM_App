
from vector_store import (
    split_pages_into_chunks,
    store_chunks,
    get_collection
)

from qa_chain import answer_question

# Sample PDF content
pages = [
    "Artificial Intelligence enables machines "
    "to perform tasks that normally require human intelligence.",

    "Machine Learning is a branch of Artificial Intelligence. "
    "It allows computers to learn from data and improve their performance.",

    "Deep Learning uses neural networks with multiple layers "
    "to learn complex patterns from large amounts of data."
]

source_name = "qa_test.pdf"

# Split PDF text into chunks
chunks, metadatas = split_pages_into_chunks(
    pages,
    source_name
)

print("Chunks created:", len(chunks))

try:
    # Store chunks in ChromaDB
    store_chunks(chunks, metadatas)

    print("Chunks stored successfully!")

    # Ask a question
    question = "What is Machine Learning?"

    print("\nQuestion:", question)
    print("\nGenerating AI answer...\n")

    # Generate answer
    result = answer_question(question)

    print("AI ANSWER:")
    print(result["answer"])

    print("\nSOURCE DETAILS:")

    for source in result["sources"]:
        print("File:", source["source"])
        print("Page:", source["page"])

finally:
    # Remove test records
    collection = get_collection()

    collection.delete(
        where={"source": source_name}
    )

    print("\nTest data cleaned successfully!")
