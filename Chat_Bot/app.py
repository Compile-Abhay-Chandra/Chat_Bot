
from flask import Flask, render_template, request, jsonify, session
from services.assistant import process_command
import os
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for session

app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    command = request.json.get("command", "")
    use_pdf = request.json.get("use_pdf", True)
    pdf_text = session.get('pdf_text', None)
    # Only use pdf_text if the user wants to
    if use_pdf and pdf_text:
        response = process_command(command, pdf_text=pdf_text)
    else:
        response = process_command(command)
    return jsonify({"response": response})


# PDF upload and parse endpoint
@app.route("/upload_pdf", methods=["POST"])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and file.filename.lower().endswith('.pdf'):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        try:
            reader = PdfReader(filepath)
            text = "\n".join(page.extract_text() or '' for page in reader.pages)
            session['pdf_text'] = text
            return jsonify({"success": True})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "Invalid file type"}), 400

if __name__ == "__main__":
    app.run(debug=True)
