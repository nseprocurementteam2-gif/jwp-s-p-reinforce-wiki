from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips, ImageClip
import os

def replace_audio(video_path, audio_path, output_path):
    video = VideoFileClip(video_path)
    new_audio = AudioFileClip(audio_path)
    
    video_duration = video.duration
    audio_duration = new_audio.duration
    
    print(f"Video duration: {video_duration}")
    print(f"Audio duration: {audio_duration}")
    
    if audio_duration > video_duration:
        # Extend video by freezing the last frame
        print("Audio is longer than video. Freezing last frame.")
        last_frame = video.get_frame(video_duration - 0.1)
        # Create an ImageClip from the last frame
        # MoviePy 2.x uses ImageClip(frame) directly
        freeze_duration = audio_duration - video_duration
        # To get a frame as an image, we can save it temporarily or use ImageClip
        # In MoviePy 2.x, VideoFileClip.get_frame returns a numpy array.
        # We can use ImageClip(numpy_array)
        freeze_clip = ImageClip(last_frame).with_duration(freeze_duration)
        
        final_video = concatenate_videoclips([video, freeze_clip], method="compose")
    else:
        # If audio is shorter, we just trim the video
        print("Audio is shorter or equal to video. Trimming video.")
        final_video = video.with_duration(audio_duration)
    
    # Apply the new audio
    final_video = final_video.with_audio(new_audio)
    
    # Save the result
    final_video.write_videofile(output_path, fps=video.fps, codec="libx264", audio_codec="aac")
    print(f"Updated video saved as {output_path}")

if __name__ == "__main__":
    replace_audio(
        "learning_plan_errors_video.mp4",
        "Generated Audio May 14, 2026 - 4_56PM.wav",
        "learning_plan_errors_video_updated.mp4"
    )
