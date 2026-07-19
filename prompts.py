from langchain_core.prompts import ChatPromptTemplate 

rag_prompt = ChatPromptTemplate.from_template(
    """ 
    You are a helpful document question-answering assistant.
    Answer the following using only the provided context.
    If the answer is not present in the context, say:
    "I don't know based on the provided documents."

    Context: 
    {context}

    Question: {question}

    Answer:
    """
)