from moviepy import ImageClip, AudioFileClip, concatenate_videoclips
import glob
import os

def generate_no_sub_video(audio_path, output_path):
    # Image patterns
    image_patterns = [
        "scratch/intro_trash_planner*.png",
        "scratch/error1_superhero*.png",
        "scratch/error2_vague*.png",
        "scratch/error3_exhausted*.png",
        "scratch/conclusion_start*.png"
    ]
    
    # Load audio to get total duration
    audio = AudioFileClip(audio_path)
    total_audio_duration = audio.duration
    
    # Original target durations (approx 120s total)
    original_durations = [20, 30, 30, 25, 15]
    original_total = sum(original_durations)
    
    # Scale durations to match new audio
    scaled_durations = [(d / original_total) * total_audio_duration for d in original_durations]
    
    clips = []
    for i, pattern in enumerate(image_patterns):
        img_files = glob.glob(pattern)
        if not img_files:
            print(f"Image not found for pattern: {pattern}")
            continue
        
        # Create clip for each image with scaled duration
        clip = ImageClip(img_files[0]).with_duration(scaled_durations[i])
        clips.append(clip)
    
    # Concatenate clips
    final_video = concatenate_videoclips(clips, method="compose")
    
    # Set audio
    final_video = final_video.with_audio(audio)
    
    # Write file
    final_video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
    print(f"No-subtitle video saved as {output_path}")

if __name__ == "__main__":
    generate_no_sub_video(
        "Generated Audio May 14, 2026 - 4_56PM.wav",
        "learning_plan_errors_video_no_sub.mp4"
    )
