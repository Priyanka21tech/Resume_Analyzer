import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import fitz  # PyMuPDF
from llm_utils import analyze_resume,is_valid_job_description,is_valid_resume

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ✅ Updated to handle password-protected PDFs
def extract_text(file_path, password=None):
    try:
        text = ''
        with fitz.open(file_path) as doc:
            if doc.needs_pass and not doc.authenticate(password or ""):
                return None  # PDF is encrypted and not authenticated
            for page in doc:
                text += page.get_text()
        return text
    except Exception as e:
        print(f"PDF extraction error: {e}")
        return ""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    resume_file = request.files['resume']
    job_text = request.form['job_desc']
    pdf_password = request.form.get('pdf_password', '')  # ✅ get password input

    # Ensure a valid resume file is uploaded
    if resume_file and allowed_file(resume_file.filename):
        filename = secure_filename(resume_file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        resume_file.save(file_path)

        resume_text = extract_text(file_path,password=pdf_password)

        # Validate before LLM processing
        if not is_valid_resume(resume_text):
            # If resume is not in valid format, return an error message
            return render_template('index.html', error="❌ Your resume is not in a valid format. Include sections like 'Experience', 'Education', or 'Skills'.")

        if not is_valid_job_description(job_text):
            # If job description is not in valid format, return an error message
            return render_template('index.html', error="❌ Please enter a proper job description with bullet points.")

        # If both resume and job description are valid, proceed with the analysis
        analysis_result = analyze_resume(resume_text, job_text)

        return render_template('results.html', result=analysis_result)

    # If the file is not a PDF
    return render_template('index.html', error="Invalid file format. Please upload a PDF file only.")

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True,port=5005)
