# Resume_Analyzer
A web-based Resume Analyzer that allows users to upload resumes in PDF format, then extracts and analyzes the content.

Project Overview-
The Resume Analyzer project aims to streamline the recruitment process by intelligently evaluating candidate resumes against specific job descriptions using AI. It allows users to upload resume PDFs—supporting encrypted files with optional passwords—and compares them to job descriptions written in proper bullet-point format. The system ensures both inputs meet formatting standards before proceeding. Using LangChain and a carefully crafted LLM prompt, it provides a structured analysis including a match score, missing qualifications, improvement suggestions, and rewritten resume points—presented in a clear, markdown-formatted output for easy review.

Here is the project structure:

-->ResumeCheck
  1. --> renv is the virtual environment that will be created like- 
        (python -m venv renv)
        Activate the virtual environment beforing running the app.py with the code (renv\Scripts\activate)
  2. -->static
        -->styles.css
  3. -->templates
        -->index.html
        -->results.html
  4. -->app.py
  5. -->llm_utils.py

     
  You need to create a .env file that will store the OPENAI_API credentials
