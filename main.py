import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os
import openai
import spacy
from spacy.cli import download

download("en_core_web_sm")
nlp = spacy.load("en_core_web_sm")


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
    You are a highly knowledgeable research assitant specializing in {topic}.
    Your task is to generate **structured research insights** in **Markdown format**.
    Your response should follow the exact structure below:
    
    # Research Insights on {topic}

    ## General Itroduction
    Provide a **concise yet informative** introduction to {topic}.

    ## List of Research Papers
    Please write in **Chicago Style Citation format**
    
    ## Future Research Directions
    Identify **novel research directions** that have not been widely explored.
    Focus on areas where **only a few studies exist** or where **new advancements are possible**.
    Provide at least **three unique ideas**, with a 1-2 sentence explanation for each.

    ## Title for Future Research

    Your response must be formatted in Markdown and strictly follow this structure.

    """
     
    responses = []
    for i in range(5):
         response_markdown = chat_model.predict(prompt_template)
         
         if isinstance(response_markdown, tuple):
              response_markdown = response_markdown[0]


         responses.append(f" ## Response Set {i+1}\n\n{response_markdown}\n\n---\n")


    summary_prompt = f"""
    You are an expert researcher. Given the following five research insights on "{topic}", provide a **concise summary**.

    Highlight 1.Key Points and Major Themes 2.Research Papers 3.Overall Trends 4.Future Research Directions 5.Suggested Title for Future Research

    {''. join(responses)}

    Format the summary in **Markdown** with the section:
    """
    
    #st.text("Generating Summary...")

    summary = chat_model.predict(summary_prompt)

    if not summary.strip():
         summary = "Summary generation failed."

    #st.text(f"Debug: Summary content:\n{summary}")

    full_markdown = (
        f" # Research Insights on {topic}\n\n" 
        + "".join(responses) 
        + f"\n\n## Summary of Research Insights\n\n{summary}"
    )

    if isinstance(full_markdown, tuple):
         full_markdown = " ".join(full_markdown)

    return full_markdown, summary

def Ner(text):
    doc = nlp(text)
    labeled_text = []

    for token in doc:
        if token.ent_type_:
            labeled_text.append(f"[{token.text} ({token.ent_type_})]")
        else:
            labeled_text.append(token.text)

    return " ".join(labeled_text)


if st.button("Generate Research Insights"):
    if topic:
             markdown_content, summary = generate_research_insights(topic)

             if markdown_content:
                  md_filename = f"Research_Insights_{topic.replace(' ', '_')}.md"
                  with open(md_filename, "w", encoding="utf-8") as md_file:
                       md_file.write(markdown_content)

                  st.success("Markdown file generated successfully!")

                  with open(md_filename, "r", encoding="utf-8") as md_file:
                       st.download_button("Download Markdown File", md_file, file_name=md_filename)

                  if isinstance(markdown_content, tuple):
                    markdown_content = "\n".join(markdown_content)
                    
    
                  st.subheader("NER-Labeled Research Papers")

                  papers_start = summary.find("Research Papers")
                  future_research_start = summary.find("Future Research Directions")

                  if papers_start != -1 and future_research_start != -1:
                       papers_section = summary[papers_start:future_research_start].strip()
                       ner_papers = Ner(papers_section)
                       st.write(ner_papers)
                  
                  else:
                      st.write("Can't find papers, please make sure the format is correct")