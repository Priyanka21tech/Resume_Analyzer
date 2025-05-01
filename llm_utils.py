import os
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
import markdown #type:ignore # For converting markdown to HTML
import re  # Regular expressions for validation

# Set your OpenAI API key (you can load from environment vars)
openaikey=os.environ["OPENAI_API_KEY"]

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

prompt = PromptTemplate(
    input_variables=["resume", "job"],
    template="""
You are a meticulous resume reviewer.
Below is a candidate's resume and a job description. Assume both are validly formatted.

Give a match score (0–100).
List the top 3 skills or qualifications missing.
Suggest improvements to the resume.
Rewrite 3 bullet points to better match the job.

Give proper headings for all handling the markdowns effectively.
Resume:
{resume}

Job Description:
{job}
"""
)

chain = LLMChain(llm=llm, prompt=prompt)

def is_valid_resume(resume_text):
    """Check if the resume has at least 2 valid sections."""
    keywords = ["experience", "education", "skills", "projects", "summary", "certifications"]
    found = [kw for kw in keywords if kw in resume_text.lower()]
    return len(found) >= 2

def is_valid_job_description(job_text):
    """Check if the job description has at least 2 bullet points."""
    bullet_lines = re.findall(r"(?m)^\s*[\u2022•\-–*]\s+.*", job_text)
    return len(bullet_lines) >= 2

def analyze_resume(resume_text, job_text):
    """Analyze the resume and job description using the LLM chain."""
    response = chain.run(resume=resume_text, job=job_text)

    # Convert Markdown response to HTML
    html_response = markdown.markdown(response)
    
    return html_response
