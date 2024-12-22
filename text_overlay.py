from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
from moviepy.editor import ImageClip


class TextOverlay:
    def __init__(self, font_path, font_size=40, font_color=(255, 255, 255),
                 shadow_color=(0, 0, 0), shadow_offset=(4, 4), shadow_spread=5,
                 shadow_opacity=0.5, resolution_scale=4):
        """Initialize text overlay properties."""
        self.font_size = font_size
        self.font = ImageFont.truetype(font_path, font_size * resolution_scale)
        self.font_color = font_color
        self.shadow_color = (
            *shadow_color,
            int(255 * shadow_opacity),
        )  # Convert shadow color to RGBA with opacity
        self.shadow_offset = tuple(i * resolution_scale for i in shadow_offset)
        self.shadow_spread = shadow_spread * resolution_scale
        self.resolution_scale = resolution_scale

    def generate_text_image(self, text):
        """Generate a high-resolution PIL Image with text and enhanced shadow."""
        # Dynamically adjust font size for longer texts
        max_font_size = 120  # Maximum font size
        min_font_size = 60  # Minimum font size
        scale_factor = 0.5  # Adjust based on length
        dynamic_font_size = max(min_font_size, max_font_size - int(len(text) * scale_factor))
        high_res_font = ImageFont.truetype(self.font.path, dynamic_font_size * self.resolution_scale)

        # Calculate text size at high resolution
        temp_img = Image.new('RGBA', (1, 1))
        temp_draw = ImageDraw.Draw(temp_img)
        text_bbox = temp_draw.textbbox((0, 0), text, font=high_res_font)

        # Create larger image to accommodate shadow spread
        padding = self.shadow_spread * 4
        img_size = (text_bbox[2] - text_bbox[0] + padding * 2,
                    text_bbox[3] - text_bbox[1] + padding * 2)

        # Create separate images for shadow and text
        shadow_img = Image.new('RGBA', img_size, (0, 0, 0, 0))
        text_img = Image.new('RGBA', img_size, (0, 0, 0, 0))

        # Draw shadow
        shadow_draw = ImageDraw.Draw(shadow_img)
        shadow_pos = (padding + self.shadow_offset[0],
                      padding + self.shadow_offset[1])
        shadow_draw.text(shadow_pos, text, font=high_res_font,
                         fill=self.shadow_color)

        # Apply Gaussian blur to shadow
        shadow_img = shadow_img.filter(
            ImageFilter.GaussianBlur(radius=self.shadow_spread)
        )

        # Draw main text
        text_draw = ImageDraw.Draw(text_img)
        text_draw.text((padding, padding), text,
                       font=high_res_font, fill=self.font_color)

        # Composite shadow and text
        high_res_img = Image.alpha_composite(shadow_img, text_img)

        # Downscale to target resolution using LANCZOS resampling
        target_size = (
            img_size[0] // self.resolution_scale,
            img_size[1] // self.resolution_scale,
        )
        final_img = high_res_img.resize(target_size, Image.Resampling.LANCZOS)
        return final_img

    def create_text_clip(self, text, start, duration, position='center'):
        """Create a MoviePy clip with the text overlay."""
        text_img = self.generate_text_image(text)
        clip = ImageClip(np.array(text_img))
        return (clip.set_start(start)
                .set_duration(duration)
                .set_position(position))
