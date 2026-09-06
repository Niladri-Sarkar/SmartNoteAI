from flask import Flask, render_template, request
from transformers import pipeline
import PyPDF2

app = Flask(__name__)

summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def extract_pdf_text(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

@app.route('/', methods=['GET', 'POST'])
def home():
    summary = ""

    if request.method == 'POST':
        text = ""

        # PDF input
        if 'pdf' in request.files and request.files['pdf'].filename != "":
            pdf_file = request.files['pdf']
            text = extract_pdf_text(pdf_file)

        # Text input
        else:
            text = request.form['text']

        if text:
            result = summarizer(text, max_length=100, min_length=30)
            summary = result[0]['summary_text']

    return render_template('index.html', summary=summary)

if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)