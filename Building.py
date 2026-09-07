import streamlit as st

from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate


st.title("🤖 Local GenAI Document Assistant")

llm = ChatOllama(
    model="llama3.2",
    temperature=0
)

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

vectorstore = Chroma(
    collection_name="documents",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 4}
)

prompt = ChatPromptTemplate.from_template("""
You are a helpful document assistant.

Use the following context to answer the question.

Context:
{context}

Question:
{question}

If the answer isn't present in the context,
say that you don't know.

Answer:
""")


question = st.chat_input("Ask a question about your documents")

if question:

    st.chat_message("user").write(question)

    docs = retriever.invoke(question)

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    messages = prompt.invoke({
        "context": context,
        "question": question
    })

    response = llm.invoke(messages)

    st.chat_message("assistant").write(
        response.content
    )
