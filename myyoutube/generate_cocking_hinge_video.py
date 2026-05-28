import os
import sys
import subprocess
from PIL import Image, ImageDraw, ImageFont

# 패키지 설치 확인
try:
    from moviepy import ImageClip, AudioFileClip, concatenate_videoclips
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "moviepy==2.0.0.dev2", "pillow"])
    from moviepy import ImageClip, AudioFileClip, concatenate_videoclips

try:
    import edge_tts
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "edge-tts"])

import asyncio

base_dir = r"c:\Users\NSE\.connect-ai-brain\myyoutube\cocking_hinge_shorts"
brain_dir = r"C:\Users\NSE\.gemini\antigravity-ide\brain\bddc8c21-2623-4632-b05a-0c9a5c2280b3"
scratch_dir = os.path.join(base_dir, "scratch")
os.makedirs(scratch_dir, exist_ok=True)

# 씬별 데이터베이스
scenes = [
    {"img": os.path.join(brain_dir, "scene1_consistent_address_1779929827732.png"), "duration": 10, "text": "코킹? 힌지? 헷갈리시죠?"},
    {"img": os.path.join(brain_dir, "scene2_consistent_cocking_1779929843806.png"), "duration": 10, "text": "왼손은 코킹! (위아래)"},
    {"img": os.path.join(brain_dir, "scene3_consistent_hinge_1779929859300.png"), "duration": 10, "text": "오른손은 힌지! (앞뒤)"},
    {"img": os.path.join(brain_dir, "scene4_consistent_halfswing_1779929882840.png"), "duration": 10, "text": "가슴 높이에서 완성!"},
    {"img": os.path.join(brain_dir, "scene5_consistent_impact_1779929897332.png"), "duration": 10, "text": "이 각도 그대로 임팩트!"}
]

# 나레이션 텍스트 
narration_text = """
코킹과 힌지, 아직도 헷갈리시나요? 50대 독학 골퍼 여러분, 오늘 가슴 높이에서 확실하게 잡아드립니다!
테이크백 이후 양손이 가슴 높이에 올 때, 왼손목은 위로 꺾이는 코킹을 만들어야 합니다. 망치질 하듯 위로 살짝 꺾어주세요.
동시에 오른손목은 뒤로 젖혀지는 힌지를 만듭니다. 무거운 쟁반을 한 손으로 안정적으로 받치고 있다고 상상해 보세요.
이 두 동작이 결합되어 손이 명치나 우측 가슴 높이에 왔을 때 견고한 하프 스윙 탑이 완성됩니다. 클럽 헤드는 하늘을 향해야 정상입니다.
이 견고한 손목 각도를 유지하며 임팩트까지 내려오면 비거리와 방향성이 획기적으로 좋아집니다. 지금 당장 거울 앞에서 연습해 보세요!
"""

audio_path = os.path.join(base_dir, "narration.mp3")

async def generate_audio():
    if not os.path.exists(audio_path):
        print("Generating TTS audio...")
        communicate = edge_tts.Communicate(text=narration_text, voice="ko-KR-InJoonNeural", rate="+10%")
        await communicate.save(audio_path)

asyncio.run(generate_audio())

output_path = os.path.join(base_dir, "cocking_hinge_shorts.mp4")
font_path = r"C:\Windows\Fonts\malgunbd.ttf"

def add_subtitle(image_path, text, output_img_path):
    img = Image.open(image_path)
    width, height = img.size
    draw = ImageDraw.Draw(img)
    
    font_size = int(height * 0.045)
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()
        
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
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
    draw_rgb.text((text_x, text_y), text, fill=(255, 235, 59), font=font)
    
    img.save(output_img_path)

processed_clips = []
for i, scene in enumerate(scenes):
    temp_img_path = os.path.join(scratch_dir, f"temp_cocking_hinge_{i}.png")
    add_subtitle(scene["img"], scene["text"], temp_img_path)
    # 기본 duration 10초 설정
    clip = ImageClip(temp_img_path).with_duration(scene["duration"])
    processed_clips.append(clip)

# 동적 오디오 길이 매칭
try:
    audio = AudioFileClip(audio_path)
    audio_duration = audio.duration
    print(f"[정보] 오디오 원본 재생 시간: {audio_duration}초")
    
    # 5개의 씬이므로 오디오 길이를 5로 나누어 균등 분배 (또는 마지막 컷 보정)
    avg_duration = audio_duration / 5
    for i in range(4):
        processed_clips[i] = processed_clips[i].with_duration(avg_duration)
    
    prev_clips_duration = avg_duration * 4
    last_clip_duration = audio_duration - prev_clips_duration
    
    print(f"[보정] 각 클립 평균 지속 시간: {avg_duration:.2f}초, 마지막 클립 지속 시간: {last_clip_duration:.2f}초")
        
    processed_clips[-1] = processed_clips[-1].with_duration(last_clip_duration)
    
    video = concatenate_videoclips(processed_clips, method="compose")
    video = video.with_audio(audio)
except Exception as e:
    print(f"오디오 처리 중 오류 발생: {e}")
    # 오디오 없는 버전으로 폴백
    video = concatenate_videoclips(processed_clips, method="compose")

video.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')
print(f"[완료] 코킹 및 힌지 쇼츠 생성 완료: {output_path}")
