@echo off
:: 코부장 대시보드 자동 시작 스크립트
echo [시스템] 코부장 비용 분석 시스템을 시작합니다...

:: 1. 프로젝트 폴더로 이동
cd /d "c:\Users\NSE\.connect-ai-brain\구매메인보드\dashboard-app"

:: 2. 기존 서버 프로세스 종료 (주의: 다른 Node 프로세스도 종료될 수 있으므로 주석 처리하거나 신중히 사용)
:: taskkill /f /im node.exe >nul 2>&1

:: 3. 서버 실행 (백그라운드/최소화)
start /min cmd /c "npm run dev"

:: 4. 서버 기동 대기 (5초)
timeout /t 5 /nobreak >nul

:: 5. 웹 브라우저로 대시보드 실행
start http://172.27.44.242:3037

echo [완료] 대시보드가 성공적으로 실행되었습니다.
