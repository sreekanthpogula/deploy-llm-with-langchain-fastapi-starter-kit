import requests
import streamlit as st

# Function to send a GET request to the chatbot API
def get_openai_response(question):
    url = "http://localhost:8000/chat/openai"
    json_data = {"question": question}
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=json_data, headers=headers)
    if response.status_code == 200:
        return response.json()['output']
    else:
        return f"Error: {response.status_code} - {response.text}"


# Function to send a GET request to the Ollama chatbot API
def get_ollama_response(question):
    url = "http://localhost:8000/chat/ollama"
    json_data = {"question": question}
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=json_data, headers=headers)

    if response.status_code == 200:
        return response.json()['output']
    else:
        return f"Error: {response.status_code} - {response.text}"


# Streamlit app configuration
st.title("LLM Chatbot API Demo with OpenAI and Ollama")

# Input text for the question
input_text1 = st.text_input("Enter your question for OpenAI:", "")

# Display instructions
st.info("Click the buttons below to get responses from the respective chatbots.")

# Buttons to get responses from OpenAI and Ollama
if st.button("Get OpenAI Response"):
    if input_text1:
        with st.spinner("Getting response from OpenAI..."):
            response = get_openai_response(input_text1)
            st.success(f"OpenAI Response: {response}")
    else:
        st.error("Please enter a question.")

# Input text for the question
input_text2 = st.text_input("Enter your question for Ollama:", "")

# Display instructions
st.info("Click the buttons below to get responses from the respective chatbots.")

# Button to get response from Ollama
if st.button("Get Ollama Response"):
    if input_text2:
        with st.spinner("Getting response from Ollama..."):
            response = get_ollama_response(input_text2)
            st.success(f"Ollama Response: {response}")
    else:
        st.error("Please enter a question.")
