# scratch/read_docx.py
import docx
import sys

# 터미널 출력 인코딩 설정 (Windows 대응)
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

def read_docx(file_path):
    doc = docx.Document(file_path)
    print("=== Paragraphs ===")
    for i, para in enumerate(doc.paragraphs):
        text = para.text.strip()
        if text:
            print(f"P{i}: {text}")
            
    print("\n=== Tables ===")
    for i, table in enumerate(doc.tables):
        # 테이블의 첫 행이나 두 번째 행에 일자가 있는지 확인
        rows = list(table.rows)
        headers = [cell.text.strip() for cell in rows[0].cells]
        print(f"Table {i} Headers: {headers}")



if __name__ == "__main__":
    read_docx(r"c:\Users\NSE\.connect-ai-brain\myyoutube\6월_하순_골프_쇼츠_계획서.docx")
