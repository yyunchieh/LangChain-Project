import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os
import openai
import json
import re
import requests
import pandas as pd
from serpapi import GoogleSearch

# Load API key
API_path = r"C:\Users\4019-tjyen\Desktop\API.txt"
with open(API_path,"r") as file:
    openapi_key = file.read().strip()
    
os.environ['OPENAI_API_KEY'] = openapi_key
openai.api_key = openapi_key

IEEE_API_path = r"C:\Users\4019-tjyen\Desktop\IEEE Xplore API.txt"
with open(IEEE_API_path, "r") as file:
    IEEE_API_key = file.read().strip() 

Serp_API_path = r"C:\Users\4019-tjyen\Desktop\SerpAPI.txt"
with open(IEEE_API_path, "r") as file:
    Serp_API_key = file.read().strip() 

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
            Each paper **must** follow this exact format:
            - "Paper Title" by Author Name, Year.

            Ensure the papers are **real** and can be verified in academic databases.
    
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
            st.session_state["markdown_content"] = markdown_content

            md_filename = "Research_Insights.md"
            
            with open(md_filename, "w", encoding="utf-8") as md_file:
                md_file.write(markdown_content + "\n\n# Summary\n" + summary)

            st.success("Markdown file generated successfully!")

            with open(md_filename, "r", encoding="utf-8") as md_file:
                st.download_button("Download Markdown File", md_file, file_name=md_filename)

               # ner_result = Ner(summary)
               #st.json(ner_result)

        else:
            st.error("Please add at least one keyword")


# Fact Check Functions          
def extract_paper_details(markdown_content):
    pattern = r'"(.*?)" by (.*?), (\d{4})\.'
    matches = re.findall(pattern, markdown_content)
    papers = [{"title": m[0], "author": m[1], "year": m[2]} for m in matches]
    return papers

def check_google_scholar(title):
    params = {
        "engine": "google_scholar",
        "q": title,
        "api_key": Serp_API_key
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    papers = results.get("organic_results", [])

    for paper in papers:
        if paper.get("title", "").lower() == title.lower():
            return True
    return False


#def check_semantic_scholar(title):
#    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={title}&limit=1"
#    response = requests.get(url)

#    if response.status_code == 200:
#        data = response.json()
#        return len(data.get("data",[])) > 0
#   return False

def check_ieee_xplore(title):
    url = f"https://ieeexploreapi.ieee.org/api/v1/search/articles?querytext={title}&apikey={IEEE_API_key}&max_records=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return len(data.get("articles", [])) > 0
    return False

def fact_check_papers(markdown_content):
    papers = extract_paper_details(markdown_content)
    verified_papers = []

    for paper in papers:
    #   found_in_semantic = check_semantic_scholar(paper["title"])
        found_in_google_scholar = check_google_scholar(paper["title"])
        found_in_ieee = check_ieee_xplore(paper["title"])

        status = "Verified" if found_in_google_scholar or found_in_ieee else "Fake/Unverified"
        verified_papers.append({
            "title":paper["title"],
            "author":paper["author"],
            "year":paper["year"],
            "status":status
        })
        
    return verified_papers

if st.button("Fact Check Research Papers"):
    if "markdown_content" in st.session_state and st.session_state["markdown_content"]:
        st.write("Checking...")

        markdown_content = st.session_state["markdown_content"]
        papers = extract_paper_details(markdown_content)

        if not papers:
            st.warning("Did not find any papers")

        else:
            checked_papers = fact_check_papers(markdown_content)

            df = pd.DataFrame(checked_papers)
            csv_filename = "Fact_check_results.csv"
            df.to_csv(csv_filename, index=False, encoding="utf-8")

            st.success(f"Fact check results saved to {csv_filename}")

            with open(csv_filename, "r", encoding="utf-8") as file:
                st.download_button("Download Fact Check CSV", file, file_name=csv_filename)
    else:
        st.error("No research insights generated yet! Please generate insights first.")
        


