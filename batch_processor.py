import os
import time
from video_generator import VideoGenerator


class BatchProcessor:
    def __init__(self, input_dir, output_dir, font_path):
        """Initialize batch processor with directories and font path."""
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.font_path = font_path
        self.generator = VideoGenerator(font_path)

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

    def get_pending_videos(self):
        """Get list of video numbers that need to be processed."""
        # Get all .srt files and extract their numbers
        srt_files = [f for f in os.listdir(self.input_dir) if f.endswith('.srt')]
        video_numbers = [int(f.split('.')[0]) for f in srt_files]

        # Check which ones have all required files
        pending = []
        for num in video_numbers:
            png_path = os.path.join(self.input_dir, f"{num}.png")
            output_path = os.path.join(self.output_dir, f"output_{num}.mp4")

            # Check for either mp3 or wav audio file
            has_audio = any(
                os.path.exists(os.path.join(self.input_dir, f"{num}{ext}"))
                for ext in ['.mp3', '.wav']
            )

            if (os.path.exists(png_path) and
                    has_audio and
                    not os.path.exists(output_path)):
                pending.append(num)

        return sorted(pending)

    def process_batch(self):
        """Process all pending videos in sequence."""
        while True:
            pending_videos = self.get_pending_videos()

            if not pending_videos:
                print("No pending videos found. Waiting for new files...")
                time.sleep(30)  # Wait 30 seconds before checking again
                continue

            for video_num in pending_videos:
                try:
                    print(f"Processing video {video_num}...")
                    output_path = self.generator.create_video(
                        video_num,
                        self.input_dir,
                        self.output_dir
                    )
                    print(f"Successfully generated: {output_path}")
                except Exception as e:
                    print(f"Error processing video {video_num}: {str(e)}")
                    continue