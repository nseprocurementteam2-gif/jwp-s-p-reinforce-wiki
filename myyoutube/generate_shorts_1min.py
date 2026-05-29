import os
import sys
import subprocess
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips

base_dir = r"c:\Users\NSE\.connect-ai-brain\myyoutube"
brain_dir = r"C:\Users\NSE\.gemini\antigravity-ide\brain\d93dfadc-6c28-44d9-976e-14c1e871415a"
scratch_dir = os.path.join(base_dir, "scratch")
os.makedirs(scratch_dir, exist_ok=True)

# 1. 스크립트 기반 TTS 오디오 생성 (edge-tts)
script_text = (
    "백스윙 탑에서 왼 손등을 펴주면 다운스윙 시 클럽 페이스가 스퀘어로 들어와 공이 똑바로 갑니다. "
    "만약 손등이 안쪽으로 굽으면 페이스가 하늘을 보며 열리게 되어 심한 슬라이스를 유발합니다. "
    "오른쪽 무릎이 정면을 보는 느낌으로 굽힘을 유지하면 상하체의 꼬임이 극대화되어 비거리가 늘어납니다. "
    "무릎이 펴지면 체중이 무너지고 엎어치는 동작의 원인이 됩니다. "
    "어깨 회전이 부족하다면 오른팔을 살짝 구부려 공간을 확보해 보세요. 훨씬 더 유연하고 큰 회전이 가능해집니다. "
    "마음이 급해 백스윙에서 바로 내려오지 말고, 탑에서 잠시 멈추는 느낌을 가지면 스윙의 일관성이 몰라보게 좋아집니다."
)

audio_path = os.path.join(base_dir, "1min_shorts_audio.wav")
print("1단계: TTS 오디오 생성 시작...")
try:
    subprocess.run(["edge-tts", "--text", script_text, "--write-media", audio_path, "--voice", "ko-KR-InJoonNeural"], check=True)
    print("TTS 오디오 생성 완료.")
except Exception as e:
    print(f"TTS 오디오 생성 실패: {e}")
    sys.exit(1)

# 2. 씬 설정 (자막 및 이미지)
# 동적으로 오디오 길이에 맞추기 위해 초기 duration은 임의로 설정
scenes = [
    {"img": os.path.join(brain_dir, "scene1_left_hand_1780032311542.png"), "duration": 15, "text": "백스윙 탑 왼 손등 펴기!"},
    {"img": os.path.join(brain_dir, "scene2_right_knee_1780032328354.png"), "duration": 15, "text": "오른쪽 무릎 굽힘 유지!"},
    {"img": os.path.join(brain_dir, "scene3_right_arm_1780032344586.png"), "duration": 12, "text": "오른팔 살짝 구부리기!"},
    {"img": os.path.join(brain_dir, "scene4_tempo_pause_1780032361681.png"), "duration": 12, "text": "탑에서 잠시 멈추는 템포!"}
]

output_path = os.path.join(base_dir, "1min_shorts.mp4")
font_path = r"C:\Windows\Fonts\malgunbd.ttf"

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

# 3. 자막 합성 및 비디오 클립화 진행
print("2단계: 자막 합성 및 클립 생성...")
processed_clips = []
for i, scene in enumerate(scenes):
    temp_img_path = os.path.join(scratch_dir, f"temp_1min_{i}.png")
    add_subtitle(scene["img"], scene["text"], temp_img_path)
    clip = ImageClip(temp_img_path).with_duration(scene["duration"])
    processed_clips.append(clip)

# 4. 동적 오디오 길이 매칭 및 병합
print("3단계: 동적 오디오 길이 매칭 및 비디오 병합...")
try:
    audio = AudioFileClip(audio_path)
    audio_duration = audio.duration
    print(f"[정보] 오디오 원본 재생 시간: {audio_duration:.2f}초")
    
    # 4컷에 대해 오디오 길이를 4등분 (마지막 컷에서 오차 보정)
    base_duration = audio_duration / len(scenes)
    for i in range(len(scenes) - 1):
        scenes[i]["duration"] = base_duration
        processed_clips[i] = processed_clips[i].with_duration(base_duration)
        
    prev_clips_duration = sum(scene["duration"] for scene in scenes[:-1])
    last_clip_duration = audio_duration - prev_clips_duration
    
    if last_clip_duration <= 0:
        last_clip_duration = base_duration
    
    print(f"[보정] 마지막 클립 지속 시간: {last_clip_duration:.2f}초")
    processed_clips[-1] = processed_clips[-1].with_duration(last_clip_duration)
    
    video = concatenate_videoclips(processed_clips, method="compose")
    video = video.with_audio(audio)
except Exception as e:
    print(f"오디오 처리 중 오류 발생: {e}")
    video = concatenate_videoclips(processed_clips, method="compose")

# 5. 최종 인코딩 및 출력
print("4단계: 최종 비디오 파일 작성...")
video.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')
print(f"[완료] 쇼츠 생성 완료: {output_path}")
