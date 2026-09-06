# =========================
# INSTALLATION
# =========================
# pip install langchain langchain-community langchain-ollama
# pip install langchain-chroma chromadb beautifulsoup4 streamlit


# =========================
# IMPORTS
# =========================

from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma

from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain


# =========================
# 1. DATA INGESTION
# =========================

url = "https://smith.langchain.com/o/c9dbcba6-e4c1-4f93-8e9d-dcb65472d026"

loader = WebBaseLoader(url)

loaded_documents = loader.load()

print("Documents loaded:", len(loaded_documents))


# =========================
# 2. TEXT SPLITTING
# =========================

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

splits = text_splitter.split_documents(loaded_documents)

print("Number of chunks:", len(splits))


# =========================
# 3. CREATE EMBEDDINGS
# =========================

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)


# =========================
# 4. STORE EMBEDDINGS
# =========================

vector_store = Chroma.from_documents(
    documents=splits,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

print("Vector database created.")


# =========================
# 5. CREATE RETRIEVER
# =========================

retriever = vector_store.as_retriever(
    search_kwargs={"k": 4}
)


# =========================
# 6. LLM
# =========================

llm = ChatOllama(
    model="llama3.2",
    temperature=0
)


# =========================
# 7. PROMPT
# =========================

prompt = ChatPromptTemplate.from_template(
    """
    Answer the following question using only the context provided.

    If the answer is not present in the context, say:
    "I don't know based on the provided documents."

    <context>
    {context}
    </context>

    Question:
    {input}

    Answer:
    """
)


# =========================
# 8. DOCUMENT CHAIN
# =========================

documents_chain = create_stuff_documents_chain(
    llm=llm,
    prompt=prompt
)


# =========================
# 9. RETRIEVAL CHAIN
# =========================

rag_chain = create_retrieval_chain(
    retriever,
    documents_chain
)


# =========================
# 10. ASK QUESTION
# =========================

query = "LangSmith has two usage?"

response = rag_chain.invoke({
    "input": query
})


# =========================
# 11. PRINT ANSWER
# =========================

print("\nQUESTION:")
print(query)

print("\nANSWER:")
print(response["answer"])




print("\nRETRIEVED CONTEXT:")

for i, doc in enumerate(response["context"]):
    print(f"\n--- Document {i + 1} ---")
    print(doc.page_content)