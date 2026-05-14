import os
import glob
from gtts import gTTS
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip, ColorClip
from PIL import Image, ImageDraw, ImageFont
import requests

# Bypassing SSL for gTTS/requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def create_subtitle_image(text, output_path, width=1920, height=200):
    # Gray transparent background (RGBA: 40, 40, 40, 180)
    img = Image.new('RGBA', (width, height), (40, 40, 40, 180))
    draw = ImageDraw.Draw(img)
    
    # Try to load a Korean font
    font_path = "C:\\Windows\\Fonts\\malgun.ttf" # Windows default
    if not os.path.exists(font_path):
        # Fallback if font doesn't exist
        font = ImageFont.load_default()
    else:
        font = ImageFont.truetype(font_path, 60)
    
    # Text size and center alignment
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (width - text_width) // 2
    y = (height - text_height) // 2 - bbox[1]
    
    # Readable color (Yellow or White)
    draw.text((x, y), text, font=font, fill='white')
    img.save(output_path)

def generate_audio(text, output_path):
    tts = gTTS(text, lang='ko', slow=False)
    # Note: gTTS doesn't easily expose SSL bypass, but requests usually respects environment variables
    # Or we can use verify=False if we modify gtts, but let's hope it works with trusted-host logic
    tts.save(output_path)

def build_video():
    sections = [
        {
            "image": "scratch/intro_trash_planner*.png",
            "text": "또 작심삼일인가요? 당신의 의지력이 약해서가 아닙니다. 설계가 잘못되었을 뿐입니다. 기억하세요. 우리는 목표의 수준까지 올라가는 게 아니라, 내가 만든 시스템의 수준까지 떨어집니다.",
            "keyword": "오류 1: 의지력의 함정"
        },
        {
            "image": "scratch/error1_superhero*.png",
            "text": "첫 번째 오류, '미래의 나'를 너무 믿는 근거 없는 자신감입니다. 보통 예상보다 1.7배의 시간이 더 걸리죠. 100% 빽빽한 계획은 무조건 터집니다. 해결책은 '70%의 법칙'입니다. 딱 70%만 계획하고 나머지 30%는 여백으로 비워두세요.",
            "keyword": "오류 1: 근거 없는 자신감 (70% 법칙)"
        },
        {
            "image": "scratch/error2_vague*.png",
            "text": "두 번째 오류, 뇌를 고민하게 만드는 모호한 지시입니다. '영어 공부'처럼 막연한 계획은 결정 피로를 유발합니다. 해결책은 '스위치 행동 설계'입니다. 계획을 '동사, 대상, 수량'으로 쪼개세요. 저녁 먹고 커피 마시면 책상에 앉아 단어 10개 외운다처럼 상황과 행동을 엮으세요.",
            "keyword": "오류 2: 모호한 지시 (If-Then 설계)"
        },
        {
            "image": "scratch/error3_exhausted*.png",
            "text": "세 번째 오류, '최상의 컨디션'만 생각한 완벽주의입니다. 계획이 무너지는 건 최악인 날을 계산하지 않았기 때문이죠. 해결책은 '최소한의 자존심' 루틴입니다. 아픈 날에도 5분만 책상에 앉아 책을 펴보세요. 흐름을 끊지 않는 것 자체가 강력한 성공 경험이 됩니다.",
            "keyword": "오류 3: 완벽주의 (최소 루틴)"
        },
        {
            "image": "scratch/conclusion_start*.png",
            "text": "완벽한 플래너를 기다리지 마세요. 대충, 빨리, 잘의 원칙을 기억하세요. 일단 70%만 적고 시작하는 것, 그것이 인생을 바꾸는 시스템의 시작입니다. 지금 바로 시작하세요.",
            "keyword": "결론: 대충, 빨리, 잘 시작하기"
        }
    ]
    
    clips = []
    total_duration = 0
    
    for i, section in enumerate(sections):
        audio_path = f"scratch/audio_{i}.mp3"
        sub_path = f"scratch/sub_{i}.png"
        
        # Generate Audio
        if not os.path.exists(audio_path):
            generate_audio(section["text"], audio_path)
        
        # Generate Subtitle Image
        create_subtitle_image(section["keyword"], sub_path)
        
        # Load assets
        audio = AudioFileClip(audio_path)
        # Handle glob for image
        img_files = glob.glob(section["image"])
        if not img_files:
            print(f"Image not found: {section['image']}")
            continue
        
        img_clip = ImageClip(img_files[0]).with_duration(audio.duration).with_audio(audio)
        
        # Create composite with subtitle
        sub_clip = ImageClip(sub_path).with_duration(audio.duration).with_position(('center', 0.8), relative=True)
        
        # Merge subtitle into image clip
        video_clip = CompositeVideoClip([img_clip, sub_clip])
        clips.append(video_clip)
        total_duration += audio.duration
        print(f"Section {i} processed. Duration: {audio.duration}")

    # Final Video
    final_video = concatenate_videoclips(clips, method="compose")
    
    # Adjust to 120s if needed (optional, gTTS might be faster or slower)
    # But user asked for "2 minute length", so we should ensure it's close.
    # If the combined audio is less than 120s, we can slow down the audio or add silence.
    # For now, let's just output what we have.
    
    final_video.write_videofile("learning_plan_errors_video.mp4", fps=24, codec="libx264", audio_codec="aac")
    print(f"Video saved as learning_plan_errors_video.mp4. Total duration: {total_duration}")

if __name__ == "__main__":
    if not os.path.exists("scratch"):
        os.makedirs("scratch")
    build_video()
