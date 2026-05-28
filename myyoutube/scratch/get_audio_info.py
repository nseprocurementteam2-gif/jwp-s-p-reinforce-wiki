import wave

def get_wav_duration(file_path):
    with wave.open(file_path, 'rb') as wav_file:
        frames = wav_file.getnframes()
        rate = wav_file.getframerate()
        duration = frames / float(rate)
        return duration

if __name__ == "__main__":
    audio_path = r"c:\Users\NSE\.connect-ai-brain\myyoutube\꼰대 부장의 이중생활 .wav"
    try:
        dur = get_wav_duration(audio_path)
        print(f"오디오 듀레이션: {dur:.3f} 초")
    except Exception as e:
        print(f"오디오 분석 실패: {e}")
