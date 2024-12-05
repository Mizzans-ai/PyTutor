import streamlit as st
from langchain_ollama import OllamaLLM
import os
import time

# Initialize the Ollama Llama 3.2 model
llama = OllamaLLM(model='llama3.2')

# Define the chatbot function
def get_python_answer(prompt):
    prompt = f"Answer this Python-related query in a professional manner, suitable for a Python tutor: (prompt)"
    response = llama.generate(prompt)
    return response

# Streamlit app setup
def chatbot_interface():
    st.title("Python Tutor Chatbot")
    st.markdown("""
        This is a chatbot that answers Python programming questions, from beginner to advanced topics. 
        Ask your Python-related questions!
    """)

    # Generate a unique key using a combination of session state and timestamp
    unique_key = f"python_question_input_{int(time.time())}"

    # Input box for user question with a unique key
    user_query = st.text_input("Ask a Python-related question:", key=unique_key)

    # Display the answer when the user submits a question
    if user_query:
        with st.spinner('Thinking...'):
            answer = get_python_answer(user_query)
            st.subheader("Answer:")
            st.write(answer)

        # Store chat history
        if "history" not in st.session_state:
            st.session_state.history = []
        st.session_state.history.append(("You", user_query))
        st.session_state.history.append(("Bot", answer))

    # Display chat history
    if "history" in st.session_state:
        for speaker, message in st.session_state.history:
            if speaker == "You":
                st.markdown(f"**You**: {message}")
            else:
                st.markdown(f"**Bot**: {message}")

if __name__ == "__main__":
    chatbot_interface()
