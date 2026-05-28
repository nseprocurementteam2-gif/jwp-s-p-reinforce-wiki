# 📺 레오 — 도출된 키워드를 기반으로 향후 4주간 업로드할 구체적인 영상 주제 및 시리즈 기획안을 작성하라.

⚠️ 레오 LLM 호출 실패: read ECONNRESET

---

## 📊 LLM 실패에도 시스템이 가져온 실데이터는 보존됨



[실시간 데이터 — 시스템이 방금 도구로 가져온 진짜 출력]

### YouTube 채널 영상 분석 (실제 API 데이터) _(exit 1)_
```
Traceback (most recent call last):
  File "c:\Users\NSE\.connect-ai-brain\_company\_agents\youtube\tools\my_videos_check.py", line 145, in main
    from googleapiclient.discovery import build
ModuleNotFoundError: No module named 'googleapiclient'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "c:\Users\NSE\.connect-ai-brain\_company\_agents\youtube\tools\my_videos_check.py", line 478, in <module>
    main()
    ~~~~^^
  File "c:\Users\NSE\.connect-ai-brain\_company\_agents\youtube\tools\my_videos_check.py", line 147, in main
    print("\u274c google-api-python-client �̼�ġ. pip install google-api-python-client requests")
    ~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'cp949' codec can't encode character '\u274c' in position 0: illegal multibyte sequence
```

### YouTube 설정 확인 (fallback) _(exit 1)_
```
������ YouTube ���� / ä�� ���� ������
  API Ű            : AIza��Zlw
  �� ä�� �ڵ�       : (����)
  �� ä�� ID        : UCDX7VoK6ehFDxEoxX0NxXYw
  ���� ä�� (0��) : (����)
  ���� ä�� (0��): (����)
  �ڷ��׷�          : �̼��� (���� �˸� ��Ȱ��)
  Ollama URL        : http://127.0.0.1:11434
  �м� ��          : (�ڵ� ����)
Traceback (most recent call last):
  File "c:\Users\NSE\.connect-ai-brain\_company\_agents\youtube\tools\youtube_account.py", line 46, in <module>
    main()
    ~~~~^^
  File "c:\Users\NSE\.connect-ai-brain\_company\_agents\youtube\tools\youtube_account.py", line 43, in main
    print("\n\u2705 ���� ���� �ε� OK. �ٸ� �������� �� ���� �ڵ����� ����մϴ�.")
    ~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'cp949' codec can't encode character '\u2705' in position 2: illegal multibyte sequence
```

🛑 **실시간 데이터 가져오기 실패** — 위 출력은 에러 메시지뿐. 사용자에게 정확히 무엇이 문제인지(Python 미설치? 패키지 미설치? API 키 미설정?) 알려주고, 가짜 분석·placeholder 데이터 절대 생성하지 마세요. 작업은 '대기' 평가로 끝내고 다음 단계는 사용자가 환경 셋업 후 재시도.

_위 데이터를 기반으로 다음 에이전트가 분석을 이어가야 합니다. "데이터 로드 실패"로 잘못 보고하지 마세요._
