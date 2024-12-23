class VideoExporter:
    @staticmethod
    def export_video(video_clip, output_path, config):
        """Export the final video clip to MP4 format using NVENC for video encoding and AAC for audio."""
        try:
            print(f"x : {config.res_x}, y : {config.res_y}, fps: {config.fps}")
            video_clip.write_videofile(
                output_path,
                fps=config.fps,
                codec='libx264',
                audio_codec='aac',
                threads=1,
                preset='fast',
                ffmpeg_params=['-vf', f'scale={config.res_x}:{config.res_y}', '-c:v', 'h264_nvenc', '-c:a', 'aac']  # Scale to 2K
            )
        except Exception as e:
            print(f"Error during video export: {str(e)}")
            raise