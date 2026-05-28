import os
import subprocess
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips

base_dir = r"c:\Users\NSE\.connect-ai-brain\myyoutube"
scratch_dir = os.path.join(base_dir, "scratch")
os.makedirs(scratch_dir, exist_ok=True)

# 1. 오디오 생성 (edge-tts)
text = "안녕하세요, 50대 시니어 여러분. 오늘부터 여러분의 든든한 조력자가 될 AI 비서입니다. 나이가 들수록 건강 걱정은 늘고, 재테크는 막막하고, 디지털 세상은 너무 빠르게 변하죠? 걱정 마세요. 이제 제가 여러분 곁에서 가장 필요한 정보만 콕 찝어 알려드릴게요. 매일 아침 전하는 작은 습관 하나가 여러분의 평생 건강과 부를 결정합니다. 저와 함께 더 젊고 똑똑한 노후를 만들어보시겠어요? 지금 바로 구독하고 저를 여러분의 비서로 고용해 보세요! 감사합니다."
audio_path = os.path.join(base_dir, "week1_shorts1_narration.mp3")

if not os.path.exists(audio_path):
    print("TTS 오디오 생성 중...")
    subprocess.run(["edge-tts", "--text", text, "--voice", "ko-KR-InJoonNeural", "--write-media", audio_path], check=True)

# 2. 이미지 및 자막 합성
scenes = [
    {"img": r"C:\Users\NSE\.gemini\antigravity-ide\brain\e0138b46-7b4d-4122-adc9-0955adf52de6\week1_scene1_1779927936395.png", "duration": 5.0, "text": "50대 인생 2막, AI 비서가 함께합니다"},
    {"img": r"C:\Users\NSE\.gemini\antigravity-ide\brain\e0138b46-7b4d-4122-adc9-0955adf52de6\week1_scene2_1779927951536.png", "duration": 18.0, "text": "건강부터 재테크까지 한 번에!"},
    {"img": r"C:\Users\NSE\.gemini\antigravity-ide\brain\e0138b46-7b4d-4122-adc9-0955adf52de6\week1_scene3_1779927969811.png", "duration": 12.0, "text": "당신의 똑똑한 노후를 위해 '구독' 하세요"}
]

font_path = r"C:\Windows\Fonts\malgunbd.ttf"
output_path = os.path.join(base_dir, "week1_shorts1.mp4")

def add_subtitle(image_path, text, output_img_path):
    img = Image.open(image_path)
    width, height = img.size
    draw = ImageDraw.Draw(img)
    
    font_size = int(width * 0.040)
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()
        
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    bar_width = int(width * 0.95)
    bar_height = int(text_height * 2.0)
    bar_x1 = int((width - bar_width) / 2)
    bar_y1 = int(height * 0.85)
    bar_x2 = bar_x1 + bar_width
    bar_y2 = bar_y1 + bar_height
    
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rounded_rectangle([bar_x1, bar_y1, bar_x2, bar_y2], radius=15, fill=(0, 0, 0, 180))
    
    img = img.convert('RGBA')
    img = Image.alpha_composite(img, overlay).convert('RGB')
    
    draw_rgb = ImageDraw.Draw(img)
    text_x = bar_x1 + (bar_width - text_width) // 2
    text_y = bar_y1 + (bar_height - text_height) // 2 - int(text_height * 0.1)
    draw_rgb.text((text_x, text_y), text, fill=(255, 235, 59), font=font)
    
    img.save(output_img_path)

processed_clips = []
for i, scene in enumerate(scenes):
    temp_img_path = os.path.join(scratch_dir, f"temp_w1s1_{i}.png")
    add_subtitle(scene["img"], scene["text"], temp_img_path)
    clip = ImageClip(temp_img_path).with_duration(scene["duration"])
    processed_clips.append(clip)

audio = AudioFileClip(audio_path)
audio_duration = audio.duration
print(f"[정보] 생성된 오디오 길이: {audio_duration}초")

# 비율대로 클립 길이를 오디오 길이에 맞춤
total_target = sum(s["duration"] for s in scenes)
for i in range(len(processed_clips)):
    new_dur = (scenes[i]["duration"] / total_target) * audio_duration
    processed_clips[i] = processed_clips[i].with_duration(new_dur)

video = concatenate_videoclips(processed_clips, method="compose")
video = video.with_audio(audio)

print("비디오 생성 중...")
video.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')
print(f"[완료] 쇼츠 1편 생성 성공: {output_path}")
