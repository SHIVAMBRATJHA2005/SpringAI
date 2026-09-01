from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# 1. Load document
loader = PyPDFLoader("company_policy.pdf")
documents = loader.load()

# 2. Chunk document
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_documents(documents)

# 3. Create embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 4. Store vectors
vector_store = FAISS.from_documents(
    chunks,
    embeddings
)

# 5. Create retriever
retriever = vector_store.as_retriever(
    search_kwargs={"k": 4}
)

# 6. User question
question = "What is the work from home policy?"

# 7. Retrieve relevant chunks
docs = retriever.invoke(question)

# 8. Create context
context = "\n\n".join(
    doc.page_content for doc in docs
)

print(context)
def rag(question):

    # Retrieve
    docs = retriever.invoke(question)

    # Create context
    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    # Prompt
    prompt = f"""
    You are a helpful assistant.

    Use the following context to answer the question.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    # Send prompt to LLM
    response = llm.invoke(prompt)

    return response
answer = rag(
    "What is the work from home policy?"
)

print(answer)