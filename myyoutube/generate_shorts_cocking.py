import os
import sys
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips

base_dir = r"c:\Users\NSE\.connect-ai-brain\myyoutube"
brain_dir = r"C:\Users\NSE\.gemini\antigravity-ide\brain\ac872f71-3e8f-4ed5-946f-5faa3da311d7"
scratch_dir = os.path.join(base_dir, "scratch")
os.makedirs(scratch_dir, exist_ok=True)

# 씬별 데이터베이스
scenes = [
    {"img": os.path.join(brain_dir, "scene1_address_1779844730741.png"), "duration": 8, "text": "독학 골프의 시작!"},
    {"img": os.path.join(brain_dir, "scene2_takeback_1779844771399.png"), "duration": 10, "text": "오른발까지 일직선!"},
    {"img": os.path.join(brain_dir, "scene3_cocking_1779844789007.png"), "duration": 9, "text": "가슴 라인 코킹&힌지"},
    {"img": os.path.join(brain_dir, "scene4_halfswing_1779844805701.png"), "duration": 9, "text": "견고한 하프 스윙!"},
    {"img": os.path.join(brain_dir, "scene5_impact_1779844821833.png"), "duration": 9, "text": "굿샷! 참 쉽죠?"}
]

# 한글 파일명 처리 주의
audio_path = os.path.join(base_dir, "코킹.wav")
if not os.path.exists(audio_path):
    print(f"[{audio_path}] 오디오 파일을 찾을 수 없습니다. 인코딩 문제일 수 있으므로 폴더 내 wav 파일을 확인합니다.")
    wav_files = [f for f in os.listdir(base_dir) if f.endswith(".wav")]
    for w in wav_files:
        if "코킹" in w or w.startswith(""): # cp949 깨짐 방지
            audio_path = os.path.join(base_dir, w)
            break

output_path = os.path.join(base_dir, "cocking_shorts.mp4")
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
    temp_img_path = os.path.join(scratch_dir, f"temp_cocking_{i}.png")
    add_subtitle(scene["img"], scene["text"], temp_img_path)
    clip = ImageClip(temp_img_path).with_duration(scene["duration"])
    processed_clips.append(clip)

# 동적 오디오 길이 매칭
try:
    audio = AudioFileClip(audio_path)
    audio_duration = audio.duration
    print(f"[정보] 오디오 원본 재생 시간: {audio_duration}초")
    
    prev_clips_duration = sum(scene["duration"] for scene in scenes[:-1])
    last_clip_duration = audio_duration - prev_clips_duration
    
    if last_clip_duration <= 0:
        print(f"[오류] 오디오 길이가 짧습니다. 최소 {prev_clips_duration}초 이상 필요합니다.")
        last_clip_duration = scenes[-1]["duration"]
    else:
        print(f"[보정] 마지막 클립 지속 시간 변경: {scenes[-1]['duration']}초 -> {last_clip_duration:.2f}초")
        
    processed_clips[-1] = processed_clips[-1].with_duration(last_clip_duration)
    
    video = concatenate_videoclips(processed_clips, method="compose")
    video = video.with_audio(audio)
except Exception as e:
    print(f"오디오 처리 중 오류 발생: {e}")
    # 오디오 없는 버전으로 폴백
    video = concatenate_videoclips(processed_clips, method="compose")

video.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')
print(f"[완료] 쇼츠 생성 완료: {output_path}")
