import streamlit as st
import time
from ingest.chain_setup import load_rag_chain

# Configure the Streamlit page settings, such as title and layout.
st.set_page_config(
    page_title="DevMentor AI",
    page_icon="🤖",
    layout="wide"
)

# Display the main title of the application.
st.title("DevMentor: AI Software Architecture Assistant 🤖")

# Load the RAG chain once and cache it for performance using a spinner for user feedback.
with st.spinner("Loading AI model and vector store..."):
    rag_chain = load_rag_chain()

# Initialize a chat history list in the session state if it doesn't already exist.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the past messages from the chat history on each script rerun.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle new user input from the chat box at the bottom of the screen.
if prompt := st.chat_input("Ask a question about the codebase..."):
    
    # Add the user's new message to the chat history and display it on the screen.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Stream the assistant's response to create a smooth, character-by-character typing effect.
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        for chunk in rag_chain.stream(prompt):
            for char in chunk:
                full_response += char
                placeholder.markdown(full_response + "▌")
                time.sleep(0.005)
        # After the stream is complete, display the final response without the cursor.
        placeholder.markdown(full_response)

    # Add the final, complete assistant's response to the chat history.
    st.session_state.messages.append({"role": "assistant", "content": full_response})
