import os
import streamlit as st
import asyncio
from dotenv import load_dotenv

from streamlit_chat import message

from modules.chatbot import Chatbot
from modules.embedder import Embedder
from modules.sidebar import Sidebar


embeds = Embedder()

st.set_page_config(layout="wide", page_icon="💬", page_title="ChatBot-PDF")


def display_header():
    st.markdown(
        "<h1 style='text-align: center;'>ChatBot-PDF, Talk with your documents ! 💬</h1>", unsafe_allow_html=True
    )


def show_user_file(uploaded_file):
    file_container = st.expander("Your PDF file :")
    file_container.write(uploaded_file)


load_dotenv()
user_api_key = os.getenv("OPENAI_API_KEY")
if not user_api_key:
    user_api_key = st.sidebar.text_input(
        label="#### Your OpenAI API key 👇", placeholder="Paste your openAI API key, sk-", type="password"
    )
else:
    st.sidebar.success("API key loaded from .env", icon="🚀")


async def main():
    display_header()

    ############################
    if user_api_key == "":
        st.markdown(
            "<div style='text-align: center;'><h4>Enter your OpenAI API key to start chatting 😉</h4></div>",
            unsafe_allow_html=True,
        )
    else:
        os.environ["OPENAI_API_KEY"] = user_api_key

        ############################
        uploaded_file = st.sidebar.file_uploader("upload", type="pdf", label_visibility="collapsed")
        if uploaded_file is not None:
            show_user_file(uploaded_file)
        else:
            st.sidebar.info(
                "👆 Upload your PDF file to get started, "
                "sample for try : [file.pdf](https://github.com/gabacode/chatPDF/blob/main/file.pdf)"
            )
        ############################

        if uploaded_file:
            try:
                # Set up sidebar with various options
                with st.sidebar.expander("🛠️ Settings", expanded=False):
                    # Add a button to reset the chat history
                    if st.button("Reset Chat"):
                        st.session_state["reset_chat"] = True

                    # Allow the user to select a chatbot model to use
                    MODEL = st.selectbox(label="Model", options=["gpt-3.5-turbo"])

                    # Allow the user to change the model temperature
                    TEMPERATURE = st.slider(label="Temperature", min_value=0.0, max_value=1.0, value=0.618, step=0.01)

                # If the chat history has not yet been initialized, do so now
                if "history" not in st.session_state:
                    st.session_state["history"] = []

                # If the chatbot is not yet ready to chat, set the "ready" flag to False
                if "ready" not in st.session_state:
                    st.session_state["ready"] = False

                # If the "reset_chat" flag has not been set, set it to False
                if "reset_chat" not in st.session_state:
                    st.session_state["reset_chat"] = False

                    # If a PDF file has been uploaded
                if uploaded_file is not None:
                    # Display a spinner while processing the file
                    with st.spinner("Processing..."):
                        # Read the uploaded PDF file
                        uploaded_file.seek(0)
                        file = uploaded_file.read()
                        # Generate embeddings vectors for the file
                        vectors = await embeds.getDocEmbeds(file, uploaded_file.name)
                        # Use the Langchain ConversationalRetrievalChain to set up the chatbot
                        chatbot = Chatbot(MODEL, TEMPERATURE, vectors)
                    # Set the "ready" flag to True now that the chatbot is ready to chat
                    st.session_state["ready"] = True

                # If the chatbot is ready to chat
                if st.session_state["ready"]:
                    # If the chat history has not yet been initialized, initialize it now
                    if "generated" not in st.session_state:
                        st.session_state["generated"] = [
                            "Hello ! Ask me anything about the document " + uploaded_file.name + " 🤗"
                        ]

                    if "past" not in st.session_state:
                        st.session_state["past"] = ["Hey ! 👋"]

                    # Create a container for displaying the chat history
                    response_container = st.container()

                    # Create a container for the user's text input
                    container = st.container()

                    with container:
                        # Create a form for the user to enter their query
                        with st.form(key="my_form", clear_on_submit=True):
                            user_input = st.text_area(
                                "Query:",
                                placeholder="Talk about your data here (:",
                                key="input",
                                label_visibility="collapsed",
                            )
                            submit_button = st.form_submit_button(label="Send")

                            # If the "reset_chat" flag has been set, reset the chat history and generated messages
                            if st.session_state["reset_chat"]:
                                st.session_state["history"] = []
                                st.session_state["past"] = ["Hey ! 👋"]
                                st.session_state["generated"] = [
                                    "Hello ! Ask me anything about the document " + uploaded_file.name + " 🤗"
                                ]
                                response_container.empty()
                                st.session_state["reset_chat"] = False

                        # If the user has submitted a query
                        if submit_button and user_input:
                            # Add the user's input to the chat history
                            st.session_state["past"].append(user_input)

                            # Generate a response using the Langchain ConversationalRetrievalChain
                            output = await chatbot.conversational_chat(user_input)

                            # Add the user's chatbot's output to the chat history
                            st.session_state["generated"].append(output)

                    # If there are generated messages to display
                    if st.session_state["generated"]:
                        # Display the chat history
                        with response_container:
                            for i in range(len(st.session_state["generated"])):
                                message(
                                    st.session_state["past"][i],
                                    is_user=True,
                                    key=str(i) + "_user",
                                    avatar_style="big-smile",
                                )
                                message(st.session_state["generated"][i], key=str(i), avatar_style="thumbs")

            except Exception as e:
                st.error(f"Error: {str(e)}")

    sidebar = Sidebar()
    sidebar.show()


# Run the main function using asyncio
if __name__ == "__main__":
    asyncio.run(main())
