from moviepy.editor import ImageClip
import numpy as np


class BackgroundAnimator:
    def __init__(self, image_path):
        """Initialize with path to background image."""
        self.image_path = image_path
        self.base_clip = ImageClip(image_path)

    def animate_background(self, duration, amplitude=0.1, frequency=0.5):
        """Create a breathing animation effect on the background image."""

        def resize_frame(t):
            scale = 1 + amplitude * np.sin(2 * np.pi * frequency * t)
            frame = self.base_clip.get_frame(t)
            return frame * scale

        animated_clip = self.base_clip.fl(resize_frame)
        return animated_clip.set_duration(duration)