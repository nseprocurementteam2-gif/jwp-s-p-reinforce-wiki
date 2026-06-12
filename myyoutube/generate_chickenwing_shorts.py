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

# 씬 정보 정의
scenes_data = [
    {
        "img": os.path.join(brain_dir, "chicken_wing_scene_1_1780641710259.png"),
        "subtitle": "아픈 팔꿈치, 치킨윙 때문?",
        "narration": "골프만 치면 엘보 통증으로 고생하십니까? 50대 독학 골퍼분들이 스윙 후 왼팔이 벌어지는 치킨윙 동작을 방치하면 심각한 관절 부상으로 이어집니다."
    },
    {
        "img": os.path.join(brain_dir, "chicken_wing_scene_2_1780641725030.png"),
        "subtitle": "억지로 뻗지 마세요!",
        "narration": "임팩트 때 볼을 억지로 띄우려 하거나 팔을 곧게 뻗으려고 의식할수록 몸은 굳고 왼팔꿈치가 뒤로 빠지게 되는 법입니다."
    },
    {
        "img": os.path.join(brain_dir, "chicken_wing_scene_3_1780641739416.png"),
        "subtitle": "자연스러운 롤오버",
        "narration": "AI가 추천하는 올바른 릴리즈는 임팩트 이후 양팔이 교차하듯 부드럽게 돌며 왼팔꿈치가 지면을 향하게 툭 떨어뜨리는 롤오버입니다."
    },
    {
        "img": os.path.join(brain_dir, "chicken_wing_scene_4_1780641754106.png"),
        "subtitle": "타겟과 악수하듯!",
        "narration": "쉽게 교정하려면 스윙 후 오른손을 목표 방향으로 뻗어 악수하듯 손바닥을 뒤집어 보세요. 왼팔꿈치가 저절로 아래로 접힙니다."
    },
    {
        "img": os.path.join(brain_dir, "chicken_wing_scene_5_1780641770456.png"),
        "subtitle": "부상 없이 싱글까지!",
        "narration": "릴리즈 때 힘 빼고 돌려만 줘도 엘보 아플 일 전혀 없습니다. 부상 없이 건강하게 동반자들을 압도해 봅시다."
    }
]

output_path = os.path.join(base_dir, "치키윙.mp4")
font_path = r"C:\Windows\Fonts\malgunbd.ttf"  # Windows 맑은 고딕 볼드 폰트
voice = "ko-KR-InJoonNeural"  # 50대 남성 목소리 톤에 적합한 edge-tts 한국어 남성 성우

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
    
    # 이미지 높이 대비 4.5% 비율의 폰트 사이즈 설정 (가독성 향상)
    font_size = int(height * 0.045)
    
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()
        print("경고: 지정된 한글 폰트를 로드할 수 없어 기본 폰트를 적용합니다.")
    
    # 텍스트 줄바꿈 처리 (15자 기준)
    text = "\n".join(textwrap.wrap(text, width=15))
    
    # 텍스트 크기 측정
    try:
        text_bbox = draw.multiline_textbbox((0, 0), text, font=font, align='center')
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
    except AttributeError:
        text_width, text_height = draw.textsize(text, font=font)
        
    # 자막 바 크기
    bar_width = int(width * 0.85)
    bar_height = int(text_height * 1.8)
    bar_x1 = int((width - bar_width) / 2)
    bar_y1 = int(height * 0.82)
    bar_x2 = bar_x1 + bar_width
    bar_y2 = bar_y1 + bar_height
    
    # 검은색 반투명 바 오버레이
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rounded_rectangle([bar_x1, bar_y1, bar_x2, bar_y2], radius=20, fill=(0, 0, 0, 180))
    
    img = img.convert('RGBA')
    img = Image.alpha_composite(img, overlay).convert('RGB')
    
    # 노란색 자막 추가
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
        # 1. TTS 파일명 설정 및 비동기 생성
        audio_file = os.path.join(scratch_dir, f"audio_scene_{i}.mp3")
        await generate_tts(scene["narration"], audio_file)
        
        # 2. 자막 입힌 임시 이미지 저장
        temp_img_path = os.path.join(scratch_dir, f"temp_scene_{i}.png")
        add_subtitle(scene["img"], scene["subtitle"], temp_img_path)
        
        # 3. 오디오 재생 시간(duration) 확인 및 클립 결합
        audio_clip = AudioFileClip(audio_file)
        duration = audio_clip.duration
        print(f"씬 {i+1} 재생 시간: {duration:.2f}초")
        
        # 이미지 클립 생성 후 오디오 및 재생 시간 연동
        clip = ImageClip(temp_img_path).with_duration(duration).with_audio(audio_clip)
        processed_clips.append(clip)
        
    print("\n--- 2단계: 비디오 클립 병합 및 인코딩 ---")
    # 비디오 전체 병합
    video = concatenate_videoclips(processed_clips, method="compose")
    
    # 최종 영상 인코딩 저장
    print(f"최종 비디오 쓰기: {output_path}")
    video.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')
    print(f"\n✅ 성공: 최종 비디오 저장 완료 -> {output_path}")

if __name__ == "__main__":
    asyncio.run(main())
