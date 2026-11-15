
import streamlit as st
from pypdf import PdfReader
from io import BytesIO
from pathlib import Path
import hashlib
import time

from vector_store import split_pages_into_chunks, store_chunks
from qa_chain import answer_question


# Page configuration
st.set_page_config(
    page_title="PDF Question Answering System",
    page_icon="📚",
    layout="wide"
)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "indexed_pdf_hash" not in st.session_state:
    st.session_state.indexed_pdf_hash = None

if "active_pdf_name" not in st.session_state:
    st.session_state.active_pdf_name = None

if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""

if "pdf_pages" not in st.session_state:
    st.session_state.pdf_pages = 0


# Application title
st.title("📚 PDF Question Answering System")

st.write(
    "Upload a PDF document and ask questions. "
    "Get answers using AI-powered semantic search."
)

st.divider()


# Sidebar
with st.sidebar:

    st.header("⚙️ Settings")

    st.write("**Language Model:** Llama 3.2")
    st.write("**Embedding Model:** nomic-embed-text")
    st.write("**Vector Database:** ChromaDB")

    st.divider()

    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()


# PDF upload section
st.subheader("1. Upload Your PDF")

uploaded_file = st.file_uploader(
    "Choose a PDF document",
    type=["pdf"]
)


if uploaded_file is not None:

    pdf_bytes = uploaded_file.getvalue()

    pdf_name = Path(uploaded_file.name).name

    pdf_hash = hashlib.sha256(pdf_bytes).hexdigest()

    # Process only when a new PDF is uploaded
    if st.session_state.indexed_pdf_hash != pdf_hash:

        st.session_state.active_pdf_name = None
        st.session_state.indexed_pdf_hash = None
        st.session_state.chat_history = []

        try:

            with st.spinner("Reading and processing PDF..."):

                pdf_reader = PdfReader(BytesIO(pdf_bytes))

                page_texts = [
                    page.extract_text() or ""
                    for page in pdf_reader.pages
                ]

                pdf_text = "\n\n".join(
                    f"PAGE {i + 1}\n{text}"
                    for i, text in enumerate(page_texts)
                )

                # Check extracted text
                if not any(text.strip() for text in page_texts):

                    st.warning(
                        "No selectable text found. "
                        "This PDF may contain scanned images."
                    )

                else:

                    # Split PDF into chunks
                    chunks, metadatas = split_pages_into_chunks(
                        page_texts,
                        pdf_name
                    )

                    if not chunks:
                        st.warning("No text chunks were created.")

                    else:

                        # Store uploaded PDF
                        upload_folder = Path("uploads")
                        upload_folder.mkdir(exist_ok=True)

                        file_path = upload_folder / pdf_name
                        file_path.write_bytes(pdf_bytes)

                        # Store chunks in ChromaDB
                        stored_count = store_chunks(
                            chunks,
                            metadatas
                        )

                        # Update session state
                        st.session_state.active_pdf_name = pdf_name
                        st.session_state.indexed_pdf_hash = pdf_hash
                        st.session_state.pdf_text = pdf_text
                        st.session_state.pdf_pages = len(pdf_reader.pages)

                        st.success("PDF processed successfully!")

                        st.write("**File name:**", pdf_name)
                        st.write(
                            "**Total pages:**",
                            len(pdf_reader.pages)
                        )
                        st.write(
                            "**Text chunks stored:**",
                            stored_count
                        )

        except Exception as e:

            st.error(f"PDF processing error: {e}")

    else:

        st.success("PDF is already processed and ready!")


# Display uploaded PDF information
if st.session_state.active_pdf_name:

    st.divider()

    st.subheader("📄 Uploaded PDF Details")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Total Pages",
            st.session_state.pdf_pages
        )

    with col2:
        st.write("**Document:**")
        st.write(st.session_state.active_pdf_name)

    with st.expander("View Extracted PDF Text"):

        st.text_area(
            "PDF Content",
            value=st.session_state.pdf_text,
            height=250,
            disabled=True
        )


    # Question-answering section
    st.divider()

    st.subheader("2. Ask Questions About Your PDF")

    with st.form("question_form"):

        question = st.text_input(
            "Enter your question:"
        )

        submitted = st.form_submit_button(
            "🔍 Get Answer"
        )

    if submitted:

        if not question.strip():

            st.warning("Please enter a question.")

        else:

            try:

                start_time = time.perf_counter()

                with st.spinner("Searching PDF and generating AI answer..."):

                    result = answer_question(
                        question,
                        source_name=st.session_state.active_pdf_name
                    )

                response_time = time.perf_counter() - start_time

                # Save conversation
                st.session_state.chat_history.append({
                    "question": question,
                    "answer": result["answer"],
                    "sources": result["sources"],
                    "response_time": response_time
                })

            except Exception as e:

                st.error(f"Question answering error: {e}")


    # Conversation history
    st.divider()

    st.subheader("3. Conversation History")

    if st.session_state.chat_history:

        for index, chat in enumerate(
            st.session_state.chat_history,
            start=1
        ):

            with st.chat_message("user"):
                st.write(chat["question"])

            with st.chat_message("assistant"):

                st.markdown(chat["answer"])

                st.caption(
                    f"Response time: "
                    f"{chat['response_time']:.2f} seconds"
                )

                if chat["sources"]:

                    source_pages = sorted({
                        item["page"]
                        for item in chat["sources"]
                    })

                    st.write(
                        "**Source PDF:**",
                        st.session_state.active_pdf_name
                    )

                    st.write(
                        "**Source pages:**",
                        ", ".join(map(str, source_pages))
                    )

                    with st.expander(
                        f"View Retrieved Chunks - Question {index}"
                    ):

                        for item in chat["sources"]:

                            st.markdown(
                                f"**Page {item['page']}**"
                            )

                            st.write(item["text"])

                            st.divider()

    else:

        st.info(
            "Your conversation history will appear here "
            "after you ask a question."
        )

else:

    st.info(
        "Please upload a PDF document to start "
        "asking questions."
    )
