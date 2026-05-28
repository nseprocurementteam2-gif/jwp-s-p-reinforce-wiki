import fitz  # PyMuPDF
import os

def extract_pdf_text(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

if __name__ == "__main__":
    file_path = r"c:\Users\NSE\.connect-ai-brain\myyoutube\저는 AI랑 대화해서 퇴근합니다.pdf"
    output_path = r"c:\Users\NSE\.connect-ai-brain\myyoutube\scratch\talk_ai_extracted.txt"
    if os.path.exists(file_path):
        content = extract_pdf_text(file_path)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"텍스트 추출 완료: {output_path}")
    else:
        print("PDF 파일을 찾을 수 없습니다.")
