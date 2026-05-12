from pdfminer.high_level import extract_text
import os

pdf_path = r"c:\Users\NSE\.connect-ai-brain\구매메인보드\003. (주)세인티앤엘특수 안성위험물 공사 공내역서 (전기, 통신공사)-REV(0).pdf"

if not os.path.exists(pdf_path):
    print(f"File not found: {pdf_path}")
    exit(1)

try:
    print("--- Extracting text using pdfminer ---")
    # 첫 3페이지만 추출 (0-indexed)
    text = extract_text(pdf_path, page_numbers=[0, 1, 2])
    print(text)
except Exception as e:
    print(f"Error: {e}")
