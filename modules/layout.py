import streamlit as st


class Layout:

    def display_header(self):
        st.markdown(
            "<h1 style='text-align: center;'>ChatBot-PDF, Talk with your documents ! 💬</h1>", unsafe_allow_html=True
        )

    def show_api_key_error(self):
        st.markdown(
            "<div style='text-align: center;'><h4>Enter your OpenAI API key to start chatting 😉</h4></div>",
            unsafe_allow_html=True,
        )
