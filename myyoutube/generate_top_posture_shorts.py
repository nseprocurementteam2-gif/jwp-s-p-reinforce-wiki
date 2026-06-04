import os
import sys
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips

# 1. 경로 및 씬 설정
base_dir = r"c:\Users\NSE\.connect-ai-brain\myyoutube"
brain_dir = r"C:\Users\NSE\.gemini\antigravity-ide\brain\cd4ccaac-1343-4b3c-81a7-1e4ecea9d306"
scratch_dir = os.path.join(base_dir, "scratch")
os.makedirs(scratch_dir, exist_ok=True)

# 씬 정보 정의 (이미지 경로, 재생 시간, 자막 문구)
scenes = [
    {
        "img": os.path.join(brain_dir, "qa_final_scene1_1780366934468.png"),
        "duration": 11,
        "text": "아직도 탑에서 흔들리시나요? AI가 딱 정해드립니다!"
    },
    {
        "img": os.path.join(brain_dir, "qa_final_scene2_1780366947051.png"),
        "duration": 11,
        "text": "유연성 부족? 온몸이 흔들흔들 힘 빼고 이것만 보세요!"
    },
    {
        "img": os.path.join(brain_dir, "qa_fixed_scene3_1780366630350.png"),
        "duration": 13,
        "text": "왼발 안쪽에 체중 꽉 잡기! 양손은 귀 옆 손목 곧게 펴기"
    },
    {
        "img": os.path.join(brain_dir, "top_posture_scene4_1780365915015.png"),
        "duration": 10,
        "text": "헤드 방향은 내 척추 각도와 똑같이 맞추기!"
    },
    {
        "img": os.path.join(brain_dir, "qa_fixed_scene5_1780366657888.png"),
        "duration": 11,
        "text": "가볍게 툭 쳐도 무조건 굿샷! 여러분의 의견 댓글 남겨주세요"
    }
]

audio_path = os.path.join(base_dir, "6월2일 탑자세.wav")
output_path = os.path.join(base_dir, "6월2일_탑자세_쇼츠.mp4")
font_path = r"C:\Windows\Fonts\malgunbd.ttf"  # Windows 맑은 고딕 볼드 폰트

# 2. 이미지 위에 한글 자막 렌더링 함수
def add_subtitle(image_path, text, output_img_path):
    if not os.path.exists(image_path):
        print(f"오류: 이미지 파일 누락 - {image_path}")
        sys.exit(1)
        
    img = Image.open(image_path)
    width, height = img.size
    draw = ImageDraw.Draw(img)
    
    # 이미지 높이 대비 3.5% 비율의 폰트 사이즈 설정 (세로형 9:16 비디오 대응, 기존 4.5%에서 축소)
    font_size = int(height * 0.035)
    
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()
        print("경고: 지정된 한글 폰트를 로드할 수 없어 기본 폰트를 적용합니다.")
    
    # 텍스트가 길 경우 줄바꿈 처리 로직 추가 (15자 기준)
    import textwrap
    text = "\n".join(textwrap.wrap(text, width=15))
    
    # 텍스트 바운딩 박스 측정
    try:
        text_bbox = draw.multiline_textbbox((0, 0), text, font=font, align='center')
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
    except AttributeError:
        text_width, text_height = draw.textsize(text, font=font)
        
    # 하단 자막 영역 바 좌표 정의 (중앙 정렬)
    bar_width = int(width * 0.90)
    bar_height = int(text_height * 1.8)
    bar_x1 = int((width - bar_width) / 2)
    bar_y1 = int(height * 0.82)
    bar_x2 = bar_x1 + bar_width
    bar_y2 = bar_y1 + bar_height
    
    # 반투명 검은 배경 바 생성 및 합성 (투명도 180/255)
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rounded_rectangle([bar_x1, bar_y1, bar_x2, bar_y2], radius=20, fill=(0, 0, 0, 180))
    
    img = img.convert('RGBA')
    img = Image.alpha_composite(img, overlay)
    img = img.convert('RGB')
    
    # 노란색 텍스트 오버레이
    draw_rgb = ImageDraw.Draw(img)
    text_x = bar_x1 + (bar_width - text_width) // 2
    text_y = bar_y1 + (bar_height - text_height) // 2 - int(text_height * 0.1)
    draw_rgb.multiline_text((text_x, text_y), text, fill=(255, 235, 59), font=font, align='center')
    
    img.save(output_img_path)
    print(f"자막 이미지 준비 완료: {output_img_path}")

# 3. 자막 합성 및 비디오 클립화 진행
print("1단계: 자막 생성 시작...")
processed_clips = []
for i, scene in enumerate(scenes):
    temp_img_path = os.path.join(scratch_dir, f"temp_top_posture_{i}.png")
    add_subtitle(scene["img"], scene["text"], temp_img_path)
    
    # 임시로 duration을 지정하여 클립 생성
    clip = ImageClip(temp_img_path).with_duration(scene["duration"])
    processed_clips.append(clip)

# 4. 비디오 클립 연결 및 오디오 합성
print("2단계: 동영상 병합 및 오디오 추가...")
if not os.path.exists(audio_path):
    print(f"오류: 오디오 파일 누락 - {audio_path}")
    sys.exit(1)

# 실제 오디오 클립 로드
audio = AudioFileClip(audio_path)
audio_duration = audio.duration
print(f"오디오 길이: {audio_duration}초")

# 56초로 만들기 위해 마지막 클립 조절
base_duration = audio_duration / len(scenes)
for i in range(len(scenes) - 1):
    scenes[i]["duration"] = base_duration
    processed_clips[i] = processed_clips[i].with_duration(base_duration)
    
prev_clips_duration = sum(scene["duration"] for scene in scenes[:-1])
last_clip_duration = audio_duration - prev_clips_duration

print(f"마지막 클립 재생 시간 동적 조정: {last_clip_duration:.2f}초")
processed_clips[-1] = processed_clips[-1].with_duration(last_clip_duration)

# 비디오 클립들을 최종 병합
video = concatenate_videoclips(processed_clips, method="compose")

# 오디오를 최종 비디오에 합성
video = video.with_audio(audio)

# 5. 최종 인코딩 및 출력
print("3단계: 최종 비디오 파일 작성...")
video.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')
print(f"성공: 최종 쇼츠 비디오 저장 완료 -> {output_path}")
