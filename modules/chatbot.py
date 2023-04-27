import streamlit as st
from langchain.chains import RetrievalQA
from langchain.llms import HuggingFacePipeline
from transformers import (
    pipeline,
    AutoModelForCausalLM,
    AutoTokenizer,
)

import torch


class Chatbot:
    def __init__(self, model_name, temperature, vectors):
        self.model_name = model_name
        self.temperature = temperature
        self.vectors = vectors

    async def conversational_chat(self, query):
        """
        Starts a conversational chat with a model via Langchain
        """

        tokenizer = AutoTokenizer.from_pretrained("databricks/dolly-v2-3b", padding_side="left")
        base_model = AutoModelForCausalLM.from_pretrained(
            "databricks/dolly-v2-3b", device_map="auto", torch_dtype=torch.float16
        )

        pipe = pipeline(
            "text-generation",
            model=base_model,
            tokenizer=tokenizer,
            max_length=1024,
            temperature=0.6,
            pad_token_id=tokenizer.eos_token_id,
            top_p=0.95,
            repetition_penalty=1.2,
            model_kwargs={"load_in_8bit": True},
        )
        local_llm = HuggingFacePipeline(pipeline=pipe)

        qa = RetrievalQA.from_chain_type(llm=local_llm, chain_type="stuff", retriever=self.vectors.as_retriever())

        result = qa({"query": query})

        st.session_state["history"].append((query, result["result"]))

        return result["result"]
