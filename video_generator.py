from moviepy.editor import CompositeVideoClip
from background_animator import BackgroundAnimator
from text_overlay import TextOverlay
from subtitle_parser import SubtitleParser
from video_exporter import VideoExporter
import os


class VideoGenerator:
    def __init__(self, font_path):
        """Initialize the video generator with font path."""
        self.font_path = font_path

    def create_video(self, video_number, input_dir, output_dir):
        """Create video for specific number using corresponding files."""
        # Construct file paths
        background_path = os.path.join(input_dir, f"{video_number}.png")
        subtitle_path = os.path.join(input_dir, f"{video_number}.srt")
        output_path = os.path.join(output_dir, f"output_{video_number}.mp4")

        # Verify files exist
        if not os.path.exists(background_path):
            raise FileNotFoundError(f"Background image not found: {background_path}")
        if not os.path.exists(subtitle_path):
            raise FileNotFoundError(f"Subtitle file not found: {subtitle_path}")

        # Initialize components
        background_animator = BackgroundAnimator(background_path)
        text_overlay = TextOverlay(self.font_path)

        # Parse subtitles and get total duration
        subtitles = SubtitleParser.parse_subtitle_file(subtitle_path)
        total_duration = max(start + duration for start, duration, _ in subtitles)

        # Generate animated background
        background_clip = background_animator.animate_background(total_duration)

        # Create text clips for each subtitle
        text_clips = [
            text_overlay.create_text_clip(text, start, duration)
            for start, duration, text in subtitles
        ]

        # Combine all clips
        final_clip = CompositeVideoClip(
            [background_clip] + text_clips,
            size=background_clip.size
        )

        # Export the final video
        VideoExporter.export_video(final_clip, output_path)

        return output_path