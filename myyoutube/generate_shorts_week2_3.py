# generate_shorts_week2_3.py
# 50대 골퍼를 위한 치킨윙 방지 및 엘보 부상 방지 쇼츠 자동 생성 스크립트

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
brain_dir = r"C:\Users\NSE\.gemini\antigravity-ide\brain\e501f0fd-3960-4f82-9a5f-96427d42d668"
scratch_dir = os.path.join(base_dir, "scratch")
os.makedirs(scratch_dir, exist_ok=True)

# 씬 정보 정의 (이미지 파일 경로 및 대본 매핑 수정 완료)
scenes_data = [
    {
        "img": os.path.join(brain_dir, "shorts_w2_s3_p1_1781217765384.png"),
        "subtitle": "골프 친 뒤 팔꿈치 아프신가요?",
        "narration": "라운드 돌고 나면 왼쪽 팔꿈치에 엘보 통증이 오시나요? 임팩트 후 왼팔이 당겨지며 바깥으로 벌어지는 치킨윙 동작이 부상과 비거리 저하의 주범입니다."
    },
    {
        "img": os.path.join(brain_dir, "shorts_w2_s3_p2_1781217778918.png"),
        "subtitle": "어드레스 시 양팔꿈치를 모으세요",
        "narration": "치킨윙을 방지하려면 셋업 자세부터 잡아야 합니다. 양팔 안쪽의 접히는 부분이 서로 마주 보게 하고, 팔꿈치 간격을 좁혀 삼각형을 단단하게 유지하세요."
    },
    {
        "img": os.path.join(brain_dir, "shorts_w2_s3_p3_1781217790823.png"),
        "subtitle": "임팩트 후 왼팔꿈치는 아래를 향하게",
        "narration": "그리고 임팩트 이후 팔이 뻗어 나갈 때, 왼팔 꿈치의 뾰족한 끝 부분이 하늘이 아니라 지면을 바라보며 자연스럽게 접히도록 회전시켜 줍니다."
    },
    {
        "img": os.path.join(brain_dir, "shorts_w2_s3_p4_1781217804331.png"),
        "subtitle": "양 겨드랑이에 수건 끼고 스윙",
        "narration": "가장 확실한 훈련법은 양쪽 겨드랑이에 수건을 가볍게 끼워두고, 하프 스윙을 하며 수건이 바닥에 떨어지지 않게 회전하는 연습을 반복하는 것입니다."
    },
    {
        "img": os.path.join(brain_dir, "shorts_w2_s3_p5_1781217818366.png"),
        "subtitle": "치킨윙 해결하고 부상 없이 싱글로!",
        "narration": "팔꿈치가 벌어지지 않고 모여 회전하면, 아프던 엘보 통증이 씻은 듯이 사라지고 피니시 라인이 깔끔해져 백점 만점의 스윙이 완성됩니다."
    }
]

output_path = os.path.join(base_dir, "치킨윙_방지_쇼츠.mp4")
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
    
    # 반투명 배경 바 그리기
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rounded_rectangle([bar_x1, bar_y1, bar_x2, bar_y2], radius=20, fill=(0, 0, 0, 180))
    
    img = img.convert('RGBA')
    img = Image.alpha_composite(img, overlay).convert('RGB')
    
    # 노란색 자막 텍스트 그리기
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
        audio_file = os.path.join(scratch_dir, f"audio_shorts_w2_s3_scene_{i}.mp3")
        await generate_tts(scene["narration"], audio_file)
        
        temp_img_path = os.path.join(scratch_dir, f"temp_shorts_w2_s3_scene_{i}.png")
        add_subtitle(scene["img"], scene["subtitle"], temp_img_path)
        
        audio_clip = AudioFileClip(audio_file)
        duration = audio_clip.duration
        print(f"씬 {i+1} 재생 시간: {duration:.2f}초")
        
        clip = ImageClip(temp_img_path).with_duration(duration).with_audio(audio_clip)
        processed_clips.append(clip)
        
    print("\n--- 2단계: 비디오 조립 및 렌더링 ---")
    video = concatenate_videoclips(processed_clips, method="compose")
    
    print(f"최종 비디오 생성 시작: {output_path}")
    video.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')
    print(f"\n✅ 완료: 쇼츠 비디오 3이 저장되었습니다 -> {output_path}")

if __name__ == "__main__":
    asyncio.run(main())
