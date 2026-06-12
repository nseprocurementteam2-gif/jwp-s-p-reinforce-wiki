# generate_shorts_week2_2.py
# 50대 골퍼를 위한 드라이버 슬라이스 해결 쇼츠 자동 생성 스크립트

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
        "img": os.path.join(brain_dir, "shorts_w2_s2_p1_1781217703182.png"),
        "subtitle": "칠 때마다 휘어지는 슬라이스?",
        "narration": "드라이버만 잡으면 오른쪽으로 사정없이 휘어지는 슬라이스 때문에 속상하셨죠? 이는 아웃에서 인으로 깎여 맞으며 공에 강한 사이드스핀이 걸려 그렇습니다."
    },
    {
        "img": os.path.join(brain_dir, "shorts_w2_s2_p2_1781217716224.png"),
        "subtitle": "오른팔꿈치를 갈비뼈에 붙이세요",
        "narration": "궤적을 고치는 가장 쉬운 비결은 백스윙 탑에서 다운스윙 시작할 때 오른팔 팔꿈치를 오른쪽 옆구리 즉 갈비뼈에 가볍게 밀착시켜 내려오는 것입니다."
    },
    {
        "img": os.path.join(brain_dir, "shorts_w2_s2_p3_1781217727715.png"),
        "subtitle": "오른손이 왼손을 덮는 릴리즈",
        "narration": "그 다음 임팩트 직후 오른손이 왼손을 부드럽게 덮어주는 회전인 릴리즈를 해주어야 페이스가 닫히며 볼을 힘차게 밀고 나갈 수 있습니다."
    },
    {
        "img": os.path.join(brain_dir, "shorts_w2_s2_p4_1781217738562.png"),
        "subtitle": "헤드를 닫아 잡는 셋업 연습",
        "narration": "어드레스 시 페이스를 닫아보는 연습과 왼손 그립을 세 손가락이 보이도록 약간 스트롱하게 잡는 것도 슬라이스 예방에 큰 도움이 됩니다."
    },
    {
        "img": os.path.join(brain_dir, "shorts_w2_s2_p5_1781217751734.png"),
        "subtitle": "직진하는 비거리 이백이십 미터!",
        "narration": "이 두 가지만 신경 쓰시면 깎여 맞는 스윙이 던져 치는 인 아웃 스윙으로 바뀌어, 슬라이스 없이 똑바로 쭉 뻗어 나가는 통쾌한 티샷을 칠 수 있습니다."
    }
]

output_path = os.path.join(base_dir, "슬라이스_해결_쇼츠.mp4")
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
        audio_file = os.path.join(scratch_dir, f"audio_shorts_w2_s2_scene_{i}.mp3")
        await generate_tts(scene["narration"], audio_file)
        
        temp_img_path = os.path.join(scratch_dir, f"temp_shorts_w2_s2_scene_{i}.png")
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
    print(f"\n✅ 완료: 쇼츠 비디오 2가 저장되었습니다 -> {output_path}")

if __name__ == "__main__":
    asyncio.run(main())
