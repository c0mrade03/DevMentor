# This script can be used as CLI and also used for debugging
from ingest.logger import logger
from ingest.chain_setup import load_rag_chain


def main():
    """
    Main function to load the vector store, build a RAG chain with Gemini, and query it.
    """
    rag_chain = load_rag_chain()

    print("\n--- DevMentor AI Assistant ---")
    print("Ask questions about the codebase. Type 'quit' or 'exit' to end the session.")

    while True:
        # Ask a question and invoke the chain
        question = input("\nQuestion: ")
        if question.lower().strip() in ['quit', 'exit']:
            break
        logger.info(f"Invoking chain with question: '{question}'")
        answer = rag_chain.invoke(question)

        # Print the final answer
        print("\n--- Answer ---")
        print(answer)
        print("--------------\n")


if __name__ == "__main__":
    main()
