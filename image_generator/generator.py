import os
from PIL import Image, ImageDraw, ImageFont
import random
from datetime import datetime

class ImageGenerator:
    def __init__(self):
        """Initialize the image generator."""
        self.output_dir = 'static/generated'
        os.makedirs(self.output_dir, exist_ok=True)

    def generate(self, prompt, width=800, height=600, quality='medium', output_format='PNG'):
        """
        Generate an image based on the prompt.
        
        Args:
            prompt (str): The text prompt for image generation
            width (int): Image width in pixels
            height (int): Image height in pixels
            quality (str): Image quality ('low', 'medium', 'high')
            output_format (str): Output image format ('PNG', 'JPEG')
            
        Returns:
            str: Path to the generated image
        """
        # For now, create a placeholder image with the prompt text
        # In a real implementation, this would call an AI image generation API
        image = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(image)
        
        # Add some basic text to show the prompt
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except IOError:
            font = ImageFont.load_default()
            
        # Draw the prompt text
        text = f"Prompt: {prompt}\n(Placeholder image)"
        draw.text((10, 10), text, fill='black', font=font)
        
        # Generate a unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"generated_{timestamp}.{output_format.lower()}"
        output_path = os.path.join(self.output_dir, filename)
        
        # Save the image
        image.save(output_path, format=output_format, quality=self._get_quality_value(quality))
        
        return output_path
    
    def _get_quality_value(self, quality):
        """Convert quality string to numeric value."""
        quality_map = {
            'low': 60,
            'medium': 80,
            'high': 95
        }
        return quality_map.get(quality.lower(), 80) 