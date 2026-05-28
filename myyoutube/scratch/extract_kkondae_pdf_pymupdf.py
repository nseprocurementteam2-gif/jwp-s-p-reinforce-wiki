# -*- coding: utf-8 -*-
import fitz  # PyMuPDF
import os

def extract_text(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text() + "\n"
        return text
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    pdf_file = r"c:\Users\NSE\.connect-ai-brain\myyoutube\꼰대부장에서 Ai마스터.pdf"
    content = extract_text(pdf_file)
    output_path = r"c:\Users\NSE\.connect-ai-brain\myyoutube\scratch\kkondae_content.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Content saved to {output_path}")
