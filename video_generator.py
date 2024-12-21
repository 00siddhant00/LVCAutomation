from moviepy.editor import CompositeVideoClip
from background_animator import BackgroundAnimator
from text_overlay import TextOverlay
from subtitle_parser import SubtitleParser
from video_exporter import VideoExporter
from audio_handler import AudioHandler
import os


class VideoGenerator:
    def __init__(self, font_path):
        """Initialize the video generator with font path."""
        self.font_path = font_path

    def create_video(self, video_number, input_dir, output_dir):
        """Create video synchronized with audio duration."""
        # Construct file paths
        background_path = os.path.join(input_dir, f"{video_number}.png")
        subtitle_path = os.path.join(input_dir, f"{video_number}.srt")

        # Look for either mp3 or wav audio file
        audio_path = None
        for ext in ['.mp3', '.wav']:
            temp_path = os.path.join(input_dir, f"{video_number}{ext}")
            if os.path.exists(temp_path):
                audio_path = temp_path
                break

        output_path = os.path.join(output_dir, f"output_{video_number}.mp4")

        # Verify files exist
        if not os.path.exists(background_path):
            raise FileNotFoundError(f"Background image not found: {background_path}")
        if not os.path.exists(subtitle_path):
            raise FileNotFoundError(f"Subtitle file not found: {subtitle_path}")
        if not audio_path:
            raise FileNotFoundError(f"Audio file not found for video {video_number}")

        # Load audio and get duration
        audio_clip, audio_duration = AudioHandler.load_audio(audio_path)

        # Initialize components
        background_animator = BackgroundAnimator(background_path)


        text_overlay = TextOverlay(
            self.font_path,
            font_size=100,  # Initial size; dynamic adjustment will follow
            shadow_spread=8,  # Higher spread for high-res text
            shadow_opacity=0.8,
            shadow_offset=(6, 6),  # Adjusted for high resolution
            resolution_scale=8  # High resolution scale for crisp text
        )

        # Generate animated background matching audio duration
        background_clip = background_animator.animate_background(audio_duration)

        # Parse subtitles
        subtitles = SubtitleParser.parse_subtitle_file(subtitle_path)

        # Create text clips for each subtitle
        text_clips = [
            text_overlay.create_text_clip(text, start, duration)
            for start, duration, text in subtitles
        ]

        # Combine all clips with audio
        final_clip = CompositeVideoClip(
            [background_clip] + text_clips,
            size=background_clip.size
        ).set_audio(audio_clip)

        # Export the final video
        VideoExporter.export_video(final_clip, output_path)

        # Clean up
        audio_clip.close()

        return output_path