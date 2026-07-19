from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser

from prompts import rag_prompt


load_dotenv()


# Create LLM
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)


def process_pdf(pdf_path):

    # Load PDF
    loader = PyPDFLoader(pdf_path)

    documents = loader.load()


    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_documents(documents)


    # Create embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


    # Create vector store
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings
    )


    # Create retriever
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 3}
    )


    return retriever


def format_docs(docs):

    return "\n\n".join(
        doc.page_content
        for doc in docs
    )


def create_rag_chain(retriever):

    rag_chain = (
        {
            "context": retriever | format_docs,
            "question": lambda x: x
        }
        | rag_prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain