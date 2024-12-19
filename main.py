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

chat_model = ChatOpenAI(model="gpt-4o", temperature=0.5)

# Define the template
prompt_template = """
You are a helpful assistant that writes clean, efficient Python code based on the following description:
{description}
    
Please generate the Python code accordingly. 
"""
modify_template = """
You are a helpful assistant that modifies Python code based on the following requirements.
Original Code:
{code}

Modification Request:
{modification_request}

Please generate the updated Python code accordingly.
"""

# Initionlize the template 
generate_prompt = PromptTemplate(input_variables=["description"], template=prompt_template)
modify_prompt = PromptTemplate(input_variables=["code","modification_request"], template=modify_template)

chain = LLMChain(llm=chat_model, prompt=prompt)
modify_chain = LLMChain(llm=chat_model, prompt=modify_prompt)

# User interface
st.title("Code Generator")

# User input requirement
st.header("Step 1 : Generate Code")
description = st.text_area("Enter your request:")
if st.button("Generate Code"):
    try:
        result = generate_chain.run({"description": description})



#-----------------------not done yet--------------



st.button("Generate Code"):
    try:
        result = chain.run({"description": description})
        st.subheader("Generated Code:")
        st.code(result, language="python")
    except Exception as e:
        st.error(f"Error:{e}")