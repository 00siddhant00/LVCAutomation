from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip
import numpy as np


class TextOverlay:
    def __init__(self, font_path, font_size=40, font_color=(255, 255, 255),
                 shadow_color=(0, 0, 0), shadow_offset=(2, 2)):
        """Initialize text overlay properties."""
        self.font = ImageFont.truetype(font_path, font_size)
        self.font_color = font_color
        self.shadow_color = shadow_color
        self.shadow_offset = shadow_offset

    def generate_text_image(self, text):
        """Generate a PIL Image with the text and shadow."""
        temp_img = Image.new('RGBA', (1, 1))
        temp_draw = ImageDraw.Draw(temp_img)
        text_bbox = temp_draw.textbbox((0, 0), text, font=self.font)

        img_size = (text_bbox[2] - text_bbox[0] + 20,
                    text_bbox[3] - text_bbox[1] + 20)
        text_img = Image.new('RGBA', img_size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(text_img)

        shadow_position = (10 + self.shadow_offset[0],
                           10 + self.shadow_offset[1])
        draw.text(shadow_position, text, font=self.font,
                  fill=self.shadow_color)

        draw.text((10, 10), text, font=self.font, fill=self.font_color)
        return text_img

    def create_text_clip(self, text, start, duration, position='center'):
        """Create a MoviePy clip with the text overlay."""
        text_img = self.generate_text_image(text)
        clip = ImageClip(np.array(text_img))
        return (clip.set_start(start)
                .set_duration(duration)
                .set_position(position))