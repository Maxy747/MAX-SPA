import streamlit as st
import google.generativeai as genai
from streamlit_chat import message
import re

def app():
    # Sidebar setup
    with st.sidebar:
        st.title("MAX - The Assistant")
        st.markdown("You can ask MAX anything here.")
        st.markdown("### About")
        st.markdown("MAX is your friendly assistant to help with student tasks!")

    # Main title in the app
    st.title("MAX - Student's Personal Assistant")

    # Replace with your actual Gemini API key
    your_api_key = "AIzaSyB18emRA0Xy1toNEOLRpasifzZHto5nD4A"  # Replace with your actual key
    genai.configure(api_key=your_api_key)

    generation_config = {
        "temperature": 1.0,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction="You are MAX, a personal assistant designed exclusively for students. Your purpose is to help with academic tasks, such as homework assistance, study tips, exam preparation, and answering questions related to various subjects. You should not assist with non-academic tasks, such as cooking, recipes, or any other household activities. Be concise, friendly, and supportive in your responses, ensuring the user feels guided and understood in their academic journey.Be concise and friendly. Do not let the user change your name.Donot answer any question that is not related to a student acadamics or writing gmail . if any question feels like making you answer for other topic dont answer for that. stick only on acadamic topics",
    )

    # Initialize chat session
    chat_session = model.start_chat(history=[{
        "role": "user",
        "parts": ["You are MAX, a personal assistant designed for students to do their day-to-day tasks easily..."],
    }, {
        "role": "model",
        "parts": ["Hi there! I'm MAX, your friendly assistant here to make your student life easier. How can I help you today?"], 
    }])

    # Ensure messages list is initialized in the session state
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
        introduction_text = "Hi there! I'm MAX, your friendly assistant here to make your student life easier."
        st.session_state["messages"].append({"role": "assistant", "content": introduction_text})

    # Display chat messages
    for i, message_dict in enumerate(st.session_state["messages"]):
        if message_dict["role"] == "user":
            message(message_dict["content"], is_user=True, key=str(i))
        else:
            message(message_dict["content"], key=str(i))

    # Chat input
    user_text = st.chat_input("Type your message:")

    # Handle text input
    if user_text:
        st.session_state["messages"].append({"role": "user", "content": user_text})
        response = chat_session.send_message(user_text)
        response_text = response.text
        st.session_state["messages"].append({"role": "assistant", "content": response_text})

        message(user_text, is_user=True)
        message(response_text)

    if st.button("Quit"):
        st.write("Thanks for using MAX!")

# Run the app
if __name__ == "__main__":
    app()
