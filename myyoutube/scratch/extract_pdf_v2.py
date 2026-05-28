
import fitz  # PyMuPDF
import os

def extract_pdf_text(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

if __name__ == "__main__":
    file_path = r"c:\Users\NSE\.connect-ai-brain\myyoutube\이게 진짜 된다고 레고처럼 조립하는 AI 자동비서 만들기.pdf"
    if os.path.exists(file_path):
        content = extract_pdf_text(file_path)
        print("--- CONTENT START ---")
        print(content)
        print("--- CONTENT END ---")
    else:
        print("File not found.")
