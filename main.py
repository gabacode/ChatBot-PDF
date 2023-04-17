import os
import streamlit as st
import asyncio
from dotenv import load_dotenv

from streamlit_chat import message

from modules.chatbot import Chatbot
from modules.embedder import Embedder
from modules.sidebar import Sidebar


load_dotenv()

st.set_page_config(layout="wide", page_icon="💬", page_title="ChatBot-PDF")

# Display the header of the app
def display_header():
    st.markdown(
        "<h1 style='text-align: center;'>ChatBot-PDF, Talk with your documents ! 💬</h1>", unsafe_allow_html=True
    )


# Load the OpenAI API key from the .env file or from the user's input
def load_api_key():
    user_api_key = os.getenv("OPENAI_API_KEY")
    if not user_api_key:
        user_api_key = st.sidebar.text_input(
            label="#### Your OpenAI API key 👇", placeholder="Paste your openAI API key, sk-", type="password"
        )
    else:
        st.sidebar.success("API key loaded from .env", icon="🚀")
    return user_api_key


# Handle the file upload and display the uploaded file
def handle_upload():
    uploaded_file = st.sidebar.file_uploader("upload", type="pdf", label_visibility="collapsed")
    if uploaded_file is not None:
        file_container = st.expander("Your PDF file :")
        file_container.write(uploaded_file)
    else:
        st.sidebar.info(
            "👆 Upload your PDF file to get started, "
            "sample for try : [file.pdf](https://github.com/gabacode/chatPDF/blob/main/file.pdf)"
        )
    return uploaded_file


# Set up the chatbot with the uploaded file, model, and temperature
async def setup_chatbot(uploaded_file, model, temperature):
    embeds = Embedder()
    with st.spinner("Processing..."):
        uploaded_file.seek(0)
        file = uploaded_file.read()
        vectors = await embeds.getDocEmbeds(file, uploaded_file.name)
        chatbot = Chatbot(model, temperature, vectors)
    st.session_state["ready"] = True
    return chatbot


# Create the sidebar with various options
def show_sidebar_options():
    with st.sidebar.expander("🛠️ Settings", expanded=False):
        if st.button("Reset Chat"):
            st.session_state["reset_chat"] = True
        st.session_state.setdefault("reset_chat", False)
        st.session_state.setdefault("model", "gpt-3.5-turbo")
        st.session_state.setdefault("temperature", 0.618)
        model = st.selectbox(label="Model", options=["gpt-3.5-turbo"])
        temperature = st.slider(label="Temperature", min_value=0.0, max_value=1.0, value=0.618, step=0.01)
        st.session_state["model"] = model
        st.session_state["temperature"] = temperature


def reset_chat_history(uploaded_file):
    st.session_state["history"] = []
    st.session_state["past"] = ["Hey ! 👋"]
    st.session_state["generated"] = ["Hello ! Ask me anything about " + uploaded_file.name + " 🤗"]
    st.session_state["reset_chat"] = False


def initialize_chat_history(uploaded_file):
    if "generated" not in st.session_state:
        st.session_state["generated"] = ["Hello ! Ask me anything about " + uploaded_file.name + " 🤗"]
    if "past" not in st.session_state:
        st.session_state["past"] = ["Hey ! 👋"]


def add_to_chat_history(user_input, output):
    st.session_state["past"].append(user_input)
    st.session_state["generated"].append(output)


def show_api_key_error():
    st.markdown(
        "<div style='text-align: center;'><h4>Enter your OpenAI API key to start chatting 😉</h4></div>",
        unsafe_allow_html=True,
    )


async def main():
    display_header()
    user_api_key = load_api_key()

    if user_api_key == "":
        show_api_key_error()
    else:
        os.environ["OPENAI_API_KEY"] = user_api_key
        uploaded_file = handle_upload()

        if uploaded_file is not None:
            chat_history = st.session_state.get("history", [])
            st.session_state["history"] = chat_history

            show_sidebar_options()

            try:
                chatbot = await setup_chatbot(uploaded_file, st.session_state["model"], st.session_state["temperature"])
                st.session_state["chatbot"] = chatbot

                ### STARTS ###
                if st.session_state["ready"]:
                    # Create a containers for displaying the chat history
                    response_container = st.container()
                    container = st.container()

                    with container:
                        with st.form(key="my_form", clear_on_submit=True):
                            user_input = st.text_area(
                                "Query:",
                                placeholder="Talk about your data here (:",
                                key="input",
                                label_visibility="collapsed",
                            )
                            submit_button = st.form_submit_button(label="Send")

                        if st.session_state["reset_chat"]:
                            reset_chat_history(uploaded_file)
                        initialize_chat_history(uploaded_file)

                        # If the user has submitted a query
                        if submit_button and user_input:
                            output = await st.session_state["chatbot"].conversational_chat(user_input)
                            add_to_chat_history(user_input, output)

                    # If there are generated messages to display
                    if st.session_state["generated"]:
                        with response_container:
                            for i in range(len(st.session_state["generated"])):
                                message(
                                    st.session_state["past"][i],
                                    is_user=True,
                                    key=f"{i}_user",
                                    avatar_style="big-smile",
                                )
                                message(st.session_state["generated"][i], key=str(i), avatar_style="thumbs")

            except Exception as e:
                st.error(f"Error: {str(e)}")

    Sidebar().show()


# Run the main function using asyncio
if __name__ == "__main__":
    asyncio.run(main())
