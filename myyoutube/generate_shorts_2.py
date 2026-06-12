# generate_shorts_2.py
# 50대 골퍼를 위한 어프로치 뒤땅 방지 쇼츠 자동 생성 스크립트

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
brain_dir = r"C:\Users\NSE\.gemini\antigravity-ide\brain\68f36c99-f634-472d-ae03-a41b2d3f6de2"
scratch_dir = os.path.join(base_dir, "scratch")
os.makedirs(scratch_dir, exist_ok=True)

# 씬 정보 정의
scenes_data = [
    {
        "img": os.path.join(brain_dir, "shorts2_scene1_1780958271884.png"),
        "subtitle": "어프로치 뒤땅, 이제 그만!",
        "narration": "그린 주변에서 홀컵에 붙이려다 뒤땅이나 탑볼로 한 번에 갈 거리를 두세 번 만에 가신 적 많으시죠? 어프로치의 실수는 백프로 손목 흔들림에서 시작됩니다."
    },
    {
        "img": os.path.join(brain_dir, "shorts2_scene2_1780958283651.png"),
        "subtitle": "왼손목은 곧게, 오른손목 힌지!",
        "narration": "어프로치의 핵심은 핸드퍼스트 셋업입니다. 양손을 왼쪽 허벅지 안쪽에 위치시키고, 임팩트 이후 피니시까지 왼손목은 단단하게 펴고 오른손목은 살짝 접힌 각도를 굳건하게 유지해야 합니다."
    },
    {
        "img": os.path.join(brain_dir, "shorts2_scene3_1780958296764.png"),
        "subtitle": "손목 로테이션 절대 금지!",
        "narration": "거리가 가깝다고 임팩트 때 볼을 띄우려고 손목을 꺾어 올리면 무조건 뒤땅이나 탑볼이 납니다. 볼은 클럽 페이스의 누워있는 각도, 즉 로프트가 알아서 띄워주니 클럽을 믿으셔야 합니다."
    },
    {
        "img": os.path.join(brain_dir, "shorts2_scene4_1780958310221.png"),
        "subtitle": "시계추 모션 연습법",
        "narration": "어깨와 양팔이 만드는 Y자 삼각형을 가슴 앞에 그대로 유지한 채 시계추처럼 시선만 볼을 쳐다보며 왔다 갔다 회전하십시오. 손가락 힘은 빼고 팔통으로 쳐야 일정한 바운스 샷이 가능합니다."
    },
    {
        "img": os.path.join(brain_dir, "shorts2_scene5_1780958325216.png"),
        "subtitle": "핀 옆에 딱 붙는 짜릿함!",
        "narration": "손목 고정만 지키면 어느 라이에서든 일정한 터치가 나와 핀 옆에 공이 찰떡같이 붙게 됩니다. 숏게임을 지배하고 타수를 극적으로 줄여 완벽한 싱글 골퍼로 거듭나십시오."
    }
]

output_path = os.path.join(base_dir, "어프로치_뒤땅방지_쇼츠.mp4")
font_path = r"C:\Windows\Fonts\malgunbd.ttf"
voice = "ko-KR-InJoonNeural"

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
    
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rounded_rectangle([bar_x1, bar_y1, bar_x2, bar_y2], radius=20, fill=(0, 0, 0, 180))
    
    img = img.convert('RGBA')
    img = Image.alpha_composite(img, overlay).convert('RGB')
    
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
        audio_file = os.path.join(scratch_dir, f"audio_shorts2_scene_{i}.mp3")
        await generate_tts(scene["narration"], audio_file)
        
        temp_img_path = os.path.join(scratch_dir, f"temp_shorts2_scene_{i}.png")
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
    print(f"\n✅ 완료: 쇼츠 비디오 2가 저장되었습니다 -> {output_path}")

if __name__ == "__main__":
    asyncio.run(main())
