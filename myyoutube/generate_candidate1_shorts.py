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
brain_dir = r"C:\Users\NSE\.gemini\antigravity-ide\brain\3b58852f-a46d-48c0-84e5-9aa35cecad4d"
scratch_dir = os.path.join(base_dir, "scratch")
os.makedirs(scratch_dir, exist_ok=True)

# 후보 1번 씬 정보 정의
scenes_data = [
    {
        "img": os.path.join(brain_dir, "slice_scene_1_1780642129578.png"),
        "subtitle": "슬라이스 지긋지긋하죠?",
        "narration": "연습장에서 아무리 세게 쳐도 자꾸 오른쪽으로 휘어지는 슬라이스 때문에 고민이십니까? 원인은 백스윙 때 손목 동작에 있습니다."
    },
    {
        "img": os.path.join(brain_dir, "slice_scene_2_1780642145755.png"),
        "subtitle": "손목 돌리지 마세요!",
        "narration": "테이크백 때 손목을 시계 방향으로 돌려버리면 헤드 페이스가 열리면서 결국 릴리즈 때 깎여 맞게 되어 슬라이스가 납니다."
    },
    {
        "img": os.path.join(brain_dir, "slice_scene_3_1780642163886.png"),
        "subtitle": "힌지는 손등 펴기",
        "narration": "가슴 높이까지 올릴 때 손목을 돌리지 말고, 왼손 등은 펴고 오른손목은 뒤로 꺾어주는 힌지 동작만 기억하십시오."
    },
    {
        "img": os.path.join(brain_dir, "slice_scene_4_1780642179047.png"),
        "subtitle": "10분만 연습하세요",
        "narration": "하루 10분씩 백스윙 탑에서 왼손등이 평평하게 펴져 있는지 거울로 체크하면 페이스가 닫혀 슬라이스가 즉시 고쳐집니다."
    },
    {
        "img": os.path.join(brain_dir, "slice_scene_5_1780642194813.png"),
        "subtitle": "똑바로 뻗어가는 샷!",
        "narration": "손목 회전 대신 올바른 코킹과 힌지만으로 부드럽게 쳐보십시오. 똑바로 뻗어가는 시원한 손맛을 느끼실 수 있습니다."
    }
]

output_path = os.path.join(base_dir, "후보1.mp4")
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
        print("경고: 지정된 한글 폰트를 로드할 수 없어 기본 폰트를 적용합니다.")
    
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
    print(f"자막 이미지 저장: {output_img_path}")

async def main():
    processed_clips = []
    
    print("--- 1단계: edge-tts 오디오 생성 및 자막 이미지 합성 ---")
    for i, scene in enumerate(scenes_data):
        audio_file = os.path.join(scratch_dir, f"audio_candidate1_scene_{i}.mp3")
        await generate_tts(scene["narration"], audio_file)
        
        temp_img_path = os.path.join(scratch_dir, f"temp_candidate1_scene_{i}.png")
        add_subtitle(scene["img"], scene["subtitle"], temp_img_path)
        
        audio_clip = AudioFileClip(audio_file)
        duration = audio_clip.duration
        print(f"씬 {i+1} 재생 시간: {duration:.2f}초")
        
        clip = ImageClip(temp_img_path).with_duration(duration).with_audio(audio_clip)
        processed_clips.append(clip)
        
    print("\n--- 2단계: 비디오 클립 병합 및 인코딩 ---")
    video = concatenate_videoclips(processed_clips, method="compose")
    
    print(f"최종 비디오 쓰기: {output_path}")
    video.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')
    print(f"\n✅ 성공: 최종 비디오 저장 완료 -> {output_path}")

if __name__ == "__main__":
    asyncio.run(main())
