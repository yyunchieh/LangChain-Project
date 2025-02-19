import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
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
    
    if not topic:
        st.error("Error: No topic provided!")
        return ""
    
    prompt_template = f"""
    You are a research assistant that generates structured answers for a given {topic}. 
    Provide the response in **Markdown format** with the following structure:
        
        Research Insights on {topic}

        General Introduction
        Provide an overview of the topic.

        List of Research Papers
        - Paper 1
        - Paper 2
        - Paper 3

        Future Research Directions that no one has done before or only a few people have done
        - Direction 1
        - Direction 2
        - Direction 3

        Titles for Future Research Directions 
        - Title 1
        - Title 2

        """
     
    responses = []
    for i in range(5):
         response_markdown = chat_model.predict(prompt_template)
         responses.append(f" ## Response Set {i+1}\n\n{response_markdown}\n\n---\n")


    summary_prompt = f"""
    You are an expert researcher. Given the following insights on "{topic}",
    provide a **concise summary**.
    Highlight key points, major themes, and overall trends.

    {''. join(responses)}

    Format the summary in **Markdown** with the section:
    """
    
    #st.text("Generating Summary...")

    summary = chat_model.predict(summary_prompt)

    if not summary.strip():
         summary = "Summary generation failed."

    #st.text(f"Debug: Summary content:\n{summary}")

    full_markdown = f" # Research Insights on {topic}\n\n" + "".join(responses) + f"\n\n## Summary of Research Insights\n\n{summary}"

    
    return full_markdown


if st.button("Generate Research Insights"):
    if topic:
             markdown_content = generate_research_insights(topic)

             if markdown_content:
                  md_filename = f"Research_Insights_{topic.replace(' ', '_')}.md"
                  with open(md_filename, "w", encoding="utf-8") as md_file:
                       md_file.write(markdown_content)

                  st.success("Markdown file generated successfully!")

                  with open(md_filename, "r", encoding="utf-8") as md_file:
                       st.download_button("Download Markdown File", md_file, file_name=md_filename)
    
    else:
        st.warning("Please enter a research topic")