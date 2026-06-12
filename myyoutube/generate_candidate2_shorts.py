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

# 후보 2번 씬 정보 정의
scenes_data = [
    {
        "img": os.path.join(brain_dir, "iron150_scene_1_1780642212134.png"),
        "subtitle": "7번 아이언 150m의 비밀",
        "narration": "50대 독학 골퍼 여러분, 7번 아이언으로 150미터 이상 비거리를 내는 완벽한 임팩트 스윙의 핵심은 무엇인지 아십니까?"
    },
    {
        "img": os.path.join(brain_dir, "iron150_scene_2_1780642227260.png"),
        "subtitle": "AI가 찾은 핵심 비결",
        "narration": "에이아이가 비거리 상위 1% 골퍼들의 스윙 궤도를 분석한 결과, 핵심은 백스윙 탑에서의 올바른 체중 이동과 각도였습니다."
    },
    {
        "img": os.path.join(brain_dir, "iron150_scene_3_1780642241319.png"),
        "subtitle": "우측 안쪽 체중 고정",
        "narration": "백스윙 탑에서 체중이 바깥으로 밀리지 않도록 오른발 안쪽에 단단히 고정하고, 양손을 충분히 높이 들어주어야 합니다."
    },
    {
        "img": os.path.join(brain_dir, "iron150_scene_4_1780642257050.png"),
        "subtitle": "눌려 맞는 임팩트!",
        "narration": "다운스윙 시 손목 풀림 없이 끌고 내려와 핸드퍼스트로 볼을 찍어 치면, 맑은 타구음과 함께 강력한 탄도가 생깁니다."
    },
    {
        "img": os.path.join(brain_dir, "iron150_scene_5_1780642273284.png"),
        "subtitle": "AI로 스마트하게 독학!",
        "narration": "무작정 세게 치지 말고, 영리하게 스윙 궤도부터 교정해 보십시오. 에이아이가 여러분의 골프 싱글 달성을 응원합니다."
    }
]

output_path = os.path.join(base_dir, "후보2.mp4")
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
        audio_file = os.path.join(scratch_dir, f"audio_candidate2_scene_{i}.mp3")
        await generate_tts(scene["narration"], audio_file)
        
        temp_img_path = os.path.join(scratch_dir, f"temp_candidate2_scene_{i}.png")
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
