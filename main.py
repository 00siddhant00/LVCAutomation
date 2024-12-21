from batch_processor import ParallelBatchProcessor

def main():
    """Example usage of the parallel batch processor."""
    # Configuration
    input_dir = "input_files"
    output_dir = "output_files"
    font_path = "klementin.otf"
    res_x = int(2560/4)
    res_y = int(1440/4)
    fps = 24

    # Create and run processor
    processor = ParallelBatchProcessor(
        input_dir=input_dir,
        output_dir=output_dir,
        font_path=font_path,
        max_workers=None  # Will use CPU count - 1
    )

    print(f"x : {res_x}, y : {res_y}, fps: {fps}")
    processor.process_videos_in_parallel(fps, res_x, res_y)


if __name__ == "__main__":
    main()