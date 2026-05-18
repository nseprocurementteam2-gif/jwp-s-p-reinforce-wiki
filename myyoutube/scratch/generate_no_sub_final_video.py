
import os
from moviepy import ImageClip, concatenate_videoclips, CompositeVideoClip, AudioFileClip

# 경로 설정
BRAIN_DIR = r"C:\Users\NSE\.gemini\antigravity\brain\23faa1fb-ecd0-42b2-b2c8-4b1492e1044d"
OUTPUT_DIR = r"c:\Users\NSE\.connect-ai-brain\myyoutube"
AUDIO_PATH = r"c:\Users\NSE\.connect-ai-brain\myyoutube\Generated Audio May 15, 2026 - 4_24PM.wav"

images = [
    os.path.join(BRAIN_DIR, "scene_1_opening_1778830200506.png"),
    os.path.join(BRAIN_DIR, "scene_2_concept_1778830215731.png"),
    os.path.join(BRAIN_DIR, "scene_3_practice_1778830231352.png"),
    os.path.join(BRAIN_DIR, "scene_4_effect_1778830248163.png"),
    os.path.join(BRAIN_DIR, "scene_5_closing_1778830265526.png")
]

durations = [15, 25, 15, 17, 18] # 총 90초

def generate_no_sub_video():
    clips = []
    
    for i in range(len(images)):
        # 배경 이미지 클립 (1920x1080)
        img_clip = ImageClip(images[i]).with_duration(durations[i]).resized(width=1920, height=1080)
        clips.append(img_clip)

    # 전체 영상 합치기
    final_video = concatenate_videoclips(clips, method="compose")
    
    # 오디오 로드 및 합성
    if os.path.exists(AUDIO_PATH):
        audio = AudioFileClip(AUDIO_PATH)
        final_video = final_video.with_audio(audio)
    
    # 저장
    output_path = os.path.join(OUTPUT_DIR, "ai_assistant_automation_90s_no_sub.mp4")
    final_video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
    print(f"No-subtitle video with audio generated at: {output_path}")

if __name__ == "__main__":
    generate_no_sub_video()
