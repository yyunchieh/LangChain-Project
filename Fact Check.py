import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os
import openai
import json
import re
import requests

# Load API key
API_path = r"C:\Users\4019-tjyen\Desktop\API.txt"
with open(API_path,"r") as file:
    openapi_key = file.read().strip()
    
os.environ['OPENAI_API_KEY'] = openapi_key
openai.api_key = openapi_key

# Initialize Chat Model
chat_model = ChatOpenAI(model="gpt-4o", temperature=0.6)

# Streamlit UI
st.title("Research Assistant")

st.header("Add Research Keywords")

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
    
    all_responses = []

    for keyword in keywords:
        keyword_responses = []
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
            Avoid hallucinating information, especially in the research papers section.
            """

            response_markdown = ""
            
            try:
                response_markdown = chat_model.predict(prompt_template)

            except Exception as e:
                st.error(f"Error generating response for '{keyword}': {e}")
                continue

       
            if isinstance(response_markdown, tuple):
                response_markdown = response_markdown[0] if response_markdown else ""

            
            keyword_responses.append(f"## Response Set {i+1} for {keyword}\n\n{response_markdown}\n\n---\n")


        all_responses.extend(keyword_responses)

    full_markdown = "".join(all_responses)


    summary_prompt = f"""
    You are an expert researcher. Given the following five research insights, provide a **concise summary**.

    Your summary must be purely based on the provided research insights. **Do not introduce new information.**
    
    Extract 1.Key Points and Major Themes 2.Research Papers (list all of them that were mentioned) 3.Overall Trends 4.Future Research Directions 5.Suggested Title for Future Research
    in the responses.

    {full_markdown}

    Format the summary in **Markdown**.
    """
    

    summary = chat_model.predict(summary_prompt)

    if not summary.strip():
        summary = "Summary generation failed."


    return full_markdown, summary

             

if st.button("Generate Research Insights"):
    if st.session_state["keyword_list"]:
        keywords = st.session_state["keyword_list"]

        markdown_content, summary = generate_research_insights(keywords)
        
        if markdown_content:
            md_filename = f"Research_Insights.md"
            
            with open(md_filename, "w", encoding="utf-8") as md_file:
                md_file.write(markdown_content + "\n\n# Summary\n" + summary)

                st.success("Markdown file generated successfully!")

                with open(md_filename, "r", encoding="utf-8") as md_file:
                    st.download_button("Download Markdown File", md_file, file_name=md_filename)

               # ner_result = Ner(summary)
               #st.json(ner_result)

        else:
            st.error("Please add at least one keyword")


# Fact Check            
def extract_paper_details(markdown_content):
    pattern = r'"(.*?)" by (.*?), (\d{4})\.'
    matches = re.findall(pattern, markdown_content)

    papers = [{"title": m[0], "author": m[1], "year": m[2]} for m in matches]
    return papers

def check_paper_existence(title):
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={title}&limit=1"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if "data" in data and len(data["data"]) > 0:
            return True
    
    return False

def fact_check_papers(markdown_content):
    papers = extract_paper_details(markdown_content)
    verified_papers = []

    for paper in papers:
        is_real = check_paper_existence
        status = "Verified" if is_real else "Fake/Unverified"
        verified_papers.append(f'-"{paper["title"]}" by {paper["author"]}, {paper["year"]}. **{status}**')

    return "\n".join(verified_papers)

if st.button("Fact Check Research Papers"):
    if markdown_content:
        checked_markdown = fact_check_papers(markdown_content)
        st.markdown(checked_markdown)
    
    else:
        st.error("No research insights generated yet!")