
import ollama
from vector_store import search_chunks

# Configuration
LLM_MODEL = "llama3.2"


def answer_question(question, source_name=None, n_results=4):

    # Retrieve relevant PDF content
    retrieved_chunks = search_chunks(
        question,
        n_results=n_results,
        source_name=source_name
    )

    if not retrieved_chunks:
        return {
            "answer": "No relevant content found in the uploaded PDF.",
            "sources": []
        }

    # Prepare context
    context = ""

    for chunk in retrieved_chunks:
        context += (
            f"\nSource: {chunk['source']}"
            f"\nPage: {chunk['page']}"
            f"\nContent: {chunk['text']}\n"
        )

    # AI instructions
    system_prompt = """
    You are a helpful PDF question-answering assistant.

    Answer questions using only the information
    provided in the PDF context.

    If the answer is not available in the context,
    clearly say that the information was not found
    in the uploaded PDF.

    Give clear and simple answers.
    """

    user_prompt = f"""
    PDF CONTEXT:
    {context}

    QUESTION:
    {question}

    Provide the answer based only on the PDF context.
    """

    # Generate AI answer
    response = ollama.chat(
        model=LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    )

    return {
        "answer": response["message"]["content"],
        "sources": retrieved_chunks
    }
