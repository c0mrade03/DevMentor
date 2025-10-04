import streamlit as st
import subprocess
import sys
import os
import shutil

# Page Configuration and Title
st.set_page_config(page_title="Add Repository", page_icon="➕")
st.title("Add a New Knowledge Base 🧠")
st.info(
    "Paste a public GitHub repository URL below to download, process, and "
    "index it into a new vector store."
)

# Initialize Session State
# Initialize our flag at the start. This runs only once.
if "confirm_overwrite" not in st.session_state:
    st.session_state.confirm_overwrite = False
if "repo_to_overwrite" not in st.session_state:
    st.session_state.repo_to_overwrite = None
if "url_to_clone" not in st.session_state:
    st.session_state.url_to_clone = None

# Helper Function for the Ingestion Process
# Put the subprocess logic in a function to avoid repeating code.
def start_ingestion(github_url):
    st.success(f"Starting ingestion for {github_url}. This may take several minutes...")
    log_placeholder = st.empty()
    log_output = ""
    command = [sys.executable, "-m", "ingest.create_vectorstore", "--url", github_url]

    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            bufsize=1,
        )
        for line in process.stdout:
            log_output += line
            log_placeholder.code(log_output, language="log")
        process.wait()
        if process.returncode == 0:
            st.success("✅ Ingestion complete! The new knowledge base is ready.")
            st.balloons()
        else:
            st.error(
                "❌ Ingestion failed. See logs above for details. "
                f"Exit code: {process.returncode}"
            )
    except Exception as e:
        st.error(f"An error occurred while launching the script: {e}")

# Main UI Logic
github_url = st.text_input("Public GitHub Repository URL:")

if st.button("Download and Index Repository"):
    if github_url:
        # Calculate the path where the repo would be cloned.
        storage_dir = "data/github_repos"
        repo_name = github_url.split("/")[-1].replace(".git", "")
        clone_path = os.path.join(storage_dir, repo_name)

        # Check if the directory already exists.
        if os.path.exists(clone_path):
            # If it exists, DON'T delete. Instead, set our flag and save the path.
            st.session_state.confirm_overwrite = True
            st.session_state.repo_to_overwrite = clone_path
            st.session_state.url_to_clone = github_url
        else:
            # If it doesn't exist, start the ingestion process immediately.
            start_ingestion(github_url)
    else:
        st.warning("Please enter a GitHub URL.")

# Confirmation UI Block
# This block of code only runs if our confirmation flag is True.
if st.session_state.confirm_overwrite:
    st.warning(
        f"Repository already exists at: `{st.session_state.repo_to_overwrite}`"
        "\n\nDo you want to delete the existing folder and re-index it?"
    )

    # Create two columns for the Yes/No buttons.
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Yes, Overwrite"):
            # If user says yes, perform the deletion and start ingestion.
            st.info(f"Deleting existing repository...")
            shutil.rmtree(st.session_state.repo_to_overwrite)
            
            # Start the ingestion process.
            start_ingestion(st.session_state.url_to_clone)

            # Reset the flags to exit the confirmation state.
            st.session_state.confirm_overwrite = False
            st.session_state.repo_to_overwrite = None
            st.session_state.url_to_clone = None
            # Rerun to clean up the UI.
            st.rerun()

    with col2:
        if st.button("No, Cancel"):
            # If user says no, just reset the flags and show a message.
            st.info("Operation cancelled.")
            st.session_state.confirm_overwrite = False
            st.session_state.repo_to_overwrite = None
            st.session_state.url_to_clone = None
            # We force a rerun to clean up the UI.
            st.rerun()