# 코부장 비용 분석 시스템 - 백엔드 및 API 연동 지식 문서

이 문서는 코부장 비용 분석 시스템의 품셈 분석 파트 고도화 및 정부 API 연동 작업 내용을 정리한 지식 문서입니다.

## 1. 개요
* **목적**: 품셈 분석 파트의 데이터를 수동 입력에서 정부 API 연동 방식으로 고도화하고, 용어를 명확히 정돈함.
* **기간**: 2026년 5월 11일
* **담당 에이전트**: Antigravity

## 2. 주요 작업 내용

### 2.1 용어 변경 (프론트엔드)
* **변경 전**: 소싱업체
* **변경 후**: 견적업체
* **내용**: 품셈 분석 파트(`CostStandardView` 및 `InputModal`) 내의 모든 '소싱업체' 표기를 '견적업체'로 일괄 변경하여 사용자의 이해도를 높임.
* **수정 파일**: `dashboard-app/src/App.jsx`

### 2.2 파이썬 백엔드 서버 구축
* **기술 스택**: Python, FastAPI, Uvicorn
* **기능**: 프론트엔드의 요청을 받아 정부 API를 호출하고 데이터를 가공하여 반환함.
* **가상환경**: `uv`를 사용한 `.venv` 구성 (패키지: `fastapi`, `uvicorn`, `requests`, `pypdf`)
* **실행 주소**: `http://127.0.0.1:8000`
* **엔드포인트**: `/api/v1/standard-estimation/{category}`

### 2.3 정부 API 분석 및 연동
* **대상 API**: 조달청_나라장터 가격정보현황서비스 (`PriceInfoService`)
* **엔드포인트**: `https://apis.data.go.kr/1230000/ao/PriceInfoService`
* **인증키**: `dc6036868177c098f44b4a6af509bf85c33e30f602e8895a0a51908879970845`
* **사용 오퍼레이션**: `getStdMarkUprcinfoList` (표준시장단가 현황 조회)
  * **근거**: PDF 매뉴얼 분석 결과, 해당 오퍼레이션이 자재비(`mtrlcstUprc`), 노무비(`lbrcstUprc`), 경비(`gnrexpnsUprc`) 단가를 제공함을 확인.

## 3. 고도화된 API 명세 (FastAPI)

### 엔드포인트: `GET /api/v1/standard-estimation/{category}`

**Query Parameters:**
* `begin_date` (string, 기본값: "20230101"): 조회 시작일 (YYYYMMDD)
* `end_date` (string, 기본값: "20231231"): 조회 종료일 (YYYYMMDD)
* `item_code` (string, 선택사항): 특정 품목 코드

**응답 형태:**
```json
{
  "source": "정부 API (조달청 표준시장단가 - 품목명)",
  "raw_data": { ... },
  "baseCost": 450000000,
  "breakdown": {
    "material": 220000000,
    "labor": 150000000,
    "expense": 80000000
  }
}
```

## 4. 향후 과제 (To-Do)
1. **프론트엔드 UI 연동**: `App.jsx`에서 조회 기간과 품목 코드를 입력받아 API를 호출하도록 UI 및 Fetch 로직 수정.
2. **데이터 파싱 정교화**: 정부 API가 돌려주는 단가 데이터를 실제 수량과 곱하여 총액을 산출하는 로직 구현.
3. **인증키 관리**: 소스코드에 하드코딩된 인증키를 환경변수(`.env`)로 분리.
