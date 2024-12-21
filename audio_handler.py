from moviepy.editor import AudioFileClip

class AudioHandler:
    @staticmethod
    def load_audio(audio_path):
        """Load audio file and return AudioFileClip with duration."""
        try:
            audio = AudioFileClip(audio_path)
            return audio, audio.duration
        except Exception as e:
            print(f"Error loading audio file: {str(e)}")
            raise