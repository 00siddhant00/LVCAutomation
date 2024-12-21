from batch_processor import BatchProcessor

def main():
    """Main entry point for the batch video generation system."""
    # Configuration
    input_dir = "input_files"
    output_dir = "output_files"
    font_path = "klementin.otf"

    # Create and run the batch processor
    processor = BatchProcessor(input_dir, output_dir, font_path)
    processor.process_batch()


if __name__ == "__main__":
    main()