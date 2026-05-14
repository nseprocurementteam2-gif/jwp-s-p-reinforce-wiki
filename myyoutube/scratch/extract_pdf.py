import pdfplumber
import sys

def extract_text(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"
            return text
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    pdf_file = "실패하는 학습 계획의 3가지 공통 오류.pdf"
    content = extract_text(pdf_file)
    with open("scratch/pdf_content.txt", "w", encoding="utf-8") as f:
        f.write(content)
    print("Content saved to scratch/pdf_content.txt")
