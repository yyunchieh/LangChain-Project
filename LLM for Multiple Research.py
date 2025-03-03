import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os
import openai
import json
import re
#import spacy
#from spacy.cli import download
#from spacy.pipeline import EntityRuler


# Load API key
API_path = r"C:\Users\4019-tjyen\Desktop\API.txt"
with open(API_path,"r") as file:
    openapi_key = file.read().strip()
    
os.environ['OPENAI_API_KEY'] = openapi_key
openai.api_key = openapi_key

# Initialize Chat Model
chat_model = ChatOpenAI(model="gpt-4o", temperature=0.8)

# Streamlit UI
st.title("Research Assistant")

st.header("Add Research Keywords")
keywords = []

if "keyword_list" not in st.session_state:
    st.session_state["keyword_list"] = []


new_keyword = st.text_input("Enter a new keyword:")
if st.button("Add Keyword") and new_keyword:
    st.session_state["keyword_list"].append(new_keyword)
    new_keyword = ""

st.subheader("Current Keywords:")
for i, kw in enumerate(st.session_state["keyword_list"]):
    st.write(f"{i+1}. {kw}")


def generate_research_insights(keywords):
    
    if not keywords:
        st.error("Error: No keywords provided!")
        return "", ""
    
    responses = []
    for keyword in keywords:
        for i in range(5):
            prompt_template = f"""
            You are a highly knowledgeable research assitant specializing in {keyword}.
            Your task is to generate **structured research insights** in **Markdown format**.
            Your response should follow the exact structure below:
    
            # Research Insights on {keyword}

            ## General Itroduction
            Provide a **concise yet informative** introduction to {keyword}.

            ## List of Research Papers
            Please write in **Chicago Style Citation format**
    
            ## Future Research Directions
            Identify **novel research directions** that have not been widely explored.
            Focus on areas where **only a few studies exist** or where **new advancements are possible**.
            Provide at least **three unique ideas**, with a 1-2 sentence explanation for each.

            ## Title for Future Research

            Your response must be formatted in Markdown and strictly follow this structure.

            """
     
            responses_markdown = chat_model.predict(prompt_template)

            if isinstance(response_markdown, tuple):
                response_markdown = response_markdown[0]

            
            responses.append(f"## Response Set {i+1} for {keyword}\n\n{response_markdown}\n\n---\n")




        full_markdown = "".join(responses)
    
        if isinstance(response_markdown, tuple):
              full_markdown = "".join(full_markdown)
    



        summary_prompt = f"""
        You are an expert researcher. Given the following five research insights, provide a **concise summary**.

        Your summary must be purely based on the provided research insights. **Do not introduce new information.**
    
        Extract 1.Key Points and Major Themes 2.Research Papers (list all of them that were mentioned) 3.Overall Trends 4.Future Research Directions 5.Suggested Title for Future Research
        in the responses.

        {''. join(responses)}

        Format the summary in **Markdown** with the section:
        """
    

        summary = chat_model.predict(summary_prompt)

        if not summary.strip():
            summary = "Summary generation failed."


        return full_markdown, summary


def Ner(text):
        ner_prompt = f"""
        Extract named entities from the following text and return them in a structured JSON format.
        
        Text:
        {text}

        Your output should be a valid JSON object with the following keys:
        - "PERSON": List of names
          *If multiple authors are separated by "and" or "," (e.g. "Smith, John, and Emily Johnson"), split them correctly.
          For example: Smith, John, and Emily Johnson should be labeled as "Smith", "John", "Emily Johnson"
        - "PROPER NOUN": List of scholar or professional words
        - "DATE": List of dates
   

        If no entity is found, return an empty list for that key.
        
        """

        response = chat_model.predict(ner_prompt)

        clean_response = re.sub(r"```json\s*([\s\S]*?)\s*```", r"\1", response.strip())

        try:
             parsed_json = json.loads(clean_response)
             return parsed_json
        except json.JSONDecodeError:
             return {"error": "Invalid JSON response from model","raw_response": response }
        
             

if st.button("Generate Research Insights"):
    if st.session_state["keyword_list"]:
        markdown_content, summary = generate_research_insights(st.session_state["keyword_list"])
        
        if markdown_content:
            md_filename = f"Research_Insights.md"
            
            with open(md_filename, "w", encoding="utf-8") as md_file:
                md_file.write(markdown_content + "\n\n# Summary\n" + summary)

                st.success("Markdown file generated successfully!")

                with open(md_filename, "r", encoding="utf-8") as md_file:
                    st.download_button("Download Markdown File", md_file, file_name=md_filename)

                if isinstance(markdown_content, tuple):
                    markdown_content = "\n".join(markdown_content)

                ner_result = Ner(summary)
                st.json(ner_result)

        else:
            st.error("Please add at least one keyword")

                    