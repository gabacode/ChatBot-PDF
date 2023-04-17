import streamlit as st


class Sidebar:
    def __init__(self):
        pass

    def about(self):
        about = st.sidebar.expander("About 🤖")
        sections = [
            "#### ChatBot-PDF is an AI chatbot featuring conversational memory, designed to enable users to discuss their PDF data in a more intuitive manner. 📄",
            "#### This is a fork of [ChatBot-CSV](https://github.com/yvann-hub/ChatBot-CSV) by [yvann-hub](https://github.com/yvann-hub), many thanks to him for his work. 🤗",
            "#### It employs large language models to provide users with seamless, context-aware natural language interactions for a better understanding of their data. 🌐",
            "#### Powered by [Langchain](https://github.com/hwchase17/langchain), [OpenAI](https://platform.openai.com/docs/models/gpt-3-5) and [Streamlit](https://github.com/streamlit/streamlit) ⚡",
            "#### Source code : [gabacode/ChatBot-PDF](https://github.com/gabacode/ChatBot-PDF)",
        ]
        for section in sections:
            about.write(section)

    def show(self):
        self.about()
