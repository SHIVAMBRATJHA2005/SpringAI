from rank_bm25 import BM25Okapi
from langchain_text_splitters import RecursiveCharacterTextSplitter


# -----------------------------
# 1. Documents
# -----------------------------

documents = [
    """
    LangGraph is a framework for building stateful applications
    with large language models. It allows developers to create
    graphs containing nodes and edges.
    """,

    """
    LangChain provides abstractions for working with language
    models, prompts, tools, agents and retrieval systems.
    """,

    """
    RAG stands for Retrieval Augmented Generation.
    It retrieves relevant information from external knowledge
    before sending the context to an LLM.
    """,

    """
    PostgreSQL is a relational database commonly used for
    storing structured application data.
    """
]


# -----------------------------
# 2. Chunk documents
# -----------------------------

splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=30
)

chunks = []

for document in documents:
    chunks.extend(splitter.split_text(document))


print("Chunks:")
for i, chunk in enumerate(chunks):
    print(i, chunk)


# -----------------------------
# 3. Build BM25 index
# -----------------------------

tokenized_chunks = [
    chunk.lower().split()
    for chunk in chunks
]

bm25 = BM25Okapi(tokenized_chunks)


# -----------------------------
# 4. Retrieve relevant chunks
# -----------------------------

def retrieve(query, k=3):

    query_tokens = query.lower().split()

    scores = bm25.get_scores(query_tokens)

    ranked_indexes = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True
    )

    return [
        chunks[i]
        for i in ranked_indexes[:k]
    ]


# -----------------------------
# 5. Test retrieval
# -----------------------------

query = "How does LangGraph work?"

results = retrieve(query)

print("\nRetrieved Context:")

for result in results:
    print("----------------")
    print(result)
    from openai import OpenAI

client = OpenAI()


def vectorless_rag(query):

    # Retrieve
    results = retrieve(query, k=3)

    context = "\n\n".join(results)

    prompt = f"""
You are a helpful AI assistant.

Answer the question using ONLY the provided context.

Context:
{context}

Question:
{query}

If the answer is not present in the context,
say "I don't know based on the provided documents."
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


answer = vectorless_rag(
    "What is LangGraph?"
)

print(answer)