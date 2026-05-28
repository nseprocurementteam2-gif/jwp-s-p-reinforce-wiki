# -*- coding: utf-8 -*-
import os
from moviepy import ImageClip, concatenate_videoclips, CompositeVideoClip, AudioFileClip
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# 경로 설정
OUTPUT_DIR = r"c:\Users\NSE\.connect-ai-brain\myyoutube"
SCRATCH_DIR = os.path.join(OUTPUT_DIR, "scratch")

def create_subtitle_image(texts, width=1080, height=1080):
    # 1. 완전 투명한 RGBA 캔버스 생성
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 2. 프리미엄 반투명 자막 배경 박스 그리기 (메인 단독이므로 세로폭 100px로 슬림하게 구성)
    box_width = 960
    box_height = 100
    rect_x_start = (width - box_width) // 2  # 60px
    rect_y_start = height - box_height - 80  # 900px
    rect_x_end = rect_x_start + box_width    # 1020px
    rect_y_end = rect_y_start + box_height   # 1000px
    
    # 둥근 모서리 반경 15px
    try:
        draw.rounded_rectangle([rect_x_start, rect_y_start, rect_x_end, rect_y_end], radius=15, fill=(20, 20, 20, 205))
    except AttributeError:
        draw.rectangle([rect_x_start, rect_y_start, rect_x_end, rect_y_end], fill=(20, 20, 20, 205))
    
    # 3. 프리미엄 윈도우 폰트 로드
    font_path = r"C:\Windows\Fonts\malgunbd.ttf"  # 맑은 고딕 Bold
    if not os.path.exists(font_path):
        font_path = "C:/Windows/Fonts/malgun.ttf"
        
    try:
        font_main = ImageFont.truetype(font_path, 34)  # 메인 키워드 크기 (1080 규격 최적화)
    except:
        font_main = ImageFont.load_default()
    
    # 4. 메인 텍스트만 박스 정중앙에 정렬하여 그리기
    main_text = texts[0]
    bbox_main = draw.textbbox((0, 0), main_text, font=font_main)
    main_w = bbox_main[2] - bbox_main[0]
    main_h = bbox_main[3] - bbox_main[1]
    
    main_x = (width - main_w) // 2
    # 박스 내부 세로 중앙 정렬 공식
    main_y = rect_y_start + (box_height - main_h) // 2 - 3
    
    # 메인 자막 (황금 옐로우 포인트 컬러: RGB 255, 220, 0)
    draw.text((main_x, main_y), main_text, font=font_main, fill=(255, 220, 0, 255))
    
    return np.array(img)

def generate_video():
    print("[INFO] Video rendering pipeline started.")
    
    # 1. 원본 이미지 경로 설정 (두 번째 이미지 교체 완료)
    image_paths = [
        r"C:\Users\NSE\.gemini\antigravity\brain\0762553d-b270-49dc-b27e-05afba5057bd\scene_1_hook_1779082600288.png",
        r"C:\Users\NSE\.gemini\antigravity\brain\0762553d-b270-49dc-b27e-05afba5057bd\scene_2_barrier_v2_1779083343735.png",
        r"C:\Users\NSE\.gemini\antigravity\brain\0762553d-b270-49dc-b27e-05afba5057bd\scene_3_turningpoint_1779082635703.png",
        r"C:\Users\NSE\.gemini\antigravity\brain\0762553d-b270-49dc-b27e-05afba5057bd\scene_4_efficiency_1779082657339.png",
        r"C:\Users\NSE\.gemini\antigravity\brain\0762553d-b270-49dc-b27e-05afba5057bd\scene_5_outro_1779082674507.png"
    ]
    
    # 2. 장면별 자막 정보 매핑 (총합: 44.40초, 메인 텍스트만 활용)
    scenes_data = [
        {
            "texts": ['"부장님, 아직도 이 두꺼운 보고서 직접 다 읽으세요?"'],
            "duration": 7.0
        },
        {
            "texts": ["AI? 그건 MZ세대나 쓰는 거 아닌가..."],
            "duration": 8.0
        },
        {
            "texts": ["수백 장짜리 PDF를 그냥 던져봤더니?"],
            "duration": 10.0
        },
        {
            "texts": ["3시간 걸리던 업무 -> 단 5분 컷!"],
            "duration": 9.0
        },
        {
            "texts": ['"질문만 하세요. AI가 다 해줍니다."'],
            "duration": 10.4  # 총 44.4초 맞춤
        }
    ]
    
    clips = []
    
    for i, (img_path, scene) in enumerate(zip(image_paths, scenes_data)):
        if not os.path.exists(img_path):
            print(f"[ERROR] Image not found: {img_path}")
            return
            
        print(f"[PROCESS] Scene {i+1} starts... ({scene['duration']}s)")
        
        # 1024x1024 이미지를 로드하여 1080x1080 크기로 리사이즈 및 듀레이션 부여 (MoviePy v2)
        img_clip = ImageClip(img_path).with_duration(scene["duration"]).resized((1080, 1080))
        
        # 고대비 하단 중앙 자막 이미지 생성 및 클립화 (MoviePy v2)
        sub_img = create_subtitle_image(scene["texts"], width=1080, height=1080)
        sub_clip = ImageClip(sub_img).with_duration(scene["duration"])
        
        # 이미지 클립과 자막 클립 오버레이 합성 (MoviePy v2)
        composite = CompositeVideoClip([img_clip, sub_clip], size=(1080, 1080))
        clips.append(composite)
        
    print("[INFO] Concatenating all scenes...")
    video_concat = concatenate_videoclips(clips, method="compose")
    
    # 3. 오디오 음원 트랙 결합
    audio_path = os.path.join(OUTPUT_DIR, "저는 AI랑 대화해서 퇴근합니다.wav")
    if os.path.exists(audio_path):
        print(f"[AUDIO] Merging audio track: {audio_path}")
        audio_clip = AudioFileClip(audio_path)
        video_concat = video_concat.with_audio(audio_clip)
    else:
        print("[WARNING] WAV audio file not found. Exporting silent video.")
        
    # 4. 최종 동영상 파일 저장 경로
    output_video_path = os.path.join(OUTPUT_DIR, "i_talk_to_ai_and_go_home.mp4")
    print(f"[RENDER] Encoding video: {output_video_path}")
    
    video_concat.write_videofile(
        output_video_path,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        temp_audiofile=os.path.join(SCRATCH_DIR, "temp-audio-talk.m4a"),
        remove_temp=True
    )
    print(f"[SUCCESS] Video file created: {output_video_path}")

if __name__ == "__main__":
    if not os.path.exists(SCRATCH_DIR):
        os.makedirs(SCRATCH_DIR)
    generate_video()
