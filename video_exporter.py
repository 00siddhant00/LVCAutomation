class VideoExporter:
    @staticmethod
    def export_video(video_clip, output_path, fps=30):
        """Export the final video clip to MP4 format."""
        video_clip.write_videofile(
            output_path,
            fps=fps,
            codec='libx264',
            audio_codec='aac'
        )