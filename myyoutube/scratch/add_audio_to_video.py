
import os
from moviepy import VideoFileClip, AudioFileClip

def add_audio_to_video():
    video_path = r"c:\Users\NSE\.connect-ai-brain\myyoutube\ai_assistant_automation_90s.mp4"
    audio_path = r"c:\Users\NSE\.connect-ai-brain\myyoutube\Generated Audio May 15, 2026 - 4_24PM.wav"
    output_path = r"c:\Users\NSE\.connect-ai-brain\myyoutube\ai_assistant_automation_90s_with_audio.mp4"

    if not os.path.exists(video_path):
        print(f"Video not found: {video_path}")
        return
    if not os.path.exists(audio_path):
        print(f"Audio not found: {audio_path}")
        return

    # 영상과 오디오 로드
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)

    # 오디오를 영상 길이에 맞추거나 오디오 길이에 영상을 맞출 수 있음
    # 여기서는 오디오를 영상에 입힘
    final_video = video.with_audio(audio)

    # 저장
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
    
    print(f"Final video with audio generated at: {output_path}")

if __name__ == "__main__":
    add_audio_to_video()
