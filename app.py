
import streamlit as st

from document_processor import (
    extract_pdf,
    extract_docx,
    extract_txt,
)

from rag_pipeline import (
    build_search_index,
    search_documents,
)

from llm_service import generate_answer


st.set_page_config(
    page_title="AI Enterprise Knowledge Copilot",
    page_icon="🤖",
    layout="wide",
)

st.title("AI Enterprise Knowledge Intelligence & Decision Copilot")

st.write(
    "Upload company documents and ask questions "
    "using AI-powered document search."
)

# Upload documents
uploaded_files = st.file_uploader(
    "Upload PDF, Word, or text documents",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True,
)

documents = []

if uploaded_files:
    for file in uploaded_files:
        try:
            if file.name.lower().endswith(".pdf"):
                text = extract_pdf(file)

            elif file.name.lower().endswith(".docx"):
                text = extract_docx(file)

            else:
                text = extract_txt(file)

            if text.strip():
                documents.append({
                    "filename": file.name,
                    "text": text,
                })

        except Exception as error:
            st.error(f"Could not process {file.name}: {error}")


# Prepare documents for search
if documents:

    with st.spinner("Preparing documents for search..."):
        index, chunks, metadata = build_search_index(documents)

    if index is not None:

        st.success(
            f"Successfully processed {len(documents)} document(s) "
            f"into {len(chunks)} searchable section(s)."
        )

        st.divider()
        st.subheader("Ask Your Documents")

        question = st.text_input(
            "Enter your question",
            placeholder="How many days of annual leave do employees get?",
        )

        if st.button("Generate AI Answer"):

            if question.strip():

                with st.spinner("Searching your documents..."):
                    results = search_documents(
                        question,
                        index,
                        chunks,
                        metadata,
                        top_k=3,
                    )

                if results:

                    st.subheader("AI-Generated Answer")

                    with st.spinner("Generating your answer..."):
                        answer = generate_answer(question, results)

                    st.write(answer)

                    st.divider()
                    st.subheader("Retrieved Sources")

                    for number, result in enumerate(results, start=1):
                        st.markdown(f"### Source {number}")
                        st.write(result["text"])
                        st.caption(f"Source: {result['filename']}")

                else:
                    st.warning("No relevant information was found.")

            else:
                st.warning("Please enter a question.")

else:
    st.info("Upload at least one document to start searching.")

