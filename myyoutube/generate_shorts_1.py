# generate_shorts_1.py
# 50대 골퍼를 위한 배치기(얼리 익스텐션) 탈출법 쇼츠 자동 생성 스크립트

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
        "img": os.path.join(brain_dir, "shorts1_scene1_1780958212276.png"),
        "subtitle": "배치기 때문에 생크 나나요?",
        "narration": "아이언만 잡으면 배치기로 생크나 슬라이스가 나서 고민이신가요? 임팩트 때 척추 각도가 서면서 골반이 앞으로 튀어나오는 현상을 얼리 익스텐션, 즉 배치기라고 부릅니다."
    },
    {
        "img": os.path.join(brain_dir, "shorts1_scene2_1780958223070.png"),
        "subtitle": "엉덩이에 가상의 벽을 두세요",
        "narration": "배치기를 고치는 가장 쉽고 효과적인 방법은 바로 엉덩이 벽 훈련입니다. 어드레스 상태에서 엉덩이 뒤에 가상의 벽이 있다고 머릿속으로 강하게 상상해 보세요."
    },
    {
        "img": os.path.join(brain_dir, "shorts1_scene3_1780958234182.png"),
        "subtitle": "다운스윙 시 왼엉덩이 대기",
        "narration": "백스윙 때는 오른쪽 엉덩이가 벽에 닿고, 다운스윙을 내릴 때는 왼쪽 엉덩이가 벽을 강하게 밀어내며 회전해야 합니다. 척추 각도가 굽혀진 채 그대로 고정되어 스윙 궤도가 완벽해집니다."
    },
    {
        "img": os.path.join(brain_dir, "shorts1_scene4_1780958247250.png"),
        "subtitle": "하루 10분 벽 밀기 연습",
        "narration": "연습장 벽에 대고 엉덩이를 교대로 닿게 만드는 연습을 하루 딱 10분만 반복하십시오. 몸이 펴지지 않고 회전하는 올바른 감각이 척추 근육에 자연스럽게 기억될 것입니다."
    },
    {
        "img": os.path.join(brain_dir, "shorts1_scene5_1780958258585.png"),
        "subtitle": "일관된 정타와 멋진 피니시!",
        "narration": "배치기가 사라지면 클럽 패스가 정교해져 기막힌 정타율과 폭발적인 비거리를 보장합니다. 당당하고 안정적인 피니시로 동반자들을 압도해 보시기 바랍니다."
    }
]

output_path = os.path.join(base_dir, "배치기_탈출_쇼츠.mp4")
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
        audio_file = os.path.join(scratch_dir, f"audio_shorts1_scene_{i}.mp3")
        await generate_tts(scene["narration"], audio_file)
        
        temp_img_path = os.path.join(scratch_dir, f"temp_shorts1_scene_{i}.png")
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
