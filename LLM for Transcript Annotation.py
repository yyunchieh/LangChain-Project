import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import json
import os
import openai

# Load API key
API_path = r"C:\Users\4019-tjyen\Desktop\API.txt"
with open(API_path,"r") as file:
    openapi_key = file.read().strip()
    
os.environ['OPENAI_API_KEY'] = openapi_key
openai.api_key = openapi_key



llm = ChatOpenAI(model = "gpt-4", temperature=0)


template = ChatPromptTemplate.from_messages([
    ("system", "你是一個文本辨別工具，請提取文字並標註類型(Person, Location, Organization, Date)。"),
    ("user", "請分析以下文本，提取命名並返回JSON格式:\n\n{text}")
])

#prompt = PromptTemplate(input_variables=["text"], template=template)

st.title("Transcript annotation tool")
st.write("Please upload the transcript or input it below:")

text_input = st.text_area("Input Transcript", placeholder="Input the transcript that needs to be analyzed...")
uploaded_file = st.file_uploader("or upload a transcript file", type=["txt"])

if uploaded_file is not None:
    text_input = uploaded_file.read().decode("utf-8")


if st.button("Annotate") and text_input.strip():
    st.write("Extracting words...")

    messages = template.format_messages(text=text_input)


    try:
        response = llm(messages)

        try:
            entities = json.loads(response.content)
            st.success("Done!Result:")
            st.json(entities)

            st.write("### Form")
            st.table(entities)

        except json.JSONDecodeError:

            st.error("The result can't be analyzed in JSON, Please check prompt or transcripts.")
    
    except Exception as e:
        st.error(f"Error:{str(e)}")

else:
    st.info("Please input transcript or upload files, and click Annotate")

st.markdown("**Hint**: Driven by GPT-4 model and designed for annotation in texts.")

