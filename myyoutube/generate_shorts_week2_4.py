# generate_shorts_week2_4.py
# 50대 골퍼를 위한 코킹과 힌지 구분 쇼츠 자동 생성 스크립트

import os
import sys
import asyncio
import textwrap
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips
import edge_tts

# 터미널 출력 인코딩 설정 (Windows 대응)
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

base_dir = r"c:\Users\NSE\.connect-ai-brain\myyoutube"
# 신규 AI 분석 그래픽이 적용된 이미지가 생성된 Artifact 폴더 경로 지정
brain_dir = r"C:\Users\NSE\.gemini\antigravity-ide\brain\a251b1bd-485d-4684-b2a7-5fe8ff60fbc7"
scratch_dir = os.path.join(base_dir, "scratch")
os.makedirs(scratch_dir, exist_ok=True)

# 씬 정보 정의 (이미지 파일 경로 및 대본 매핑)
scenes_data = [
    {
        "img": os.path.join(brain_dir, "cocking_v2_scene_one_1781650153983.png"),
        "subtitle": "코킹과 힌지, 헷갈리지 마세요!",
        "narration": "백스윙 때 손목을 어떻게 꺾어야 할지 헷갈리시죠? 가슴 높이를 기준으로 코킹과 힌지를 나누면 골프가 쉬워집니다."
    },
    {
        "img": os.path.join(brain_dir, "cocking_v2_scene_two_1781650166621.png"),
        "subtitle": "코킹은 위아래 수직 꺾임!",
        "narration": "코킹은 손목을 위아래 즉 수직 방향으로 꺾어주는 동작입니다. 백스윙 올라갈 때 가볍게 위로 접어 지렛대 힘을 만듭니다."
    },
    {
        "img": os.path.join(brain_dir, "cocking_v2_scene_three_1781650179382.png"),
        "subtitle": "힌지는 좌우 수평 접힘!",
        "narration": "반면 힌지는 손등이 뒤로 젖혀지듯 양옆 즉 수평으로 접히는 동작입니다. 백스윙에서 페이스 면을 스퀘어로 유지하는 비결입니다."
    },
    {
        "img": os.path.join(brain_dir, "cocking_v2_scene_four_1781650190635.png"),
        "subtitle": "가슴 높이에서 손목 체크",
        "narration": "클럽이 가슴 높이에 왔을 때, 왼 손목은 코킹으로 단단히 꺾여 있고 오른 손등은 힌지로 쟁반을 받치듯 접혀 있는지 확인하세요."
    },
    {
        "img": os.path.join(brain_dir, "cocking_v2_scene_five_1781650202169.png"),
        "subtitle": "정확한 궤적과 비거리 상승!",
        "narration": "코킹과 힌지의 완벽한 조화가 이루어지면 헤드 페이스가 흐트러지지 않아 스윙 궤도가 정밀해지고 강인한 비거리가 만들어집니다."
    }
]

output_path = os.path.join(base_dir, "코킹_힌지_구분_쇼츠.mp4")
font_path = r"C:\Windows\Fonts\malgunbd.ttf"  # Windows 맑은 고딕 볼드 폰트
voice = "ko-KR-InJoonNeural"  # 50대 남성 톤의 목소리

async def generate_tts(text, file_path):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(file_path)
    print(f"TTS 생성 완료: {file_path}")

def add_subtitle(image_path, text, output_img_path):
    if not os.path.exists(image_path):
        print(f"오류: 이미지 파일 누락 - {image_path}")
        sys.exit(1)
        
    img = Image.open(image_path)
    width, height = img.size
    draw = ImageDraw.Draw(img)
    
    # 9:16 비디오 해상도에 맞춘 자막 폰트 크기 계산
    font_size = int(height * 0.045)
    
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()
        print("경고: 한글 폰트를 불러오지 못해 기본 폰트를 사용합니다.")
    
    # 텍스트 줄바꿈 처리
    text = "\n".join(textwrap.wrap(text, width=15))
    
    try:
        text_bbox = draw.multiline_textbbox((0, 0), text, font=font, align='center')
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
    except AttributeError:
        text_width, text_height = draw.textsize(text, font=font)
        
    bar_width = int(width * 0.85)
    bar_height = int(text_height * 1.8)
    bar_x1 = int((width - bar_width) / 2)
    bar_y1 = int(height * 0.82)
    bar_x2 = bar_x1 + bar_width
    bar_y2 = bar_y1 + bar_height
    
    # 반투명 배경 바 그리기 (투명도 180)
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rounded_rectangle([bar_x1, bar_y1, bar_x2, bar_y2], radius=20, fill=(0, 0, 0, 180))
    
    img = img.convert('RGBA')
    img = Image.alpha_composite(img, overlay).convert('RGB')
    
    # 노란색 자막 텍스트 렌더링
    draw_rgb = ImageDraw.Draw(img)
    text_x = bar_x1 + (bar_width - text_width) // 2
    text_y = bar_y1 + (bar_height - text_height) // 2 - int(text_height * 0.1)
    draw_rgb.multiline_text((text_x, text_y), text, fill=(255, 235, 59), font=font, align='center')
    
    img.save(output_img_path)
    print(f"자막 이미지 저장 완료: {output_img_path}")

async def main():
    processed_clips = []
    
    print("--- 1단계: TTS 오디오 및 자막 합성 이미지 생성 ---")
    for i, scene in enumerate(scenes_data):
        audio_file = os.path.join(scratch_dir, f"audio_shorts_w2_s4_scene_{i}.mp3")
        await generate_tts(scene["narration"], audio_file)
        
        temp_img_path = os.path.join(scratch_dir, f"temp_shorts_w2_s4_scene_{i}.png")
        add_subtitle(scene["img"], scene["subtitle"], temp_img_path)
        
        audio_clip = AudioFileClip(audio_file)
        duration = audio_clip.duration
        print(f"씬 {i+1} 재생 시간: {duration:.2f}초")
        
        # MoviePy v2.x 대응 API 체이닝 적용
        clip = ImageClip(temp_img_path).with_duration(duration).with_audio(audio_clip)
        processed_clips.append(clip)
        
    print("\n--- 2단계: 비디오 조립 및 렌더링 ---")
    video = concatenate_videoclips(processed_clips, method="compose")
    
    print(f"최종 비디오 생성 시작: {output_path}")
    video.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')
    print(f"\n✅ 완료: 코킹/힌지 구분 쇼츠 비디오가 저장되었습니다 -> {output_path}")

if __name__ == "__main__":
    asyncio.run(main())
