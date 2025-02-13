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

# Initialize Chat Model
chat_model = ChatOpenAI(model="gpt-4o", temperature=0.5)

# Streamlit UI
st.title("Research Assistant")
topic = st.text_input("Enter your research topic:")

def generate_research_insights(topic):
    prompt_template = """
    You are a helpful research assistant that generates answers according to topic that users input. The answers include:
     1. Gerneral introduction of the topic
     2. A list of important research papers for the topic
     3. Possible directions of future research that no one has done before or only a few people have done
     4. Titles for future research you mentioned in the last question

    Topic:
    {topic}

    Please generate the answers accordingly.
    """

    formatted_prompt = prompt_template.format(topic=topic)
    response_sets = []

    for _ in range(5):
        response = chat_model.predict(formatted_prompt)
        response_sets.append(response.split("\n\n"))
    
    return response_sets

if st.button("Generate Research Insights"):
    if topic:
        research_outputs = generate_research_insights(topic)

        for set_idx, response_set in enumerate(research_outputs, start=1):
             st.markdown(f"<h2 style='font-size:24px; font-weight:bold;'>Response Set {set_idx}</h2>", unsafe_allow_html=True)
             
             for idx, response in enumerate(response_set, start=1):
                st.markdown(f"<h3 style='font-size:20px; font-weight:bold>", unsafe_allow_html=True)
                st.write(response)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<h2 style='font-size:24px; font-weight:bold;'>Summary</h2>", unsafe_allow_html=True)

        summary_responses = [
            "General Introduction:" + "".join([set[0] for set in research_outputs]),
            "List of Research Papers:" + "".join([set[1] for set in research_outputs]),
            "Future Research Directions:" + "".join([set[2] for set in research_outputs]),
            "Titles for Future Research:" + "".join([set[3] for set in research_outputs])
        ]

        for idx, summary in enumerate(summary_responses, start=1):
            st.markdown(f"<h3 style='font-size:20px; font-weight:bold;'>Part {idx}</h3>", unsafe_allow_html=True)
            st.write(summary)
    
    else:
        st.warning("Please enter a research topic")