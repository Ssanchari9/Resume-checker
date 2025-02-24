from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
from pdfminer.high_level import extract_text

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "uploads"

# Create the upload folder if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Predefined skill categories
SKILL_CATEGORIES = {
    "Programming": ["Python", "Java", "C++", "JavaScript"],
    "Machine Learning": ["TensorFlow", "PyTorch", "AI", "Neural Networks"],
    "Data Analysis": ["Excel", "SQL", "Pandas", "NumPy"],
    "Soft Skills": ["Communication", "Teamwork", "Leadership"],
    "Tools/Software": ["Git", "Jira", "Docker", "Kubernetes"]
}


def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    return extract_text(pdf_path)


def classify_skills(text):
    """Classifies skills based on keywords in the text."""
    skills = {category: [] for category in SKILL_CATEGORIES}

    for category, words in SKILL_CATEGORIES.items():
        for word in words:
            if word.lower() in text.lower():
                skills[category].append(word)

    return {k: v for k, v in skills.items() if v}  # Remove empty categories


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/classify", methods=["POST"])
def classify():
    skills = {}

    if "resume" in request.files:
        file = request.files["resume"]
        if file.filename.endswith(".pdf"):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
            file.save(filepath)
            text = extract_text_from_pdf(filepath)
            skills = classify_skills(text)

    elif "resume_text" in request.form:
        text = request.form["resume_text"]
        skills = classify_skills(text)

    return jsonify({"skills": skills})


if __name__ == "__main__":
    app.run(debug=True)
