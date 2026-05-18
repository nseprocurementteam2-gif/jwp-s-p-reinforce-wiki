
import os
from moviepy import ImageClip, concatenate_videoclips, ColorClip, CompositeVideoClip
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# 경로 설정
BRAIN_DIR = r"C:\Users\NSE\.gemini\antigravity\brain\23faa1fb-ecd0-42b2-b2c8-4b1492e1044d"
OUTPUT_DIR = r"c:\Users\NSE\.connect-ai-brain\myyoutube"
SCRATCH_DIR = os.path.join(OUTPUT_DIR, "scratch")

# 이미지 파일 경로 (실제 생성된 파일명으로 업데이트 필요)
images = [
    os.path.join(BRAIN_DIR, "scene_1_opening_1778830200506.png"),
    os.path.join(BRAIN_DIR, "scene_2_concept_1778830215731.png"),
    os.path.join(BRAIN_DIR, "scene_3_practice_1778830231352.png"),
    os.path.join(BRAIN_DIR, "scene_4_effect_1778830248163.png"),
    os.path.join(BRAIN_DIR, "scene_5_closing_1778830265526.png")
]

# 타임스탬프 (초 단위)
durations = [15, 25, 15, 17, 18] # 총 90초

# 자막 데이터
subtitles = [
    ["오늘 읽어야 할 자료 100개", "내 대신 일하는 자동 요리법"],
    ["시작 벨소리 (Trigger)", "자동 로봇의 할 일 (Action)"],
    ["Gmail → GPT → Notion", "3단계 기적의 프로세스"],
    ["실행까지 해주는", "진짜 자동화"],
    ["오늘 딱 하나만 자동화 해보기", "지금 바로 시작하기"]
]

def create_subtitle_image(texts, width=1920, height=1080):
    # 자막 이미지를 생성 (투명 배경)
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 한글 폰트 설정 (윈도우 기본 폰트 사용)
    font_path = "C:/Windows/Fonts/malgun.ttf" # 맑은 고딕
    try:
        font_main = ImageFont.truetype(font_path, 40) # 메인 키워드 크기
        font_sub = ImageFont.truetype(font_path, 25)  # 서브 키워드 크기
    except:
        font_main = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    # 자막 배경 (회색 투명 바탕) - 중앙 배치
    padding = 20
    box_width = 800
    box_height = 150
    rect_x_start = (width - box_width) // 2
    rect_y_start = (height - box_height) // 2
    rect_x_end = rect_x_start + box_width
    rect_y_end = rect_y_start + box_height
    
    draw.rectangle([rect_x_start, rect_y_start, rect_x_end, rect_y_end], fill=(50, 50, 50, 180))

    # 텍스트 그리기 - 중앙 정렬
    y_offset = rect_y_start + 30
    for i, text in enumerate(texts):
        current_font = font_main if i == 0 else font_sub
        bbox = draw.textbbox((0, 0), text, font=current_font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        draw.text((x, y_offset), text, font=current_font, fill=(255, 255, 255, 255))
        y_offset += 50

    return np.array(img)

def generate_video():
    clips = []
    
    for i in range(len(images)):
        # 배경 이미지 클립 (크기 조절 추가)
        img_clip = ImageClip(images[i]).with_duration(durations[i]).resized(width=1920, height=1080)
        
        # 자막 이미지 생성
        sub_img = create_subtitle_image(subtitles[i])
        sub_clip = ImageClip(sub_img).with_duration(durations[i])
        
        # 합성
        composite = CompositeVideoClip([img_clip, sub_clip])
        clips.append(composite)

    # 전체 영상 합치기
    final_video = concatenate_videoclips(clips, method="compose")
    
    # 오디오 제외하고 저장
    output_path = os.path.join(OUTPUT_DIR, "ai_assistant_automation_90s.mp4")
    final_video.write_videofile(output_path, fps=24, audio=False, codec="libx264")
    print(f"Video generated at: {output_path}")

if __name__ == "__main__":
    generate_video()
