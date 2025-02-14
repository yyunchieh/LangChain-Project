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
chat_model = ChatOpenAI(model="gpt-4o", temperature=0.5, response_format="json")

# Streamlit UI
st.title("Research Assistant")
topic = st.text_input("Enter your research topic:")

def generate_research_insights(topic):
    prompt_template = """
    You are a helpful research assistant that generates structured answers for a given topic. Provide the response in JSON format with the following structure:
    {
        "General Introduction": "Your answer here",
        "Research Papers": ["Paper 1", "Paper 2", "Paper3"],
        "Future Research Directions": ["Direction 1", "Direction 2", "Direction 3"]
        "Research Titles": ["Title 1", "Title 2"]
    }
    Topic: {topic}
    """

    formatted_prompt = prompt_template.format(topic=topic)
    response_sets = []

    for _ in range(5):
        response = chat_model.predict(formatted_prompt)
        response_json = json.loads(response)
        response_sets.append(response_json)
    
    return response_sets

def format_as_markdown(response_sets):
        markdown_text = f"# Research Insights on {topic}\n\n"

        
#if st.button("Generate Research Insights"):
 #   if topic:
  #      research_outputs = generate_research_insights(topic)

        for idx, response in enumerate(response_sets, start=1):
             markdown_text += f"## Response Set {idx}\n\n"
             markdown_text += f"### General Introduction\n{response["General_Introduction"]}\n\n"
             markdown_text += f"### List of Research Papers\n"
             for paper in response["Research_Papers"]:
                  markdown_text += f"- {paper}\n"
             markdown_text += f"\n### Future Research Directions\n"
             for direction in response["Future_Research_Directions"]:
                  markdown_text += f"-{direction}\n"
             markdown_text += f"\n### Titles for Future Research\n"
             for title in response["Research_Titles"]:
                  markdown_text += "\n---\n"
        
        return markdown_text


if st.button("Generate Research Insights"):
    if topic:
             research_outputs = generate_research_insights(topic)
             markdown_content = format_as_markdown(research_outputs)

             md_filename = f"Research_Insights_{topic.replace("","_")}.md"
             with open(md_filename, "w", encoding="utf-8") as md_file:
                  md_file.write(markdown_content)

             st.success("Markdown file generated successfully!")

             with open(md_filename, "r", encoding="utf-8") as md_file:
                  st.download_button("Download Markdown File", md_file, file_name=filename)

    else:
         st.warning("Please enter a research topic")
         
                  
                   
             