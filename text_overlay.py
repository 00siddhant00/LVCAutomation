from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
from moviepy.editor import ImageClip, ImageSequenceClip, concatenate_videoclips
import math
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s')

class TextOverlay:
    def __init__(self, font_path, font_size=40, font_color=(255, 255, 255),
                 shadow_color=(0, 0, 0), shadow_offset=(4, 4), shadow_spread=5,
                 shadow_opacity=0.5, resolution_scale=4, fade_frames=12,
                 fade_in_start_scale=3, fade_in_end_scale=1.0,
                 main_start_scale=1.0, main_end_scale=0.95,
                 fade_out_start_scale=0.95, fade_out_end_scale=0.2):
        logging.debug(f"Initializing TextOverlay with font: {font_path}")
        self.font_size = font_size
        self.font = ImageFont.truetype(font_path, font_size * resolution_scale)
        self.font_color = font_color
        self.shadow_color = (*shadow_color, int(255 * shadow_opacity))
        self.shadow_offset = tuple(i * resolution_scale for i in shadow_offset)
        self.shadow_spread = shadow_spread * resolution_scale
        self.resolution_scale = resolution_scale
        self.fade_frames = fade_frames

        # Store scaling parameters
        self.fade_in_start_scale = fade_in_start_scale
        self.fade_in_end_scale = fade_in_end_scale
        self.main_start_scale = main_start_scale
        self.main_end_scale = main_end_scale
        self.fade_out_start_scale = fade_out_start_scale
        self.fade_out_end_scale = fade_out_end_scale

        self.frame_size = None

    def _calculate_base_size(self, text):
        logging.debug(f"Calculating base size for text: {text}")
        max_scale = max(self.fade_in_start_scale, self.fade_in_end_scale,
                        self.main_start_scale, self.main_end_scale,
                        self.fade_out_start_scale, self.fade_out_end_scale)

        max_font_size = 150
        min_font_size = 60
        scale_factor = 0.5
        dynamic_font_size = max(min_font_size, max_font_size - int(len(text) * scale_factor))
        high_res_font = ImageFont.truetype(self.font.path,
                                           int(dynamic_font_size * self.resolution_scale * max_scale))

        temp_img = Image.new('RGBA', (1, 1))
        temp_draw = ImageDraw.Draw(temp_img)
        text_bbox = temp_draw.textbbox((0, 0), text, font=high_res_font)

        padding = int(self.shadow_spread * 4 * max_scale)
        width = text_bbox[2] - text_bbox[0] + padding * 2
        height = text_bbox[3] - text_bbox[1] + padding * 2

        self.frame_size = (width // self.resolution_scale,
                           height // self.resolution_scale)
        logging.debug(f"Calculated frame size: {self.frame_size}")
        return width, height

    def generate_text_image(self, text, opacity=1.0, scale=1.0):
        logging.debug(f"Generating text image for: {text} with opacity: {opacity} and scale: {scale}")
        if self.frame_size is None:
            self._calculate_base_size(text)

        high_res_size = (self.frame_size[0] * self.resolution_scale,
                         self.frame_size[1] * self.resolution_scale)

        shadow_img = Image.new('RGBA', high_res_size, (0, 0, 0, 0))
        text_img = Image.new('RGBA', high_res_size, (0, 0, 0, 0))

        max_font_size = 160
        min_font_size = 60
        scale_factor = 0.5
        dynamic_font_size = max(min_font_size, max_font_size - int(len(text) * scale_factor))
        scaled_font_size = int(dynamic_font_size * self.resolution_scale * scale)
        scaled_font = ImageFont.truetype(self.font.path, scaled_font_size)

        temp_draw = ImageDraw.Draw(shadow_img)
        text_bbox = temp_draw.textbbox((0, 0), text, font=scaled_font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        x = (high_res_size[0] - text_width) // 2
        y = (high_res_size[1] - text_height) // 2

        shadow_color = (*self.shadow_color[:3], int(self.shadow_color[3] * opacity))
        font_color = (*self.font_color[:3], int(255 * opacity))

        shadow_draw = ImageDraw.Draw(shadow_img)
        shadow_pos = (x + int(self.shadow_offset[0] * scale),
                      y + int(self.shadow_offset[1] * scale))
        shadow_draw.text(shadow_pos, text, font=scaled_font, fill=shadow_color)

        shadow_img = shadow_img.filter(
            ImageFilter.GaussianBlur(radius=self.shadow_spread * scale))

        text_draw = ImageDraw.Draw(text_img)
        text_draw.text((x, y), text, font=scaled_font, fill=font_color)

        final_img = Image.alpha_composite(shadow_img, text_img)

        final_img = final_img.resize(self.frame_size, Image.Resampling.LANCZOS)
        return final_img

    def _generate_fade_sequence(self, text, fade_in=True):
        logging.debug(f"Generating fade sequence for text: {text} (fade_in={fade_in})")
        frames = []
        for i in range(self.fade_frames):
            progress = i / (self.fade_frames - 1)

            if fade_in:
                opacity = progress
            else:
                opacity = 1 - progress
            opacity = self._ease_in_out(opacity)

            if fade_in:
                scale = self._lerp(self.fade_in_start_scale,
                                   self.fade_in_end_scale,
                                   self._ease_out_expo(progress))
            else:
                scale = self._lerp(self.fade_out_start_scale,
                                   self.fade_out_end_scale,
                                   self._ease_in_expo(progress))

            frames.append(np.array(self.generate_text_image(text,
                                                            opacity=opacity,
                                                            scale=scale)))
        return frames

    def _generate_main_sequence(self, text, duration, fps):
        logging.debug(f"Generating main sequence for text: {text} with duration: {duration}, fps: {fps}")
        frames = []
        total_frames = int(duration * fps)

        for i in range(total_frames):
            progress = i / max(1, total_frames - 1)
            # Direct linear scaling without easing
            scale = self.main_start_scale + (self.main_end_scale - self.main_start_scale) * progress

            frames.append(np.array(self.generate_text_image(text,
                                                        opacity=1.0,
                                                        scale=scale)))
        return frames

    def _lerp(self, start, end, progress):
        return start + (end - start) * progress

    def _ease_in_out(self, x):
        if x < 0.5:
            return math.pow(2, 20 * x - 10) / 2
        else:
            return (2 - math.pow(2, -20 * x + 10)) / 2

    def _ease_out_expo(self, x):
        return 1 - math.pow(2, -8 * x)

    def _ease_in_expo(self, x):
        return math.pow(2, 8 * x - 8)

    def _ease_in_out_cubic(self, x):
        if x < 0.5:
            return 4 * x * x * x
        else:
            return 1 - math.pow(-2 * x + 2, 3) / 2

    def create_text_clip(self, text, start, duration, fps=30, position='center'):
        logging.debug(f"Creating text clip for text: {text} at start: {start}, duration: {duration}, fps: {fps}")
        self._calculate_base_size(text)

        fade_duration = self.fade_frames / fps
        main_duration = max(0, duration - 2 * fade_duration)

        fade_in_frames = self._generate_fade_sequence(text, fade_in=True)
        main_frames = self._generate_main_sequence(text, main_duration, fps)
        fade_out_frames = self._generate_fade_sequence(text, fade_in=False)

        fade_in_clip = ImageSequenceClip(fade_in_frames, fps=fps).set_duration(fade_duration)
        main_clip = ImageSequenceClip(main_frames, fps=fps).set_duration(main_duration)
        fade_out_clip = ImageSequenceClip(fade_out_frames, fps=fps).set_duration(fade_duration)

        clips = [fade_in_clip]
        if main_duration > 0:
            clips.append(main_clip)
        clips.append(fade_out_clip)

        final_clip = concatenate_videoclips(clips)
        final_clip = final_clip.set_start(start).set_position(position)

        logging.debug(f"Text clip created successfully.")
        return final_clip
