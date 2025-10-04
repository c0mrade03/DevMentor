import streamlit as st
import time
import os
from ingest.chain_setup import load_rag_chain


def get_available_github_repos():
    vector_store_dir = "data/vector_stores"
    if not os.path.exists(vector_store_dir):
        return []
    available_repos = [i for i in os.listdir(
        vector_store_dir) if os.path.isdir(os.path.join(vector_store_dir, i))]
    return available_repos


# Configure the Streamlit page settings, such as title and layout.
st.set_page_config(
    page_title="DevMentor AI",
    page_icon="🤖",
    layout="wide"
)

# Display the main title of the application.
st.title("DevMentor: AI Software Architecture Assistant 🤖")

# Initialize a chat history list in the session state if it doesn't already exist.
if "messages" not in st.session_state:
    st.session_state.messages = []
if "active_repo" not in st.session_state:
    st.session_state.active_repo = None

github_repos = get_available_github_repos()

# Handle the "empty state" where no github repositories are present.
if not github_repos:
    st.warning("No knowledge bases found. Please add a repository first.")
    st.info(
        "You can add a new knowledge base by navigating to the "
        "'Add Repo' page from the sidebar."
    )
    st.stop()

# Create the dropdown menu for the user to select a knowledge base.
selected_repo = st.selectbox(
    "Select a Knowledge Base to Chat With:",
    options=github_repos
)

# Block for change detection and history reset
if st.session_state.active_repo != selected_repo:
    # If the selected repo has changed, we reset the chat
    st.session_state.messages = []
    # Update our tracker to the new selection
    st.session_state.active_repo = selected_repo
    
# Load the RAG chain once and cache it for performance using a spinner for user feedback.
with st.spinner("Loading AI model and vector store..."):
    rag_chain = load_rag_chain(selected_repo)

# Handle the case where the vector store might be missing or corrupted.
if not rag_chain:
    st.error(
        f"Failed to load the knowledge base for '{selected_repo}'. "
        "It may be corrupted or missing. Please try re-indexing it."
    )
    st.stop()

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
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response})
