# -*- coding: utf-8 -*-
import os
from moviepy import ImageClip, concatenate_videoclips, CompositeVideoClip, AudioFileClip
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# 경로 설정
OUTPUT_DIR = r"c:\Users\NSE\.connect-ai-brain\myyoutube"
SCRATCH_DIR = os.path.join(OUTPUT_DIR, "scratch")

# 생성된 이미지 경로
images = [
    r"C:\Users\NSE\.gemini\antigravity\brain\0762553d-b270-49dc-b27e-05afba5057bd\scene_1_opening_1779079234605.png",
    r"C:\Users\NSE\.gemini\antigravity\brain\0762553d-b270-49dc-b27e-05afba5057bd\scene_2_visual_agent_1779079251669.png",
    r"C:\Users\NSE\.gemini\antigravity\brain\0762553d-b270-49dc-b27e-05afba5057bd\scene_3_calculation_agent_1779079269061.png",
    r"C:\Users\NSE\.gemini\antigravity\brain\0762553d-b270-49dc-b27e-05afba5057bd\scene_4_law_agent_1779079288872.png",
    r"C:\Users\NSE\.gemini\antigravity\brain\0762553d-b270-49dc-b27e-05afba5057bd\scene_5_report_agent_1779079307180.png"
]

# 장면별 듀레이션 설정 (총합: 48.08초로 오디오 길이와 정확히 싱크)
durations = [9.0, 9.0, 9.0, 9.0, 12.08]

# 자막 데이터 설정 (메인 타이틀, 서브 설명)
subtitles = [
    ["도면 검토 3일 → 단 10분!", "3일의 기적을 10분으로 압축하는 AI 설계 혁명"],
    ["[도면 인식] 심볼·치수 데이터화 완료!", "시각 지능 에이전트의 CAD 도면 3D 변환 및 구조화"],
    ["[수량 산출] 면적·체적 자동 계산 중...", "연산 및 코드 생성 에이전트의 자재 수량 자동 산출"],
    ["[법규 검토] 최신 법령 대조·위반 항목 탐지!", "법규 검토 에이전트의 건축 규정 실시간 교차 검증"],
    ["[최종 보고] 적합성 보고서 생성 완료!", "통합 보고 에이전트의 설계 적합성 대시보드 및 결과물 브리핑"]
]

def create_subtitle_image(texts, width=1080, height=1080):
    # 투명한 RGBA 이미지 생성
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 맑은 고딕 폰트 로드
    font_path = "C:/Windows/Fonts/malgunbd.ttf"  # Bold 버전 사용
    if not os.path.exists(font_path):
        font_path = "C:/Windows/Fonts/malgun.ttf"
        
    try:
        font_main = ImageFont.truetype(font_path, 34)  # 메인 키워드 크기 (1080 규격 최적화)
        font_sub = ImageFont.truetype(font_path, 21)   # 서브 설명 크기
    except:
        font_main = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    # 자막 상자 설정 (1080x1080 해상도의 하단 중앙에 배치)
    box_width = 960
    box_height = 150
    rect_x_start = (width - box_width) // 2
    # 하단 80px 띄우고 배치
    rect_y_start = height - box_height - 80
    rect_x_end = rect_x_start + box_width
    rect_y_end = rect_y_start + box_height
    
    # 세련된 어두운 회색의 반투명 둥근 사각형 배경 생성
    try:
        draw.rounded_rectangle([rect_x_start, rect_y_start, rect_x_end, rect_y_end], radius=15, fill=(20, 20, 20, 205))
    except AttributeError:
        draw.rectangle([rect_x_start, rect_y_start, rect_x_end, rect_y_end], fill=(20, 20, 20, 205))

    # 텍스트 렌더링 (중앙 정렬)
    # 첫 번째 줄: 메인 자막 (노란색 강조)
    main_text = texts[0]
    bbox_main = draw.textbbox((0, 0), main_text, font=font_main)
    main_w = bbox_main[2] - bbox_main[0]
    main_x = (width - main_w) // 2
    main_y = rect_y_start + 28
    draw.text((main_x, main_y), main_text, font=font_main, fill=(255, 220, 0, 255))  # 노란색 강조
    
    # 두 번째 줄: 서브 자막 (흰색)
    sub_text = texts[1]
    bbox_sub = draw.textbbox((0, 0), sub_text, font=font_sub)
    sub_w = bbox_sub[2] - bbox_sub[0]
    sub_x = (width - sub_w) // 2
    sub_y = main_y + 55
    draw.text((sub_x, sub_y), sub_text, font=font_sub, fill=(255, 255, 255, 255))  # 흰색
    
    return np.array(img)

def generate_video():
    clips = []
    
    print("비디오 클립 생성을 시작합니다...")
    for i in range(len(images)):
        if not os.path.exists(images[i]):
            print(f"오류: 이미지를 찾을 수 없습니다. 경로: {images[i]}")
            return
            
        # 배경 이미지 클립 로드 및 1080x1080 리사이즈 (1:1 비율로 강제 왜곡되지 않게 맞춤)
        img_clip = ImageClip(images[i]).with_duration(durations[i]).resized((1080, 1080))
        
        # 자막 이미지 생성 (1080x1080 규격) 및 오버레이 클립 생성
        sub_img = create_subtitle_image(subtitles[i], width=1080, height=1080)
        sub_clip = ImageClip(sub_img).with_duration(durations[i])
        
        # 이미지 클립과 자막 클립 합성 (명시적 1080x1080 크기 지정)
        composite = CompositeVideoClip([img_clip, sub_clip], size=(1080, 1080))
        clips.append(composite)
        print(f"장면 {i+1} 처리 완료 ({durations[i]}초)")

    # 모든 비디오 클립 순차 연결
    print("모든 비디오 클립을 연결하는 중...")
    final_video = concatenate_videoclips(clips, method="compose")
    
    # 음원 오디오 파일 로드
    audio_path = os.path.join(OUTPUT_DIR, "3일의 기적.wav")
    if not os.path.exists(audio_path):
        print(f"오류: 음원 파일을 찾을 수 없습니다. 경로: {audio_path}")
        return
        
    print("음원 오디오를 로드하여 병합하는 중...")
    audio_clip = AudioFileClip(audio_path)
    
    # 비디오에 오디오 추가
    final_video = final_video.with_audio(audio_clip)
    
    # 최종 결과물 저장 경로
    output_path = os.path.join(OUTPUT_DIR, "3days_miracle_ai_design.mp4")
    
    print("최종 동영상 파일 인코딩 및 내보내기 중...")
    final_video.write_videofile(
        output_path, 
        fps=24, 
        codec="libx264", 
        audio_codec="aac",
        temp_audiofile=os.path.join(SCRATCH_DIR, "temp-audio.m4a"),
        remove_temp=True
    )
    print(f"최종 동영상 생성 성공! 파일 위치: {output_path}")

if __name__ == "__main__":
    if not os.path.exists(SCRATCH_DIR):
        os.makedirs(SCRATCH_DIR)
    generate_video()
