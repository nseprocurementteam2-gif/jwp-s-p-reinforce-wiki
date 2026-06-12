# generate_shorts_week2_1.py
# 50대 골퍼를 위한 눌려 맞는 아이언 임팩트 쇼츠 자동 생성 스크립트

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

# 씬 정보 정의 (이미지 파일 경로 및 대본 매핑)
scenes_data = [
    {
        "img": os.path.join(brain_dir, "shorts_w2_s1_p1_1781217635575.png"),
        "subtitle": "아이언 비거리 왜 안 날까요?",
        "narration": "아이언 비거리가 자꾸 줄고 걷어 올리는 샷이 나와 고민이신가요? 이는 임팩트 시 클럽 페이스가 열리거나 캐스팅이 일어났기 때문입니다."
    },
    {
        "img": os.path.join(brain_dir, "shorts_w2_s1_p2_1781217646783.png"),
        "subtitle": "손이 헤드보다 앞서는 핸드퍼스트",
        "narration": "해결책은 오직 하나, 임팩트 순간에 손이 헤드보다 무조건 앞서 나가는 핸드 퍼스트 자세를 확실히 만드는 것입니다."
    },
    {
        "img": os.path.join(brain_dir, "shorts_w2_s1_p3_1781217659762.png"),
        "subtitle": "왼발로 과감한 체중 이동!",
        "narration": "다운스윙 전환 시 과감하게 체중을 왼발로 보내며 공을 위에서 아래로 눌러 쳐야 진정한 정타를 맞출 수 있습니다."
    },
    {
        "img": os.path.join(brain_dir, "shorts_w2_s1_p4_1781217678354.png"),
        "subtitle": "동전이나 수건 뒤에 두고 연습",
        "narration": "볼 뒤 오 센티미터 지점에 수건이나 동전을 두고, 수건을 건드리지 않고 공만 바로 타격하는 연습을 하루 십분 반복해 보세요."
    },
    {
        "img": os.path.join(brain_dir, "shorts_w2_s1_p5_1781217690584.png"),
        "subtitle": "상위 1%의 짜릿한 아이언 손맛",
        "narration": "자세가 완성되면 로프트 각도대로 강력히 눌려 맞아, 짜릿한 손맛과 함께 압도적인 비거리와 정밀도를 경험하실 수 있습니다."
    }
]

output_path = os.path.join(base_dir, "아이언_임팩트_쇼츠.mp4")
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
        audio_file = os.path.join(scratch_dir, f"audio_shorts_w2_s1_scene_{i}.mp3")
        await generate_tts(scene["narration"], audio_file)
        
        temp_img_path = os.path.join(scratch_dir, f"temp_shorts_w2_s1_scene_{i}.png")
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
    print(f"\n✅ 완료: 쇼츠 비디오 1이 저장되었습니다 -> {output_path}")

if __name__ == "__main__":
    asyncio.run(main())
