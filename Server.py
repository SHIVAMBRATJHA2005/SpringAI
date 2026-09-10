from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langserve import add_routes
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY is missing. Add it to your .env file or environment.")

model = ChatGroq(api_key=groq_api_key, model="gemma2-9b-it", temperature=0.7)

system_template = "translate the following into {language}:"
prompt = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("human", "{text}"),
])

parser = StrOutputParser()
chain = prompt | model | parser

app = FastAPI(title="LangServe Groq Example", description="LangServe Groq Example", version="0.1.0")
add_routes(app, chain, path="/chain")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)