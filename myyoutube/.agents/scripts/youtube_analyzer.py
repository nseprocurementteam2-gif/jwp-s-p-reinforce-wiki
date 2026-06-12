# .agents/scripts/youtube_analyzer.py
import os
import sys
from googleapiclient.discovery import build

# dotenv 로드 시도 (패키지가 없을 경우 대비 예외처리)
try:
    from dotenv import load_dotenv
    # 루트 디렉토리의 .env 파일을 로드하기 위해 경로 탐색 시도
    # 스크립트 위치가 .agents/scripts/ 이므로 두 단계 상위 디렉토리를 기준으로도 로드
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    env_path = os.path.join(base_dir, '.env')
    if os.path.exists(env_path):
        load_dotenv(dotenv_path=env_path)
    else:
        load_dotenv()
except ImportError:
    pass

# 터미널 출력 인코딩 설정 (Windows 환경 대응)
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

def main():
    # 1. 환경 변수에서 API 키와 채널 ID 가져오기
    # YOUTUBE_TARGET_CHANNEL_ID가 없으면 기존 .env 파일의 CHANNEL_ID도 확인
    api_key = os.environ.get("YOUTUBE_API_KEY")
    channel_id = os.environ.get("YOUTUBE_TARGET_CHANNEL_ID") or os.environ.get("CHANNEL_ID")

    if not api_key or not channel_id:
        print("❌ 오류: YOUTUBE_API_KEY 또는 YOUTUBE_TARGET_CHANNEL_ID 환경 변수가 설정되지 않았습니다.")
        sys.exit(1)

    youtube = build("youtube", "v3", developerKey=api_key)
    print(f"🚀 채널 분석 시작... (Target ID/Handle: {channel_id})\n")

    # 2. 채널의 최근 영상(업로드 재생목록) 가져오기
    # 채널 ID가 핸들(@) 형식일 때와 일반 ID 형식일 때 구분하여 처리
    try:
        if channel_id.startswith('@'):
            channel_req = youtube.channels().list(part="contentDetails", forHandle=channel_id)
        else:
            channel_req = youtube.channels().list(part="contentDetails", id=channel_id)
        channel_res = channel_req.execute()
    except Exception as e:
        print(f"❌ API 호출 중 오류가 발생했습니다: {e}")
        sys.exit(1)

    if not channel_res.get("items"):
        print("❌ 채널을 찾을 수 없습니다. 채널 ID 또는 핸들을 확인해 주세요.")
        return

    uploads_playlist_id = channel_res["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    playlist_req = youtube.playlistItems().list(
        part="snippet",
        playlistId=uploads_playlist_id,
        maxResults=5 # 최신 영상 5개만
    )
    playlist_res = playlist_req.execute()

    # 3. 각 영상의 제목 및 댓글 수집
    for item in playlist_res.get("items", []):
        video_id = item["snippet"]["resourceId"]["videoId"]
        video_title = item["snippet"]["title"]
        print(f"🎬 영상: {video_title}")

        # 영상 조회수, 좋아요 가져오기
        stat_req = youtube.videos().list(part="statistics", id=video_id)
        stat_res = stat_req.execute()
        stats = stat_res["items"][0]["statistics"]
        print(f" 📊 조회수: {stats.get('viewCount', 0)}, 좋아요: {stats.get('likeCount', 0)}")

        # 댓글 가져오기 (최대 10개)
        try:
            comment_req = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                order="relevance",
                maxResults=10
            )
            comment_res = comment_req.execute()
            print(" 💬 주요 댓글:")
            for c_item in comment_res.get("items", []):
                comment_text = c_item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                print(f" - {comment_text}")
        except Exception as e:
            print(" 💬 댓글을 가져올 수 없습니다 (댓글 사용 중지 등).")
        print("-" * 50)

    print("\n✅ 데이터 추출 완료! 위 텍스트를 바탕으로 시청자 니즈를 분석하고 기획안을 도출하세요.")

if __name__ == "__main__":
    main()
