class VideoExporter:
    @staticmethod
    def export_video(video_clip, output_path, fps=30, res_x=1920, res_y=1080):
        """Export the final video clip to MP4 format using NVENC for video encoding and AAC for audio."""
        try:
            video_clip.write_videofile(
                output_path,
                fps=fps,
                codec='libx264',
                audio_codec='aac',
                threads=4,
                preset='fast',
                ffmpeg_params=['-vf', f'scale={res_x}:{res_y}', '-c:v', 'h264_nvenc', '-c:a', 'aac']  # Scale to 2K
            )
        except Exception as e:
            print(f"Error during video export: {str(e)}")
            raise
