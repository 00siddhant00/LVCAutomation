import logging
from moviepy.editor import CompositeVideoClip
from background_animator import BackgroundAnimator
from text_overlay import TextOverlay
from subtitle_parser import SubtitleParser
from video_exporter import VideoExporter
from audio_handler import AudioHandler
import os


class VideoGenerator:
    def __init__(self, font_path, logger=None):
        """Initialize the video generator with font path and an optional logger."""
        self.font_path = font_path
        self.logger = logger or logging.getLogger(__name__)  # Default to root logger if no logger is provided

    def create_video(self, video_number, input_dir, output_dir, config):
        """Create video synchronized with audio duration and update done.txt file."""
        try:
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

            # Log the start of video generation
            self.logger.info(f"Generating video {video_number}...")

            # Load audio and get duration
            audio_clip, audio_duration = AudioHandler.load_audio(audio_path)

            # Initialize components
            background_animator = BackgroundAnimator(background_path, res_x=config.res_x, res_y=config.res_y)
            text_overlay = TextOverlay(
                self.font_path,
                font_size=160,  # Initial size; dynamic adjustment will follow
                shadow_spread=5,  # Higher spread for high-res text
                shadow_opacity=0.9,
                shadow_color=(255, 255, 255),
                shadow_offset=(0, 0),  # Adjusted for high resolution
                resolution_scale=1  # High resolution scale for crisp text
            )

            # Generate animated background matching audio duration
            background_clip = background_animator.animate_background(audio_duration)

            # Parse subtitles
            subtitles = SubtitleParser.parse_subtitle_file(subtitle_path)

            # Create text clips for each subtitle
            text_clips = [
                text_overlay.create_text_clip(
                    text=text,
                    start=start,
                    duration=duration,
                    fps=config.fps
                )
                for start, duration, text in subtitles
            ]

            # Combine all clips with audio
            final_clip = CompositeVideoClip(
                [background_clip] + text_clips,
                # size=background_clip.size
                size=(config.res_x, config.res_y)
            ).set_audio(audio_clip)

            # Export the final video
            VideoExporter.export_video(final_clip, output_path, config)

            # Clean up
            audio_clip.close()

            # Log successful completion
            self.logger.info(f"Successfully generated video {video_number}: {output_path}")

            # Update done.txt after successful video generation
            # self._update_done_file(done_file_path, video_number, status="done")

            return output_path

        except Exception as e:
            # Log any error that occurs during the video generation process
            self.logger.error(f"Error generating video {video_number}: {str(e)}")

            # Update done.txt with failure status
            # self._update_done_file(done_file_path, video_number, status="failed")

            raise

    def _update_done_file(self, done_file_path, video_number, status):
        """Update the done.txt file with video status."""
        try:
            # Check if done.txt exists, otherwise create it
            if not os.path.exists(done_file_path):
                with open(done_file_path, 'w') as f:
                    f.write("Video generation status:\n")

            # Append the current video's status to the done.txt file
            with open(done_file_path, 'a') as f:
                f.write(f"Video {video_number} - {status}\n")

            self.logger.info(f"Updated done.txt with status for video {video_number}: {status}")

        except Exception as e:
            self.logger.error(f"Error updating done.txt: {str(e)}")
