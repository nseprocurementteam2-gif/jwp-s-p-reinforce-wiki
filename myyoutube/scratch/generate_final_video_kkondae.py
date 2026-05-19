# -*- coding: utf-8 -*-
import os
from moviepy import ImageClip, concatenate_videoclips, CompositeVideoClip, AudioFileClip
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# 경로 설정
OUTPUT_DIR = r"c:\Users\NSE\.connect-ai-brain\myyoutube"
SCRATCH_DIR = os.path.join(OUTPUT_DIR, "scratch")

# 생성된 고품질 3D 씬 이미지들 (9:16 비율)
images = [
    r"C:\Users\NSE\.gemini\antigravity\brain\1193b810-2fed-4de3-9c18-3c08ee8a03a6\kkondae_scene_1_1779154333238.png",
    r"C:\Users\NSE\.gemini\antigravity\brain\1193b810-2fed-4de3-9c18-3c08ee8a03a6\kkondae_scene_2_1779154351452.png",
    r"C:\Users\NSE\.gemini\antigravity\brain\1193b810-2fed-4de3-9c18-3c08ee8a03a6\kkondae_scene_3_1779154368546.png",
    r"C:\Users\NSE\.gemini\antigravity\brain\1193b810-2fed-4de3-9c18-3c08ee8a03a6\kkondae_scene_4_1779154390794.png",
    r"C:\Users\NSE\.gemini\antigravity\brain\1193b810-2fed-4de3-9c18-3c08ee8a03a6\kkondae_scene_5_1779154408844.png"
]

# 장면별 듀레이션 설정 (총합 52.6초 - 음원 길이와 완벽 매칭)
durations = [11.0, 11.0, 10.0, 10.0, 10.6]

# 자막 데이터 설정 (노란색 메인 자막 단일 구성)
subtitles = [
    "기적 같은 칼퇴, 해보셨나요?",
    "저만의 진짜 하루가 시작",
    "성과 위주로 공부하면 일이 놀이",
    "이미지 생성 AI로 창작",
    "꼰대 부장에서 AI 마스터"
]

def create_subtitle_image(text, width=1080, height=1920):
    # 투명 RGBA 캔버스 생성
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 맑은 고딕 폰트 로드
    font_path = "C:/Windows/Fonts/malgunbd.ttf"
    if not os.path.exists(font_path):
        font_path = "C:/Windows/Fonts/malgun.ttf"
        
    try:
        font_main = ImageFont.truetype(font_path, 40)  # 한 줄 자막 가독성 강화를 위해 크기를 40으로 확대
    except:
        font_main = ImageFont.load_default()

    # 자막 상자 설정 (한 줄이므로 컴팩트하게 100px 높이로 축소)
    box_width = 960
    box_height = 100
    rect_x_start = (width - box_width) // 2  # 60px
    rect_y_start = height - box_height - 210  # 하단 여백 보정
    rect_x_end = rect_x_start + box_width
    rect_y_end = rect_y_start + box_height
    
    # 세련된 어두운 회색의 반투명 둥근 사각형 배경 생성
    try:
        draw.rounded_rectangle([rect_x_start, rect_y_start, rect_x_end, rect_y_end], radius=15, fill=(20, 20, 20, 210))
    except AttributeError:
        draw.rectangle([rect_x_start, rect_y_start, rect_x_end, rect_y_end], fill=(20, 20, 20, 210))

    # 텍스트 렌더링 및 정중앙 배치 정렬
    bbox_main = draw.textbbox((0, 0), text, font=font_main)
    main_w = bbox_main[2] - bbox_main[0]
    main_h = bbox_main[3] - bbox_main[1]
    main_x = (width - main_w) // 2
    main_y = rect_y_start + (box_height - main_h) // 2 - 4  # 세로 정중앙 미세 보정
    draw.text((main_x, main_y), text, font=font_main, fill=(255, 220, 0, 255))
    
    return np.array(img)


def generate_video():
    clips = []
    
    print("[PROCESS] Starting 9:16 Short Video generation...")
    for i in range(len(images)):
        if not os.path.exists(images[i]):
            print(f"[ERROR] Image not found: {images[i]}")
            return
            
        print(f"[SCENE {i+1}] Loading and processing ({durations[i]}s)...")
        # 배경 이미지 클립 로드 및 9:16 해상도 (1080x1920) 리사이즈
        img_clip = ImageClip(images[i]).with_duration(durations[i]).resized((1080, 1920))
        
        # Pillow를 활용한 1080x1920 자막 레이어 생성 및 클립화
        sub_img = create_subtitle_image(subtitles[i], width=1080, height=1920)
        sub_clip = ImageClip(sub_img).with_duration(durations[i])
        
        # 이미지와 자막 합성
        composite = CompositeVideoClip([img_clip, sub_clip], size=(1080, 1920))
        clips.append(composite)
        
    print("[INFO] Concatenating all scenes...")
    final_video = concatenate_videoclips(clips, method="compose")
    
    # 음원 오디오 파일 로드
    audio_path = os.path.join(OUTPUT_DIR, "꼰대 부장의 이중생활 .wav")
    if not os.path.exists(audio_path):
        print(f"[ERROR] Audio file not found at: {audio_path}")
        return
        
    print(f"[AUDIO] Merging audio track: {audio_path}")
    audio_clip = AudioFileClip(audio_path)
    
    # 비디오에 오디오 추가
    final_video = final_video.with_audio(audio_clip)
    
    # 최종 결과물 저장 경로
    output_path = os.path.join(OUTPUT_DIR, "꼰대_부장의_이중생활_마스터.mp4")
    
    print("[RENDER] Encoding 9:16 MP4 video...")
    final_video.write_videofile(
        output_path, 
        fps=24, 
        codec="libx264", 
        audio_codec="aac",
        temp_audiofile=os.path.join(SCRATCH_DIR, "temp-audio-kkondae.m4a"),
        remove_temp=True
    )
    print(f"[SUCCESS] Video successfully generated at: {output_path}")

if __name__ == "__main__":
    if not os.path.exists(SCRATCH_DIR):
        os.makedirs(SCRATCH_DIR)
    generate_video()
