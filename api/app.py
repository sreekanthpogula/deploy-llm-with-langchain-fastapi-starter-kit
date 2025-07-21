from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langserve import add_routes
import uvicorn
from dotenv import load_dotenv
import os
from langchain_community.llms import ollama

# Load environment variables from .env file
load_dotenv()

# Set the OpenAI API key if available
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Enable LangChain tracing
os.environ["LANGCHAIN_TRACING_V2"] = "true"

# Set the LangChain API key if available
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")


# Create FastAPI app
app = FastAPI(
    title="LLM Chatbot API",
    description="An API for a chatbot powered by LangChain and OpenAI.",
    version="1.0.0",
)

add_routes( 
    app,
    ChatOpenAI(),
    path="/chat",
)

# Define the OpenAI chat model
llm1 = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

# OpenAI chat model
llm2 = ollama.Ollama(model="gemma3", temperature=0.7)


# Prompt template
chat_prompt1 = ChatPromptTemplate.from_messages([
    ("system", "Welcome to the LLM Chatbot API!"),
    ("human", "Question: {question}"),
])

chat_prompt2 = ChatPromptTemplate.from_messages([
    ("system", "Welcome to the LLM Chatbot API with Ollama!"),
    ("human", "Question: {question}"),
])

add_routes(
    app,
    llm1| chat_prompt1,
    path="/chat/openai",
)

add_routes(
    app,
    llm2| chat_prompt2,
    path="/chat/gemma3",
)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)

# This FastAPI application serves as a chatbot API using LangChain and OpenAI.
# It provides endpoints for interacting with both OpenAI and Ollama chat models.
# The application uses LangChain to create a chat prompt template and integrates with OpenAI and Ollama.
# To run the FastAPI app, use the command:
# uvicorn api.app:app --reload
# This will start the server at http://localhost:8000
# You can access the API documentation at http://localhost:8000/docs
# You can test the chatbot API by sending POST requests to the /chat endpoint with a JSON body containing the "question" field.
# Example request:
# {
#     "question": "What is the capital of France?"
# }
# Example response:
# {
#     "response": "The capital of France is Paris."
# }
# You can also test the OpenAI and Ollama chat models by sending requests to the /chat/openai and /chat/ollama endpoints respectively.
# Example request for OpenAI:
# {
#     "question": "What is the capital of France?"
# }
# Example response for OpenAI:
# {
#     "response": "The capital of France is Paris."
# }
# Example request for Ollama:
# {
#     "question": "What is the capital of France?"
# }
# Example response for Ollama:
# {
#     "response": "The capital of France is Paris."
# }