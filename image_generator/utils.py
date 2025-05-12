"""
Utility functions for the image generator.
"""

from typing import Tuple, List, Optional
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

class ImageUtils:
    """Utility class for image manipulation."""
    
    @staticmethod
    def sin_deg(deg: float) -> float:
        """Calculate sine of angle in degrees."""
        return math.sin(math.radians(deg))
    
    @staticmethod
    def cos_deg(deg: float) -> float:
        """Calculate cosine of angle in degrees."""
        return math.cos(math.radians(deg))
    
    @staticmethod
    def rotate_point(x: float, y: float, angle: float, center_x: float = 0, center_y: float = 0) -> Tuple[float, float]:
        """Rotate a point around a center by given angle in degrees."""
        rad = math.radians(angle)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        
        x -= center_x
        y -= center_y
        
        new_x = x * cos_a - y * sin_a
        new_y = x * sin_a + y * cos_a
        
        return new_x + center_x, new_y + center_y
    
    @staticmethod
    def apply_blur(image: Image.Image, radius: float = 2.0) -> Image.Image:
        """Apply Gaussian blur to image."""
        return image.filter(ImageFilter.GaussianBlur(radius))
    
    @staticmethod
    def adjust_brightness(image: Image.Image, factor: float) -> Image.Image:
        """Adjust image brightness."""
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(factor)
    
    @staticmethod
    def adjust_contrast(image: Image.Image, factor: float) -> Image.Image:
        """Adjust image contrast."""
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(factor)
    
    @staticmethod
    def add_noise(image: Image.Image, amount: float = 0.1) -> Image.Image:
        """Add random noise to image."""
        img_array = np.array(image)
        noise = np.random.normal(0, amount * 255, img_array.shape).astype(np.uint8)
        noisy_array = np.clip(img_array + noise, 0, 255).astype(np.uint8)
        return Image.fromarray(noisy_array)
    
    @staticmethod
    def create_gradient(width: int, height: int, 
                       start_color: Tuple[int, int, int],
                       end_color: Tuple[int, int, int],
                       direction: str = 'vertical') -> Image.Image:
        """Create a gradient image."""
        image = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(image)
        
        if direction == 'vertical':
            for y in range(height):
                r = int(start_color[0] + (end_color[0] - start_color[0]) * y / height)
                g = int(start_color[1] + (end_color[1] - start_color[1]) * y / height)
                b = int(start_color[2] + (end_color[2] - start_color[2]) * y / height)
                draw.line([(0, y), (width, y)], fill=(r, g, b))
        else:  # horizontal
            for x in range(width):
                r = int(start_color[0] + (end_color[0] - start_color[0]) * x / width)
                g = int(start_color[1] + (end_color[1] - start_color[1]) * x / width)
                b = int(start_color[2] + (end_color[2] - start_color[2]) * x / width)
                draw.line([(x, 0), (x, height)], fill=(r, g, b))
        
        return image
    
    @staticmethod
    def blend_images(image1: Image.Image, image2: Image.Image, alpha: float = 0.5) -> Image.Image:
        """Blend two images together."""
        if image1.size != image2.size:
            image2 = image2.resize(image1.size)
        return Image.blend(image1, image2, alpha)
    
    @staticmethod
    def create_shadow(image: Image.Image, offset: Tuple[int, int] = (5, 5),
                     blur_radius: float = 3.0, opacity: float = 0.5) -> Image.Image:
        """Create a shadow effect for an image."""
        # Create shadow mask
        shadow = Image.new('RGBA', image.size, (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        shadow_draw.rectangle([(0, 0), image.size], fill=(0, 0, 0, int(255 * opacity)))
        
        # Apply blur and offset
        shadow = shadow.filter(ImageFilter.GaussianBlur(blur_radius))
        shadow = Image.new('RGBA', 
                         (image.size[0] + abs(offset[0]), image.size[1] + abs(offset[1])),
                         (0, 0, 0, 0))
        shadow.paste(shadow, (max(0, offset[0]), max(0, offset[1])))
        
        # Combine with original image
        result = Image.new('RGBA', shadow.size, (0, 0, 0, 0))
        result.paste(shadow, (0, 0))
        result.paste(image, (max(0, -offset[0]), max(0, -offset[1])))
        
        return result 