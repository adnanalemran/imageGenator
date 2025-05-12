"""
Configuration module for the image generator.
"""

from typing import Optional, Dict, Any
from pathlib import Path
import json
from pydantic import BaseModel, Field

class GeneratorConfig(BaseModel):
    """Configuration for the image generator."""
    
    # Image dimensions
    width: int = Field(default=800, ge=100, le=4000)
    height: int = Field(default=600, ge=100, le=4000)
    
    # Output settings
    output_dir: Path = Field(default=Path("outputs"))
    output_format: str = Field(default="PNG", pattern="^(PNG|JPEG|BMP)$")
    output_quality: int = Field(default=95, ge=1, le=100)
    
    # Style settings
    background_color: str = Field(default="#87CEEB")  # Sky blue
    element_colors: Dict[str, str] = Field(default_factory=lambda: {
        "sun": "yellow",
        "tree": "forestgreen",
        "bird": "black",
        "mountain": "#a0c4ff",
        "river": "blue",
        "cloud": "white",
        "star": "white",
        "cow": "black",
        "goat": "black"
    })
    
    # Generation settings
    max_elements: int = Field(default=20, ge=1, le=100)
    min_elements: int = Field(default=5, ge=1, le=50)
    seed: Optional[int] = Field(default=None)
    
    # Performance settings
    parallel_processing: bool = Field(default=False)
    batch_size: int = Field(default=4, ge=1, le=16)
    
    class Config:
        """Pydantic model configuration."""
        arbitrary_types_allowed = True

def load_config(config_path: Optional[Path] = None) -> GeneratorConfig:
    """Load configuration from a JSON file or use defaults."""
    if config_path is None:
        return GeneratorConfig()
    
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_path) as f:
        config_data = json.load(f)
    
    return GeneratorConfig(**config_data)

def save_config(config: GeneratorConfig, config_path: Path) -> None:
    """Save configuration to a JSON file."""
    config_data = config.model_dump()
    with open(config_path, 'w') as f:
        json.dump(config_data, f, indent=4) 