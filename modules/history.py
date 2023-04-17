import os
import streamlit as st


class ChatHistory:
    def __init__(self):
        self.history = st.session_state.get("history", [])
        st.session_state["history"] = self.history

    def default_greeting(self):
        return "Hey ! 👋"

    def default_prompt(self, thingy, topic):
        return f"Hello! Ask me anything about the {thingy} {topic} 🤗"

    def initialize_past(self):
        st.session_state["past"] = [self.default_greeting()]

    def initialize_generated(self, uploaded_file):
        st.session_state["generated"] = [self.default_prompt("document", uploaded_file.name)]

    def initialize(self, uploaded_file):
        if "generated" not in st.session_state:
            self.initialize_generated(uploaded_file)
        if "past" not in st.session_state:
            self.initialize_past()

    def reset(self, uploaded_file):
        st.session_state["history"] = []
        self.initialize_past()
        self.initialize_generated(uploaded_file)
        st.session_state["reset_chat"] = False

    def append(self, mode, message):
        st.session_state[mode].append(message)

    def load(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, "r") as f:
                self.history = f.read().splitlines()

    def save(self):
        with open(self.history_file, "w") as f:
            f.write("\n".join(self.history))
