import streamlit as st
import time
from ingest.chain_setup import load_rag_chain

# --- Block 1: Page Configuration ---
st.set_page_config(
    page_title="DevMentor AI",
    page_icon="🤖",
    layout="wide"
)

# --- Block 2: Title and Model Loading ---
st.title("DevMentor: AI Software Architecture Assistant 🤖")

with st.spinner("Loading AI model and vector store..."):
    rag_chain = load_rag_chain()

# --- Block 3: Initializing Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Block 4: Displaying Past Messages ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Block 5: Handling New User Input ---
if prompt := st.chat_input("Ask a question about the codebase..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Wrote this type of code so that UX feels more like chatgpt or gemini smooth typing effect
    placeholder = st.empty()
    full_response = ""
    for chunk in rag_chain.stream(prompt):
        for char in chunk:
            full_response += char
            placeholder.markdown(full_response + "▌")
            time.sleep(0.005)
    placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})