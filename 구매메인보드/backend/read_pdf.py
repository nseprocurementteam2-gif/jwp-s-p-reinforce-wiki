import pypdf
import os

pdf_path = r"c:\Users\NSE\.connect-ai-brain\구매메인보드\조달청 open ai.pdf"

if not os.path.exists(pdf_path):
    print(f"File not found: {pdf_path}")
    exit(1)

reader = pypdf.PdfReader(pdf_path)
print(f"Total pages: {len(reader.pages)}")

# 검색할 키워드
keywords = ["PriceInfoService", "getPrice", "Operation", "오퍼레이션"]

for i, page in enumerate(reader.pages):
    text = page.extract_text()
    if any(kw in text for kw in keywords):
        print(f"--- Page {i+1} ---")
        print(text)
        print("-" * 20)
