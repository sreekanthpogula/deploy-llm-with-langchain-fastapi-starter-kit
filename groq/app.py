import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
import time


from dotenv import load_dotenv
load_dotenv()

# Set up the Groq API key
groq_api_key = os.environ['GROQ_API_KEY']
if not groq_api_key:
    st.error("GROQ_API_KEY is not set in the environment variables.")

if "vectorstore" not in st.session_state:
    st.session_state.embeddings = OllamaEmbeddings(model="llama2")
    st.session_state.loader = WebBaseLoader("https://python.langchain.com/")
    st.session_state.documents = st.session_state.loader.load()
    st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.documents)
    st.session_state.vectorstore = FAISS.from_documents(st.session_state.final_documents, st.session_state.embeddings)

st.title("Groq Chatbot with LangChain Data")

# Initialize the Groq chat model
llm = ChatGroq(
    model="gemma2-9b-It",
    api_key=groq_api_key
)

prompt= ChatPromptTemplate.from_template(
    "You are a helpful assistant. Answer the question based on the provided context on LangChain.\n\n"
    "{context}\n\n"
    "Question: {input}\n\n"
)

document_chain = create_stuff_documents_chain(
    llm=llm,
    prompt=prompt,
)
retriver = st.session_state.vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5}
)
retrival_chain = create_retrieval_chain(
    retriever=retriver,
    combine_docs_chain=document_chain,
)

prompt = st.text_input("Enter your question:", "")

if prompt:
    start= time.process_time()
    st.write("Processing your request...")
    response = retrival_chain.invoke({"input": prompt})
    st.write("Response:", response['answer'])
    end = time.process_time()
    st.write(f"Processing time: {end - start:.2f} sec")