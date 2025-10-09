# LangChain Research Assistant Project

This project is a modular AI-powered research assistant built with **LangChain**, **OpenAI API**, and **Streamlit**.
It automates different research workflow tasks, including literature retrieval, summarization, transcript annotation, code generation, and fact-checking.

---

## Features

### Researcher
- `researcher.py`:
- Generate research summaries from a single keyword or topic for five times, including:
  -  General introduction
  -  List of research papers 
  -  Future research directions
  -  Suggested titles for future research
     Additionally, annotates content using NER (Named Entity Recognition).
     Reports are saved automatically in researcher/reports/.

- `multiple_research.py`:
- Support multiple keywords input and produce research insights in the same format as above.
Also performs NER annotation.
Reports are saved in researcher/reports/.

### Summarizer
- `literature_summarizer.py`: 
- Create concise summaries based on PDF files uploaded by users.
Summaries are saved in summarizer/reports/.

### Transcript Annotation
- `transcript_annotation.py`:
- Annotates and analyzes transcripts from text or PDF files uploaded by users.

### Code Generator
- `code_generator.py`:
- Automatically generates clean and efficient Python code, and modifies it according to user input.
  
### Advanced Tools
- `factcheck/`: Fact-check and filter research outputs.
- `factcheck.py`:
  - Detects factual inconsistencies in AI-generated research outputs by cross-checking cited papers against:
    - Google Scholar (via SerpAPI)
    - IEEE Xplore API
- `fact_filtered.py`: Filters and exports verified statements to CSV.
- Input and output files located in `advanced_tools/factcheck/fact_check_result/` and `/filtered_result/`.

---

## Project Structure
```text
langchain-project/
├── researcher/
│   ├── researcher.py
│   ├── multiple_research.py
│   └── reports/
├── summarizer/
│   ├── literature_summarizer.py
│   └── reports/
├── transcript_annotation/
│   └── transcript_annotation.py
├── code_generator/
│   └── code_generator.py
├── advanced_tools/
│   └── factcheck/
│       ├── factcheck.py
│       ├── fact_filtered.py
│       ├── fact_check_result/
│       └── filtered_result/
├── README.md
└── requirements.txt

