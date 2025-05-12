"""
Main image generator module.
"""

from typing import List, Dict, Optional, Tuple, Union
from pathlib import Path
import random
import logging
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm
from rich.logging import RichHandler
import numpy as np
from PIL import Image, ImageDraw

from .config import GeneratorConfig, load_config
from .elements import SceneElement, ElementFactory, ElementStyle
from .utils import ImageUtils

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
logger = logging.getLogger("image_generator")

class ImageGenerator:
    """Main image generator class."""
    
    def __init__(self, config: Optional[GeneratorConfig] = None):
        """
        Initialize the image generator.
        
        Args:
            config: Optional configuration object
        """
        self.config = config or load_config()
        self._setup_random_seed()
        self._element_cache: Dict[str, SceneElement] = {}
        self._setup_logging()
    
    def _setup_random_seed(self) -> None:
        """Set up random seed if specified in config."""
        if self.config.seed is not None:
            random.seed(self.config.seed)
            np.random.seed(self.config.seed)
    
    def _setup_logging(self) -> None:
        """Configure logging based on environment."""
        if self.config.parallel_processing:
            logger.setLevel(logging.WARNING)
        else:
            logger.setLevel(logging.INFO)
    
    def _create_canvas(self) -> Tuple[Image.Image, ImageDraw.Draw]:
        """Create a new canvas with the configured dimensions."""
        img = Image.new("RGB", (self.config.width, self.config.height),
                       self.config.background_color)
        return img, ImageDraw.Draw(img)
    
    def _get_element(self, element_type: str) -> SceneElement:
        """Get or create a scene element with caching."""
        if element_type not in self._element_cache:
            style = ElementStyle(
                color=self.config.element_colors.get(element_type, "black")
            )
            self._element_cache[element_type] = ElementFactory.create(element_type, style)
        return self._element_cache[element_type]
    
    def _parse_prompt(self, prompt: str) -> List[str]:
        """Parse the prompt into element types."""
        # Simple keyword-based parsing
        keywords = {
            'sun': ['sun', 'sunny'],
            'tree': ['tree', 'forest', 'woods'],
            'bird': ['bird', 'birds', 'flying'],
            'mountain': ['mountain', 'mountains', 'hill', 'hills'],
            'river': ['river', 'stream', 'water'],
            'cloud': ['cloud', 'clouds', 'cloudy'],
            'star': ['star', 'stars', 'night'],
            'cow': ['cow', 'cows', 'cattle'],
            'goat': ['goat', 'goats']
        }
        
        elements = []
        prompt_lower = prompt.lower()
        
        for element_type, words in keywords.items():
            if any(word in prompt_lower for word in words):
                elements.append(element_type)
        
        return elements
    
    def _generate_positions(self, element_type: str, count: int) -> List[Tuple[int, int]]:
        """Generate valid positions for elements."""
        positions = []
        element = self._get_element(element_type)
        
        # Define position constraints based on element type
        constraints = {
            'sun': {'y_range': (50, 150)},
            'bird': {'y_range': (50, 300)},
            'cloud': {'y_range': (50, 200)},
            'star': {'y_range': (50, 300)},
            'tree': {'y_range': (350, 500)},
            'mountain': {'y_range': (300, 600)},
            'river': {'y_range': (400, 600)},
            'cow': {'y_range': (400, 500)},
            'goat': {'y_range': (450, 550)}
        }
        
        constraint = constraints.get(element_type, {})
        y_range = constraint.get('y_range', (0, self.config.height))
        
        attempts = 0
        max_attempts = count * 10  # Limit attempts to prevent infinite loops
        
        while len(positions) < count and attempts < max_attempts:
            x = random.randint(50, self.config.width - 50)
            y = random.randint(y_range[0], y_range[1])
            
            # Check for overlaps with existing elements
            position_valid = True
            for pos in positions:
                if element.intersects(element, (x, y), pos):
                    position_valid = False
                    break
            
            if position_valid:
                positions.append((x, y))
            
            attempts += 1
        
        return positions
    
    def generate(self, prompt: str, output_path: Optional[Union[str, Path]] = None) -> Path:
        """
        Generate an image based on the prompt.
        
        Args:
            prompt: Text description of the scene
            output_path: Optional path to save the image
            
        Returns:
            Path: Path to the generated image
        """
        logger.info(f"Generating image for prompt: {prompt}")
        
        # Create canvas
        img, draw = self._create_canvas()
        
        # Parse prompt and generate elements
        element_types = self._parse_prompt(prompt)
        if not element_types:
            logger.warning("No elements found in prompt")
            element_types = ['tree', 'sun']  # Default elements
        
        # Generate and draw elements
        for element_type in element_types:
            # Calculate number of elements based on min and max settings
            count = random.randint(
                self.config.min_elements,
                min(self.config.max_elements, len(element_types) * 3)
            )
            positions = self._generate_positions(element_type, count)
            
            element = self._get_element(element_type)
            for position in positions:
                element.draw(draw, position)
        
        # Save image
        if output_path is None:
            output_path = self.config.output_dir / f"{prompt.replace(' ', '_')}.{self.config.output_format.lower()}"
        else:
            output_path = Path(output_path)
        
        img.save(output_path, self.config.output_format, quality=self.config.output_quality)
        logger.info(f"Image saved to: {output_path}")
        
        return output_path
    
    def generate_batch(self, prompts: List[str], output_dir: Optional[Path] = None) -> List[Path]:
        """
        Generate multiple images from a list of prompts.
        
        Args:
            prompts: List of text descriptions
            output_dir: Optional directory to save images
            
        Returns:
            List[Path]: List of paths to generated images
        """
        output_dir = output_dir or self.config.output_dir
        output_dir.mkdir(parents=True, exist_ok=True)
        
        if self.config.parallel_processing:
            return self._generate_batch_parallel(prompts, output_dir)
        else:
            return self._generate_batch_sequential(prompts, output_dir)
    
    def _generate_batch_sequential(self, prompts: List[str], output_dir: Path) -> List[Path]:
        """Generate images sequentially with progress bar."""
        output_paths = []
        for prompt in tqdm(prompts, desc="Generating images"):
            output_path = output_dir / f"{prompt.replace(' ', '_')}.{self.config.output_format.lower()}"
            self.generate(prompt, output_path)
            output_paths.append(output_path)
        return output_paths
    
    def _generate_batch_parallel(self, prompts: List[str], output_dir: Path) -> List[Path]:
        """Generate images in parallel using multiple processes."""
        def generate_worker(prompt: str) -> Path:
            output_path = output_dir / f"{prompt.replace(' ', '_')}.{self.config.output_format.lower()}"
            self.generate(prompt, output_path)
            return output_path
        
        with ProcessPoolExecutor() as executor:
            output_paths = list(tqdm(
                executor.map(generate_worker, prompts),
                total=len(prompts),
                desc="Generating images in parallel"
            ))
        
        return output_paths 