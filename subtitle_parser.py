import pysrt

class SubtitleParser:
    @staticmethod
    def parse_subtitle_file(file_path):
        """Parse SRT file and return list of (start_time, duration, text)."""
        subs = pysrt.open(file_path)
        return [(sub.start.ordinal / 1000.0,
                (sub.end - sub.start).ordinal / 1000.0,
                sub.text) for sub in subs]