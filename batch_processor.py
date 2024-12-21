import os
import time
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import List, Optional
from video_generator import VideoGenerator
import logging


class ParallelBatchProcessor:
    def __init__(self, input_dir: str, output_dir: str, font_path: str, max_workers: Optional[int] = None):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.font_path = font_path
        self.max_workers = max_workers or max(1, mp.cpu_count() - 1)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        os.makedirs(output_dir, exist_ok=True)

    @staticmethod
    def process_single_video(args: tuple) -> tuple:
        video_num, input_dir, output_dir, font_path, fps, res_x, res_y = args
        try:
            # Set up logger specific to this video process
            process_logger = logging.getLogger(f"Video_{video_num}")
            process_logger.setLevel(logging.INFO)

            # Create Video Generator instance with logger
            generator = VideoGenerator(font_path, process_logger)

            # Generate video
            output_path = generator.create_video(video_num, input_dir, output_dir,fps, res_x, res_y)

            return video_num, True, output_path
        except Exception as e:
            return video_num, False, str(e)

    def process_videos_in_parallel(self, fps, res_x=1920, res_y=1080):
        # Dynamically get video numbers based on available .srt or .png files in the input directory
        video_files = [f for f in os.listdir(self.input_dir) if f.endswith('.srt')]
        video_numbers = [int(f.split('.')[0]) for f in video_files]

        if not video_numbers:
            self.logger.info("No video files to process.")
            return

        self.logger.info(f"Found {len(video_numbers)} videos to process: {video_numbers}")

        input_dir = self.input_dir
        output_dir = self.output_dir
        font_path = self.font_path

        # Create a pool of workers to process videos in parallel
        with mp.Pool(self.max_workers) as pool:
            results = pool.map(self.process_single_video,
                               [(video_num, input_dir, output_dir, font_path, fps, res_x, res_y) for video_num in
                                video_numbers])

        # Log the results
        for video_num, success, result in results:
            if success:
                self.logger.info(f"Successfully processed video {video_num}: {result}")
            else:
                self.logger.error(f"Failed to process video {video_num}: {result}")
