import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import json
import os
import openai
import fitz
import traceback
import re

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

st.title("Transcript Annotation Tool")
st.write("Please upload the transcript or input it below:")

text_input = st.text_area("Input Transcript", placeholder="Input the transcript that needs to be analyzed...")
uploaded_file = st.file_uploader("or upload a transcript file", type=["txt", "pdf"])


def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = "\n".join([page.get_text() for page in doc])
    return text

if uploaded_file is not None:
    if uploaded_file.name.endswith(".txt"):
        text_input = uploaded_file.read().decode("utf-8")
    elif uploaded_file.name.endswith(".pdf"):
        text_input = extract_text_from_pdf(uploaded_file)

if st.button("Annotate") and text_input.strip():
    st.write("Extracting words...")

    messages = template.format_messages(text=text_input)


    try: 
        response = llm.invoke(messages)

        try:
            entities = json.loads(response.content)
            st.success("Done! Result:")
            st.json(entities)

            st.write("### Form")
            st.table(entities)

            annotations = []

            for entity_type, entity_list in entities.items():
                for entity in entity_list:
                    for match in re.finditer(re.escape(entity), text_input):
                        annotations.append({
                            "start": match.start(),
                            "end": match.end(),
                            "text": text_input[match.start():match.end()],
                            "labels": [entity_type.lower()]
                        })

            if annotations:
                st.write("### Annotations with positions (JSON format)")
                st.json(annotations)
            else:
                st.warning("No entities found in the text")

        except json.JSONDecodeError:

            st.error("The result can't be analyzed in JSON. Below is the raw output:")
            st.text(response.content) 


    except Exception as e:
        st.error(f"Error:{str(e)}")
        st.text(traceback.format_exc())

else:
    st.info("Please input transcript or upload files, and click Annotate")

st.markdown("**Hint**: Driven by GPT-4 model and designed for annotation in texts.")

