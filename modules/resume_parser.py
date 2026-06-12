from pypdf import PdfReader

def extract_resume_text(uploaded_file):
    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:
        text += page.extract_text() + "\n"

    return text