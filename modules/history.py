import os
import streamlit as st


class History:
    def __init__(self):
        self.history = st.session_state.get("history", [])
        st.session_state["history"] = self.history

    def init(self, uploaded_file):
        if "generated" not in st.session_state:
            st.session_state["generated"] = ["Hello ! Ask me anything about " + uploaded_file.name + " 🤗"]
        if "past" not in st.session_state:
            st.session_state["past"] = ["Hey ! 👋"]

    def reset(self, uploaded_file):
        st.session_state["history"] = []
        st.session_state["past"] = ["Hey ! 👋"]
        st.session_state["generated"] = ["Hello ! Ask me anything about " + uploaded_file.name + " 🤗"]
        st.session_state["reset_chat"] = False

    def append(self, user_input, output):
        st.session_state["past"].append(user_input)
        st.session_state["generated"].append(output)

    def load(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, "r") as f:
                self.history = f.read().splitlines()

    def save(self):
        with open(self.history_file, "w") as f:
            f.write("\n".join(self.history))
