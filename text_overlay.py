from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
from moviepy.editor import ImageClip, ImageSequenceClip, concatenate_videoclips
import math


class TextOverlay:
    def __init__(self, font_path, font_size=40, font_color=(255, 255, 255),
                 shadow_color=(0, 0, 0), shadow_offset=(4, 4), shadow_spread=5,
                 shadow_opacity=0.5, resolution_scale=4, fade_frames=7):
        """Initialize text overlay properties."""
        self.font_size = font_size
        self.font = ImageFont.truetype(font_path, font_size * resolution_scale)
        self.font_color = font_color
        self.shadow_color = (*shadow_color, int(255 * shadow_opacity))
        self.shadow_offset = tuple(i * resolution_scale for i in shadow_offset)
        self.shadow_spread = shadow_spread * resolution_scale
        self.resolution_scale = resolution_scale
        self.fade_frames = fade_frames  # Number of frames for fade effect

    def generate_text_image(self, text, opacity=1.0):
        """Generate a high-resolution PIL Image with text and enhanced shadow with opacity control."""
        # Dynamically adjust font size for longer texts
        max_font_size = 150
        min_font_size = 60
        scale_factor = 0.5
        dynamic_font_size = max(min_font_size, max_font_size - int(len(text) * scale_factor))
        high_res_font = ImageFont.truetype(self.font.path, dynamic_font_size * self.resolution_scale)

        # Calculate text size at high resolution
        temp_img = Image.new('RGBA', (1, 1))
        temp_draw = ImageDraw.Draw(temp_img)
        text_bbox = temp_draw.textbbox((0, 0), text, font=high_res_font)

        # Create larger image with padding
        padding = self.shadow_spread * 4
        img_size = (text_bbox[2] - text_bbox[0] + padding * 2,
                    text_bbox[3] - text_bbox[1] + padding * 2)

        # Create separate images for shadow and text
        shadow_img = Image.new('RGBA', img_size, (0, 0, 0, 0))
        text_img = Image.new('RGBA', img_size, (0, 0, 0, 0))

        # Adjust colors for opacity
        shadow_color = (*self.shadow_color[:3], int(self.shadow_color[3] * opacity))
        font_color = (*self.font_color[:3], int(255 * opacity))

        # Draw shadow with adjusted opacity
        shadow_draw = ImageDraw.Draw(shadow_img)
        shadow_pos = (padding + self.shadow_offset[0],
                      padding + self.shadow_offset[1])
        shadow_draw.text(shadow_pos, text, font=high_res_font, fill=shadow_color)

        # Apply Gaussian blur to shadow
        shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(radius=self.shadow_spread))

        # Draw main text with adjusted opacity
        text_draw = ImageDraw.Draw(text_img)
        text_draw.text((padding, padding), text, font=high_res_font, fill=font_color)

        # Composite shadow and text
        high_res_img = Image.alpha_composite(shadow_img, text_img)

        # Downscale to target resolution
        target_size = (img_size[0] // self.resolution_scale,
                       img_size[1] // self.resolution_scale)
        final_img = high_res_img.resize(target_size, Image.Resampling.LANCZOS)
        return final_img

    def _generate_fade_sequence(self, text, fade_in=True):
        """Generate a sequence of images with fade effect."""
        frames = []
        for i in range(self.fade_frames):
            if fade_in:
                opacity = i / (self.fade_frames - 1)
            else:
                opacity = 1 - (i / (self.fade_frames - 1))

            # Use smooth easing function
            opacity = self._ease_in_out(opacity)
            frames.append(np.array(self.generate_text_image(text, opacity=opacity)))
        return frames

    def _ease_in_out(self, x):
        """Apply smooth easing function to make the fade more natural."""
        if x < 0.5:
            return math.pow(2, 20 * x - 10) / 2
        else:
            return (2 - math.pow(2, -20 * x + 10)) / 2

    def create_text_clip(self, text, start, duration, fps=30, position='center'):
        """Create a MoviePy clip with the text overlay and fade effects."""
        print(f"started with {fps} and duration: {duration}")
        # Calculate timing for fade effects
        fade_duration = self.fade_frames / fps
        main_duration = max(0, duration - 2 * fade_duration)

        # Generate frame sequences for fade-in and fade-out
        fade_in_frames = self._generate_fade_sequence(text, fade_in=True)
        main_frame = np.array(self.generate_text_image(text, opacity=1.0))
        fade_out_frames = self._generate_fade_sequence(text, fade_in=False)

        # Create clips for each phase
        fade_in_clip = ImageSequenceClip(fade_in_frames, fps=fps).set_duration(fade_duration)
        main_clip = ImageClip(main_frame).set_duration(main_duration)
        fade_out_clip = ImageSequenceClip(fade_out_frames, fps=fps).set_duration(fade_duration)

        # Prepare all clips with position
        # fade_in_clip = fade_in_clip.set_position(960, 540)
        # main_clip = main_clip.set_position(960, 540)
        # fade_out_clip = fade_out_clip.set_position(960, 540)

        # Create clip list
        clips = [fade_in_clip]
        if main_duration > 0:
            clips.append(main_clip)
        clips.append(fade_out_clip)

        # Concatenate clips
        final_clip = concatenate_videoclips(clips)

        # Set the start time for the entire concatenated clip
        final_clip = (final_clip.set_start(start).set_position(position))

        return final_clip
