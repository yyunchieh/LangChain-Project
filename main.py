import streamlit as st
import os
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
import openai

API_path = r"C:\Users\4019-tjyen\Desktop\API.txt"
with open(API_path,"r") as file:
    openapi_key = file.read().strip()
    
os.environ['OPENAI_API_KEY'] = openapi_key
openai.api_key = openapi_key

chat_model = ChatOpenAI(model="gpt-4", temperature=0.5)

# Define the template
prompt_template = """
You are a helpful assistant that writes clean, efficient Python code based on the following description:
{description}
    
Please generate the Python code accordingly. 
"""
    
# Initionlize the template 
prompt = PromptTemplate(input_variables=["description"], template=prompt_template)
chain = LLMChain(llm=chat_model, prompt=prompt)

# User interface
st.title("Code Generator")

# User input requirement
description = st.text_area("Enter your request:")

if st.button("Generate Code"):
    try:
        result = chain.run({"description": description})
        st.subheader("Generated Code:")
        st.code(result, language="python")
    except Exception as e:
        st.error(f"Error:{e}")