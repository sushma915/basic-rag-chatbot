import streamlit as st
import tempfile

from rag_pipeline import (
    process_pdf,
    create_rag_chain
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="📚",
    layout="wide"
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "retriever" not in st.session_state:
    st.session_state.retriever = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pdf_name" not in st.session_state:
    st.session_state.pdf_name = None


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.title("📚 RAG Chatbot")

    st.markdown(
        "Upload a PDF and ask questions based on its content."
    )

    st.divider()

    uploaded_file = st.file_uploader(
        "📄 Upload your PDF",
        type=["pdf"]
    )

    if uploaded_file:

        st.info(
            f"📎 {uploaded_file.name}"
        )

        if st.button(
            "⚙️ Process PDF",
            use_container_width=True
        ):

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            ) as temp_file:

                temp_file.write(
                    uploaded_file.getvalue()
                )

                pdf_path = temp_file.name


            with st.spinner(
                "Processing your document..."
            ):

                retriever = process_pdf(
                    pdf_path
                )

                st.session_state.retriever = retriever

                st.session_state.pdf_name = (
                    uploaded_file.name
                )

                st.session_state.messages = []


            st.success(
                "✅ PDF processed successfully!"
            )

    st.divider()

    if st.session_state.retriever:

        st.success(
            f"📄 Active document: "
            f"{st.session_state.pdf_name}"
        )

        if st.button(
            "🗑️ Clear Chat",
            use_container_width=True
        ):

            st.session_state.messages = []

            st.rerun()


# --------------------------------------------------
# MAIN PAGE
# --------------------------------------------------

st.title("📚 Basic RAG Chatbot")

st.markdown(
    "Ask questions and get answers based on your uploaded PDF."
)


# --------------------------------------------------
# WELCOME MESSAGE
# --------------------------------------------------

if not st.session_state.retriever:

    st.info(
        "👈 Upload a PDF from the sidebar to get started."
    )

    st.markdown(
        """
        ### How it works

        1. 📄 Upload a PDF
        2. ⚙️ Process the document
        3. 💬 Ask questions
        4. 🤖 Get answers from your document
        """
    )


# --------------------------------------------------
# DISPLAY CHAT HISTORY
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# --------------------------------------------------
# CHAT INPUT
# --------------------------------------------------

if st.session_state.retriever:

    question = st.chat_input(
        "Ask a question about your PDF..."
    )


    if question:

        # Display user message
        with st.chat_message("user"):

            st.markdown(
                question
            )


        # Save user message
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )


        # Create RAG chain
        rag_chain = create_rag_chain(
            st.session_state.retriever
        )


        # Generate answer
        with st.chat_message("assistant"):

            with st.spinner(
                "Searching the document..."
            ):

                answer = rag_chain.invoke(
                    question
                )


            st.markdown(
                answer
            )


        # Save assistant message
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )