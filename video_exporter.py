class VideoExporter:
    @staticmethod
    def export_video(video_clip, output_path, fps=30):
        """Export the final video clip to MP4 format using NVENC for video encoding and AAC for audio."""
        try:
            video_clip.write_videofile(
                output_path,
                fps=fps,
                codec='libx264',  # Use libx264 for compatibility; NVENC will handle the actual encoding
                audio_codec='aac',
                threads=4,  # Use 1 thread for CPU tasks; NVENC handles encoding
                preset='fast',  # Choose 'fast' for quicker encoding; adjust as needed
                ffmpeg_params=['-c:v', 'h264_nvenc', '-c:a', 'aac']  # Specify NVENC for video and AAC for audio
            )
        except Exception as e:
            print(f"Error during video export: {str(e)}")
            raise
