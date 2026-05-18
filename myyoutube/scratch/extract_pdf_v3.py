
import fitz  # PyMuPDF
import os

def extract_pdf_text(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

if __name__ == "__main__":
    file_path = r"c:\Users\NSE\.connect-ai-brain\myyoutube\3일의 기적을 10분으로 압축하는 AI 설계 혁명.pdf"
    output_path = r"c:\Users\NSE\.connect-ai-brain\myyoutube\scratch\extracted_text.txt"
    if os.path.exists(file_path):
        content = extract_pdf_text(file_path)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Text extracted and saved to {output_path}")
    else:
        print("File not found.")
