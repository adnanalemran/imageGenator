"""
Scene elements module containing all drawable objects.
"""

from abc import ABC, abstractmethod
from typing import Tuple, List, Optional, Dict, Any
from dataclasses import dataclass
import math
import random
from PIL import Image, ImageDraw
import numpy as np

@dataclass
class ElementStyle:
    """Style configuration for scene elements."""
    color: str
    size: float = 1.0
    opacity: float = 1.0
    stroke_width: int = 1
    rotation: float = 0.0

class SceneElement(ABC):
    """Base class for all scene elements."""
    
    def __init__(self, style: Optional[ElementStyle] = None):
        self.style = style or ElementStyle(color="black")
        self._cache = {}
    
    @abstractmethod
    def draw(self, draw: ImageDraw.Draw, position: Tuple[int, int], **kwargs) -> None:
        """Draw the element at the specified position."""
        pass
    
    def get_bounds(self, position: Tuple[int, int]) -> Tuple[int, int, int, int]:
        """Get the bounding box of the element."""
        raise NotImplementedError
    
    def intersects(self, other: 'SceneElement', pos1: Tuple[int, int], pos2: Tuple[int, int]) -> bool:
        """Check if this element intersects with another element."""
        bounds1 = self.get_bounds(pos1)
        bounds2 = other.get_bounds(pos2)
        return not (bounds1[2] < bounds2[0] or bounds1[0] > bounds2[2] or
                   bounds1[3] < bounds2[1] or bounds1[1] > bounds2[3])

class Sun(SceneElement):
    """Sun element with rays."""
    
    def __init__(self, style: Optional[ElementStyle] = None):
        super().__init__(style or ElementStyle(color="yellow"))
        self.ray_count = 12
        self.ray_length = 20
    
    def draw(self, draw: ImageDraw.Draw, position: Tuple[int, int], **kwargs) -> None:
        x, y = position
        size = int(40 * self.style.size)
        
        # Draw sun body
        draw.ellipse((x-size, y-size, x+size, y+size), 
                    fill=self.style.color)
        
        # Draw rays
        for i in range(self.ray_count):
            angle = i * (360 / self.ray_count)
            rad = math.radians(angle)
            ray_length = int(self.ray_length * self.style.size)
            
            x1 = x + int(size * math.cos(rad))
            y1 = y + int(size * math.sin(rad))
            x2 = x + int((size + ray_length) * math.cos(rad))
            y2 = y + int((size + ray_length) * math.sin(rad))
            
            draw.line((x1, y1, x2, y2), 
                     fill=self.style.color,
                     width=self.style.stroke_width)
    
    def get_bounds(self, position: Tuple[int, int]) -> Tuple[int, int, int, int]:
        x, y = position
        size = int(40 * self.style.size) + self.ray_length
        return (x-size, y-size, x+size, y+size)

