import pypdf
import os

pdf_path = r"c:\Users\NSE\.connect-ai-brain\구매메인보드\003. (주)세인티앤엘특수 안성위험물 공사 공내역서 (전기, 통신공사)-REV(0).pdf"

if not os.path.exists(pdf_path):
    print(f"File not found: {pdf_path}")
    exit(1)

reader = pypdf.PdfReader(pdf_path)
print(f"Total pages: {len(reader.pages)}")

# 구조 파악을 위해 첫 3페이지만 텍스트 추출
for i in range(min(3, len(reader.pages))):
    print(f"--- Page {i+1} ---")
    print(reader.pages[i].extract_text())
    print("-" * 20)
