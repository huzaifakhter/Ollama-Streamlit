import streamlit as st
import ollama

MODEL = "smollm2:360m"

st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")
st.title("🤖 AI Chatbot with Ollama & Streamlit")
st.write("Chat with an AI model powered by Ollama!")

"""
Chat history
"""
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("How can i assist you today...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response_container = st.empty()
            message = ""

            for chunk in ollama.chat(model=MODEL, messages=st.session_state.messages, stream=True):
                message += chunk["message"]["content"]
                response_container.markdown(message + "▌")
            
            response_container.markdown(message)

    st.session_state.messages.append({"role": "assistant", "content": message})
