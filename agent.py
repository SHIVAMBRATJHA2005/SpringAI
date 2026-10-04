from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_ollama import ChatOllama
from langchain.agents import create_agent


# -------------------------
# Database
# -------------------------

db = SQLDatabase.from_uri(
    "sqlite:///students.db"
)


# -------------------------
# LLM
# -------------------------

llm = ChatOllama(
    model="llama3.2",
    temperature=0
)


# -------------------------
# SQL Toolkit
# -------------------------

toolkit = SQLDatabaseToolkit(
    db=db,
    llm=llm
)

tools = toolkit.get_tools()


# -------------------------
# Agent
# -------------------------

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="""
You are a SQL database assistant.

You have access to a student database.

Rules:

1. Use SQL tools to answer database questions.
2. Never guess database results.
3. Always inspect the database schema when necessary.
4. Generate valid SQL.
5. Only perform read-only SQL operations.
6. Explain the final result clearly.
"""
)


# -------------------------
# Ask Question
# -------------------------

question = "Which student has the highest CGPA?"

response = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": question
        }
    ]
})

print(response)