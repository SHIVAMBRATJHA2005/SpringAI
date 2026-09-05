from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

# Embedding model
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

# Load existing vector database
vector_store = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)

# Create retriever
retriever = vector_store.as_retriever(
    search_kwargs={"k": 4}
)

# LLM
llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)

# Prompt
prompt = ChatPromptTemplate.from_template("""
You are a helpful document assistant.

Answer the question using ONLY the provided context.

If the answer is not present in the context,
say "I don't know based on the provided documents."

Context:
{context}

Question:
{question}

Answer:
""")

print("RAG Chatbot started.")
print("Type 'exit' to stop.\n")

while True:

    question = input("You: ")

    if question.lower() == "exit":
        print("Goodbye!")
        break

    # Retrieve relevant chunks
    documents = retriever.invoke(question)

    # Combine retrieved documents
    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    # Create prompt
    messages = prompt.invoke({
        "context": context,
        "question": question
    })

    # Generate answer
    response = llm.invoke(messages)

    print("\nBot:", response.content)

    # Show sources
    print("\nSources:")

    for document in documents:
        print(
            f"- Page {document.metadata.get('page', 'unknown') + 1}"
        )

    print()