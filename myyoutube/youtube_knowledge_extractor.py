import os
import sys
from dotenv import load_dotenv
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from google import genai
from google.genai import types
import re

# 터미널 출력 인코딩 오류 방지
sys.stdout.reconfigure(encoding='utf-8')

# 환경 변수 로드
load_dotenv()

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
CHANNEL_ID = os.getenv('CHANNEL_ID')

OUTPUT_DIR = r"c:\Users\NSE\.connect-ai-brain\osidian 지식화"

def check_env():
    missing = []
    if not YOUTUBE_API_KEY: missing.append('YOUTUBE_API_KEY')
    if not GEMINI_API_KEY: missing.append('GEMINI_API_KEY')
    if not CHANNEL_ID: missing.append('CHANNEL_ID')
    if missing:
        print(f"오류: 환경 변수가 누락되었습니다: {', '.join(missing)}")
        print("'.env' 파일에 정보를 입력해주세요.")
        sys.exit(1)

def get_channel_videos(youtube, channel_id):
    """채널의 모든 동영상 ID와 메타데이터를 가져옵니다."""
    videos = []
    try:
        # 1. 채널의 '업로드' 재생목록 ID 찾기
        if channel_id.startswith('@'):
            request = youtube.channels().list(
                part="contentDetails",
                forHandle=channel_id
            )
        else:
            request = youtube.channels().list(
                part="contentDetails",
                id=channel_id
            )
        response = request.execute()
        
        if not response.get('items'):
            print("채널을 찾을 수 없습니다. 채널 ID를 확인해주세요.")
            return videos
            
        uploads_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        
        # 2. 재생목록에서 동영상 가져오기 (페이지네이션 처리)
        next_page_token = None
        while True:
            playlist_request = youtube.playlistItems().list(
                part="snippet",
                playlistId=uploads_playlist_id,
                maxResults=50,
                pageToken=next_page_token
            )
            playlist_response = playlist_request.execute()
            
            for item in playlist_response['items']:
                video_id = item['snippet']['resourceId']['videoId']
                title = item['snippet']['title']
                description = item['snippet']['description']
                videos.append({
                    'video_id': video_id,
                    'title': title,
                    'description': description
                })
                
            next_page_token = playlist_response.get('nextPageToken')
            if not next_page_token:
                break
                
        return videos
    except Exception as e:
        print(f"유튜브 데이터 가져오기 오류: {e}")
        return []

def get_video_transcript(video_id):
    """영상의 자막을 추출합니다. (한국어 우선)"""
    try:
        tlist = YouTubeTranscriptApi().list(video_id)
        transcript = tlist.find_transcript(['ko', 'en']).fetch()
        formatter = TextFormatter()
        text_formatted = formatter.format_transcript(transcript)
        return text_formatted
    except Exception as e:
        print(f"  [{video_id}] 자막 추출 실패: {e}")
        return ""

def sanitize_filename(filename):
    """파일명으로 사용할 수 없는 문자를 제거합니다."""
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def generate_knowledge_markdown(client, title, description, transcript):
    """Gemini를 사용하여 옵시디언 포맷 마크다운을 생성합니다."""
    
    prompt = f"""
다음은 유튜브 영상의 정보입니다. 이 정보를 분석하여 아래의 구조화된 마크다운 포맷으로 변환해주세요.
반드시 아래의 양식을 정확히 지켜야 하며, 설명은 모두 한국어로 작성해주세요.

[영상 정보]
제목: {title}
설명: {description}
자막: {transcript if transcript else '자막 없음'}

[출력 양식]
# [[Title of Concept/Entity]]

## 📌 Brief Summary
(이 주제에 대한 간결한 1~2문장의 정의)

## 📖 Core Content
(원본 출처를 바탕으로 상세하게 종합한 내용)

## 🔗 Knowledge Connections
- **Related Topics:** [[관련-주제-A]], [[관련-주제-B]]
- **Projects/Contexts:** [[관련-프로젝트-이름]]
- **Contradictions/Notes:** (주목할 만한 예외사항이나 주의점 등)

---
*Last updated: {{오늘 날짜}}*
"""
    try:
        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        print(f"Gemini API 오류: {e}")
        return ""

def main():
    check_env()
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    print(f"유튜브 클라이언트 초기화 중...")
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    
    print(f"Gemini 클라이언트 초기화 중...")
    gemini_client = genai.Client(api_key=GEMINI_API_KEY)
    
    print(f"채널 ID({CHANNEL_ID})에서 영상 목록을 가져옵니다...")
    videos = get_channel_videos(youtube, CHANNEL_ID)
    print(f"총 {len(videos)}개의 영상을 찾았습니다.\n")
    
    for i, video in enumerate(videos):
        print(f"[{i+1}/{len(videos)}] 처리 중: {video['title']}")
        
        transcript = get_video_transcript(video['video_id'])
        if not transcript:
            print("  자막이 없어 제목과 설명글만으로 지식화를 시도합니다.")
            
        markdown_content = generate_knowledge_markdown(
            gemini_client, 
            video['title'], 
            video['description'], 
            transcript
        )
        
        if markdown_content:
            # 안전한 파일명 생성 (제목에서 앞 30자 정도만 사용)
            safe_title = sanitize_filename(video['title'])[:30].strip()
            filename = f"{safe_title}.md"
            filepath = os.path.join(OUTPUT_DIR, filename)
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(markdown_content)
            print(f"  -> 저장 완료: {filepath}")
        else:
            print(f"  -> 처리 실패")

if __name__ == "__main__":
    main()
