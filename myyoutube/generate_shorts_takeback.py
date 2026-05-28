import os
import sys
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips

# 1. 경로 및 씬 설정
base_dir = r"c:\Users\NSE\.connect-ai-brain\myyoutube"
brain_dir = r"C:\Users\NSE\.gemini\antigravity-ide\brain\11a8a44f-9951-4577-8fa2-a501c5bdb259"
scratch_dir = os.path.join(base_dir, "scratch")
os.makedirs(scratch_dir, exist_ok=True)

# 씬 정보 정의 (이미지 경로, 재생 시간, 자막 문구)
scenes = [
    {
        "img": os.path.join(brain_dir, "takeback_scene_1_1779771200727.png"),
        "duration": 14,
        "text": "손으로 들면?"
    },
    {
        "img": os.path.join(brain_dir, "takeback_scene_2_1779771220440.png"),
        "duration": 11,
        "text": "손 대신 왼어깨"
    },
    {
        "img": os.path.join(brain_dir, "takeback_scene_3_1779771243003.png"),
        "duration": 11,
        "text": "오른발 라인까지"
    },
    {
        "img": os.path.join(brain_dir, "takeback_scene_4_1779771261372.png"),
        "duration": 11,
        "text": "덮쳐침 vs 정타"
    },
    {
        "img": os.path.join(brain_dir, "takeback_scene_5_1779771277649.png"),
        "duration": 12,
        "text": "왼어깨만 기억!"
    }
]

audio_path = os.path.join(base_dir, "테이크백.wav")
output_path = os.path.join(base_dir, "테이크백_쇼츠.mp4")
font_path = r"C:\Windows\Fonts\malgunbd.ttf"  # Windows 맑은 고딕 볼드 폰트

# 2. 이미지 위에 한글 자막 렌더링 함수
def add_subtitle(image_path, text, output_img_path):
    if not os.path.exists(image_path):
        print(f"오류: 이미지 파일 누락 - {image_path}")
        sys.exit(1)
        
    img = Image.open(image_path)
    width, height = img.size
    draw = ImageDraw.Draw(img)
    
    # 이미지 높이 대비 4.5% 비율의 폰트 사이즈 설정 (세로형 9:16 비디오 대응)
    font_size = int(height * 0.045)
    
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()
        print("경고: 지정된 한글 폰트를 로드할 수 없어 기본 폰트를 적용합니다.")
    
    # 텍스트 바운딩 박스 측정
    try:
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
    except AttributeError:
        text_width, text_height = draw.textsize(text, font=font)
        
    # 하단 자막 영역 바 좌표 정의 (중앙 정렬)
    bar_width = int(width * 0.85)
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
    draw_rgb.text((text_x, text_y), text, fill=(255, 235, 59), font=font)
    
    img.save(output_img_path)
    print(f"자막 이미지 준비 완료: {output_img_path}")

# 3. 자막 합성 및 비디오 클립화 진행
print("1단계: 자막 생성 시작...")
processed_clips = []
for i, scene in enumerate(scenes):
    temp_img_path = os.path.join(scratch_dir, f"temp_takeback_{i}.png")
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

# 마지막 클립을 제외한 이전 클립들의 총 길이 계산
prev_clips_duration = sum(scene["duration"] for scene in scenes[:-1])

# 마지막 클립의 duration을 오디오 전체 길이에 맞춰 동적으로 조절
last_clip_duration = audio_duration - prev_clips_duration
if last_clip_duration <= 0:
    print(f"오류: 오디오 길이가 너무 짧습니다. 최소 {prev_clips_duration}초 이상이어야 합니다.")
    sys.exit(1)

print(f"마지막 클립 재생 시간 동적 조정: {scenes[-1]['duration']}초 -> {last_clip_duration:.2f}초")
processed_clips[-1] = processed_clips[-1].with_duration(last_clip_duration)

# 비디오 클립들을 최종 병합
video = concatenate_videoclips(processed_clips, method="compose")

# 오디오를 최종 비디오에 합성 (moviepy v2.x 호환 API 'with_audio' 적용)
video = video.with_audio(audio)

# 5. 최종 인코딩 및 출력
print("3단계: 최종 비디오 파일 작성...")
video.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')
print(f"성공: 최종 쇼츠 비디오 저장 완료 -> {output_path}")
