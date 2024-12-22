from batch_processor import ParallelBatchProcessor


class Config:
    def __init__(self, fps, res_x, res_y):
        self.fps = fps
        self.res_x = res_x
        self.res_y = res_y


def main():
    """Example usage of the parallel batch processor."""
    # Configuration
    input_dir = "input_files"
    output_dir = "output_files"
    font_path = "klementin.otf"
    div = 1

    # Create and run processor
    processor = ParallelBatchProcessor(
        input_dir=input_dir,
        output_dir=output_dir,
        font_path=font_path,
        max_workers=None  # Will use CPU count - 1
    )

    config = Config(fps=5, res_x=int(2560 / div), res_y=int(1440 / div))

    print(f"x : {config.res_x}, y : {config.res_y}, fps: {config.fps}")
    processor.process_videos_in_parallel(config)


if __name__ == "__main__":
    main()
