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

# Initialize the Chat Model
chat_model = ChatOpenAI(model="gpt-4o", temperature=0.5)

# Define the templates
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

# Initialize the templates 
generate_prompt = PromptTemplate(input_variables=["description"], template=prompt_template)
modify_prompt = PromptTemplate(input_variables=["code","modification_request"], template=modify_template)

chain = LLMChain(llm=chat_model, prompt=generate_prompt)
modify_chain = LLMChain(llm=chat_model, prompt=modify_prompt)

if "current_code" not in st.session_state:
    st.session_state["current_code"] = ""

if "modification_history" not in st.session_state:
    st.session_state["modification_history"] = []

# User interface
st.title("Code Generator")

# Step 1 : Generate Code
st.header("Generate Code")
description = st.text_area("Enter your request:", key = "code_description")
if st.button("Generate Code"):
    try:
        result = chain.run({"description": description})
        # Store the generated code
        st.session_state["current_code"] = result
        # Initialize modification history
        st.session_state["modification_history"] = []
        st.subheader("Generated_code")
        st.code(result, language="python")
    except Exception as e:
        st.error(f"Error generating code: {e}")

# Step 2 : Modify Code       
if st.session_state["current_code"]:
    st.header("Modify Code")

    # Input for modification request
    modification_request = st.text_area("Enter your modification request:", key = "modification_request")
    
    # Display current code
    st.subheader("Current Code:")
    st.code(st.session_state["current_code"], language="python")

    if st.button("Apply Modification"):
        try:
            # Initialize modification_history if missing
            if "modification_history" not in st.session_state:
                st.session_state["modification_history"] = []

            # Run modification chain    
            updated_code = modify_chain.run({
            "code": st.session_state["current_code"],
            "modification_request": modification_request
            })

            # Update current code and save modification history
            st.session_state["current_code"] = updated_code
            st.session_state["modification_history"].append(modification_request)

            st.success("Code modified successfully!")
            st.subheader("Modified Code:")
            st.code(updated_code, language="python")
        except Exception as e:
            st.error(f"Error modifying code: {e}")
    

    if st.session_state["modification_history"]:
        st.subheader("Modification History:")
        for i, request in enumerate(st.session_state["modication_history"], 1):
            st.write(f"{i}. {request}")
            
            
        
            
    
    