import streamlit as st
from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
import os
import openai

# Load API key
API_path = r"C:\Users\4019-tjyen\Desktop\API.txt"
with open(API_path,"r") as file:
    openapi_key = file.read().strip()
    
os.environ['OPENAI_API_KEY'] = openapi_key
openai.api_key = openapi_key

st.title("PDF Summarizer")
uploaded_file = st.file_uploader("Please upload PDF file", type=["pdf"])

if uploaded_file is not None:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    
    loader = PyMuPDFLoader("temp.pdf")
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    split_docs = text_splitter.split_documents(documents)

    llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
    chain = load_summarize_chain(llm, chain_type="map_reduce")

    with st.spinner("Generating Summary..."):
        summary = chain.run(split_docs)

    st.subheader("Summary")
    st.write(summary)