class Tree(SceneElement):
    """Tree element with trunk and foliage."""
    
    def __init__(self, style: Optional[ElementStyle] = None):
        trunk_style = ElementStyle(color="saddlebrown")
        foliage_style = ElementStyle(color="forestgreen")
        super().__init__(style)
        self.trunk_style = trunk_style
        self.foliage_style = foliage_style
    
    def draw(self, draw: ImageDraw.Draw, position: Tuple[int, int], **kwargs) -> None:
        x, y = position
        trunk_width = int(20 * self.style.size)
        trunk_height = int(60 * self.style.size)
        foliage_size = int(50 * self.style.size)
        
        # Draw trunk
        draw.rectangle((x-trunk_width//2, y, x+trunk_width//2, y+trunk_height),
                      fill=self.trunk_style.color)
        
        # Draw foliage
        for offset in [(0, -foliage_size), (-foliage_size, 0), (foliage_size, 0)]:
            draw.ellipse((x+offset[0]-foliage_size//2, y+offset[1]-foliage_size//2,
                         x+offset[0]+foliage_size//2, y+offset[1]+foliage_size//2),
                        fill=self.foliage_style.color)
    
    def get_bounds(self, position: Tuple[int, int]) -> Tuple[int, int, int, int]:
        x, y = position
        trunk_width = int(20 * self.style.size)
        trunk_height = int(60 * self.style.size)
        foliage_size = int(50 * self.style.size)
        return (x-foliage_size, y-foliage_size, x+foliage_size, y+trunk_height)

class Bird(SceneElement):
    """Bird element."""
    
    def __init__(self, style: Optional[ElementStyle] = None):
        super().__init__(style or ElementStyle(color="black"))
    
    def draw(self, draw: ImageDraw.Draw, position: Tuple[int, int], **kwargs) -> None:
        x, y = position
        size = int(20 * self.style.size)
        
        # Draw body
        draw.ellipse((x, y, x+size, y+size//2), fill=self.style.color)
        
        # Draw head
        draw.ellipse((x+size-5, y-5, x+size+5, y+5), fill=self.style.color)
        
        # Draw beak
        draw.polygon([(x+size//3, y), (x+size//2, y-15), (x+size//2, y)], fill=self.style.color)
        
        # Draw wings
        draw.line((x, y+size//2, x-10, y+size), fill=self.style.color, width=2)
        draw.line((x, y+size//2, x-10, y+size//2), fill=self.style.color, width=2)
    
    def get_bounds(self, position: Tuple[int, int]) -> Tuple[int, int, int, int]:
        x, y = position
        size = int(20 * self.style.size)
        return (x-10, y-5, x+size+5, y+size)

class Mountain(SceneElement):
    """Mountain element."""
    
    def __init__(self, style: Optional[ElementStyle] = None):
        super().__init__(style or ElementStyle(color="#a0c4ff"))
        self.secondary_color = "#6699cc"
        self.tertiary_color = "#336699"
    
    def draw(self, draw: ImageDraw.Draw, position: Tuple[int, int], **kwargs) -> None:
        x, y = position
        width = int(400 * self.style.size)
        height = int(200 * self.style.size)
        
        # Draw main mountain
        draw.polygon([(x, y), (x+width//4, y-height//2), (x+width//2, y),
                     (x+3*width//4, y-height//3), (x+width, y), (x+width, y+height), (x, y+height)],
                    fill=self.style.color)
        
        # Draw secondary mountain
        draw.polygon([(x, y-height//4), (x+width//3, y-height//2), (x+2*width//3, y-height//4),
                     (x+width, y-height//3), (x+width, y), (x, y)],
                    fill=self.secondary_color)
        
        # Draw tertiary mountain
        draw.polygon([(x, y+height//4), (x+width//2, y), (x+width, y+height//4),
                     (x+width, y+height//2), (x, y+height//2)],
                    fill=self.tertiary_color)
    
    def get_bounds(self, position: Tuple[int, int]) -> Tuple[int, int, int, int]:
        x, y = position
        width = int(400 * self.style.size)
        height = int(200 * self.style.size)
        return (x, y-height//2, x+width, y+height)

class River(SceneElement):
    """River element."""
    
    def __init__(self, style: Optional[ElementStyle] = None):
        super().__init__(style or ElementStyle(color="blue"))
    
    def draw(self, draw: ImageDraw.Draw, position: Tuple[int, int], **kwargs) -> None:
        x, y = position
        width = int(800 * self.style.size)
        height = int(200 * self.style.size)
        
        # Draw river
        draw.polygon([(x, y), (x+width, y+height//2), (x+width, y+height), (x, y+height)],
                    fill=self.style.color)
        
        # Add some wave details
        for i in range(0, width, 50):
            wave_height = random.randint(5, 15)
            draw.arc((x+i, y+height//2, x+i+50, y+height//2+wave_height),
                    0, 180, fill="lightblue", width=2)
    
    def get_bounds(self, position: Tuple[int, int]) -> Tuple[int, int, int, int]:
        x, y = position
        width = int(800 * self.style.size)
        height = int(200 * self.style.size)
        return (x, y, x+width, y+height)

class Cloud(SceneElement):
    """Cloud element."""
    
    def __init__(self, style: Optional[ElementStyle] = None):
        super().__init__(style or ElementStyle(color="white"))
    
    def draw(self, draw: ImageDraw.Draw, position: Tuple[int, int], **kwargs) -> None:
        x, y = position
        size = int(100 * self.style.size)
        
        # Draw multiple circles to form a cloud
        for i in range(5):
            offset = i * 20
            draw.ellipse((x+offset, y, x+offset+size//2, y+size//3),
                        fill=self.style.color)
    
    def get_bounds(self, position: Tuple[int, int]) -> Tuple[int, int, int, int]:
        x, y = position
        size = int(100 * self.style.size)
        return (x, y, x+size+80, y+size//3)

class Star(SceneElement):
    """Star element."""
    
    def __init__(self, style: Optional[ElementStyle] = None):
        super().__init__(style or ElementStyle(color="white"))
    
    def draw(self, draw: ImageDraw.Draw, position: Tuple[int, int], **kwargs) -> None:
        x, y = position
        size = int(4 * self.style.size)
        draw.ellipse((x, y, x+size, y+size), fill=self.style.color)
    
    def get_bounds(self, position: Tuple[int, int]) -> Tuple[int, int, int, int]:
        x, y = position
        size = int(4 * self.style.size)
        return (x, y, x+size, y+size)

class Cow(SceneElement):
    """Cow element."""
    
    def __init__(self, style: Optional[ElementStyle] = None):
        super().__init__(style or ElementStyle(color="black"))
        self.spots_color = "white"
    
    def draw(self, draw: ImageDraw.Draw, position: Tuple[int, int], **kwargs) -> None:
        x, y = position
        body_width = int(60 * self.style.size)
        body_height = int(30 * self.style.size)
        
        # Draw body
        draw.rectangle((x, y, x+body_width, y+body_height), fill=self.style.color)
        
        # Draw legs
        for i in range(4):
            leg_x = x + (i * body_width // 3)
            draw.rectangle((leg_x, y+body_height, leg_x+5, y+body_height+20),
                         fill=self.style.color)
        
        # Draw head
        draw.rectangle((x-20, y+5, x, y+20), fill=self.style.color)
        
        # Draw horns
        draw.line((x-20, y+5, x-25, y), fill=self.style.color, width=2)
        draw.line((x-20, y+5, x-15, y), fill=self.style.color, width=2)
        
        # Draw spots
        for _ in range(5):
            spot_x = x + random.randint(0, body_width-10)
            spot_y = y + random.randint(0, body_height-10)
            spot_size = random.randint(5, 15)
            draw.ellipse((spot_x, spot_y, spot_x+spot_size, spot_y+spot_size),
                        fill=self.spots_color)
    
    def get_bounds(self, position: Tuple[int, int]) -> Tuple[int, int, int, int]:
        x, y = position
        body_width = int(60 * self.style.size)
        body_height = int(30 * self.style.size)
        return (x-25, y, x+body_width, y+body_height+20)

class Goat(SceneElement):
    """Goat element."""
    
    def __init__(self, style: Optional[ElementStyle] = None):
        super().__init__(style or ElementStyle(color="black"))
    
    def draw(self, draw: ImageDraw.Draw, position: Tuple[int, int], **kwargs) -> None:
        x, y = position
        body_width = int(40 * self.style.size)
        body_height = int(20 * self.style.size)
        
        # Draw body
        draw.rectangle((x, y, x+body_width, y+body_height), fill=self.style.color)
        
        # Draw legs
        for i in range(4):
            leg_x = x + (i * body_width // 3)
            draw.rectangle((leg_x, y+body_height, leg_x+4, y+body_height+15),
                         fill=self.style.color)
        
        # Draw head
        draw.rectangle((x-15, y, x, y+10), fill=self.style.color)
        
        # Draw horns
        draw.line((x-10, y+10, x-10, y+15), fill=self.style.color, width=2)
    
    def get_bounds(self, position: Tuple[int, int]) -> Tuple[int, int, int, int]:
        x, y = position
        body_width = int(40 * self.style.size)
        body_height = int(20 * self.style.size)
        return (x-15, y, x+body_width, y+body_height+15)

class ElementFactory:
    """Factory for creating scene elements."""
    
    _elements: Dict[str, type] = {
        'sun': Sun,
        'tree': Tree,
        'bird': Bird,
        'mountain': Mountain,
        'river': River,
        'cloud': Cloud,
        'star': Star,
        'cow': Cow,
        'goat': Goat
    }
    
    @classmethod
    def create(cls, element_type: str, style: Optional[ElementStyle] = None) -> SceneElement:
        """Create a new scene element of the specified type."""
        if element_type not in cls._elements:
            raise ValueError(f"Unknown element type: {element_type}")
        return cls._elements[element_type](style)
    
    @classmethod
    def register_element(cls, name: str, element_class: type) -> None:
        """Register a new element type."""
        if not issubclass(element_class, SceneElement):
            raise TypeError("Element class must inherit from SceneElement")
        cls._elements[name] = element_class 