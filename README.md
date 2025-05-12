# Image Generator

A Python-based image generator that creates scenes from text prompts using procedural generation. The generator creates visually appealing images by combining various elements like trees, mountains, people, and animals based on natural language descriptions.

## Features

- 🎨 **Rich Visual Elements**: Supports multiple scene elements including:
  - Nature: sun, clouds, trees, mountains, rivers, birds
  - Animals: cows, goats
  - School: students, school buildings, backpacks
  - Sports: football fields, players
  - And more!

- 🎯 **Smart Scene Composition**:
  - Automatic element placement and layering
  - Intelligent overlap prevention
  - Context-aware element selection
  - Realistic positioning based on element type

- 🎨 **Advanced Visual Effects**:
  - Textures (wood, metal, fabric)
  - Patterns (stripes, dots, checkered)
  - Dynamic shadows and highlights
  - Post-processing for enhanced quality

- ⚡ **Performance Features**:
  - Parallel processing for batch generation
  - Element caching for faster rendering
  - Configurable quality settings
  - Memory-efficient processing

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/image-generator.git
cd imageGenatorAI
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Generate a single image:
```bash
python generate.py "a sunny day at school with students playing"
```

Generate multiple images from a file:
```bash
python generate.py -f prompts.txt
```

Interactive mode:
```bash
python generate.py -i
```

### Command Line Options

#### Image Settings
- `-w/--width`: Image width (default: 800)
- `-H/--height`: Image height (default: 600)
- `--format`: Output format (PNG, JPEG, BMP, GIF)
- `--quality`: Image quality (1-100)

#### Generation Settings
- `--seed`: Random seed for reproducibility
- `--min-elements`: Minimum elements per scene
- `--max-elements`: Maximum elements per scene

#### Visual Effects
- `--no-textures`: Disable textures
- `--no-patterns`: Disable patterns
- `--no-shadows`: Disable shadows
- `--no-highlights`: Disable highlights
- `--render-quality`: Set render quality (low/medium/high)

#### Output Settings
- `-o/--output`: Output directory
- `--prefix`: Filename prefix
- `--suffix`: Filename suffix

#### Performance Settings
- `--parallel`: Enable parallel processing
- `--max-workers`: Number of parallel workers
- `--cache-size`: Element cache size

### Example Commands

1. Generate a high-quality image:
```bash
python generate.py "a peaceful scene with mountains and trees" --width 1200 --height 800 --quality 95 --format PNG
```

2. Generate multiple images in parallel:
```bash
python generate.py -f prompts.txt --parallel --max-workers 4
```

3. Generate with custom visual effects:
```bash
python generate.py "a sunny day at school" --render-quality high --no-textures
```

## Available Elements

### Nature Elements
- Sun
- Clouds
- Trees
- Mountains
- Rivers
- Birds

### School Elements
- School buildings
- Students (boys and girls)
- Backpacks
- Books

### Sports Elements
- Football fields
- Footballs
- Players

### Animals
- Cows
- Goats

## Configuration

The generator can be configured through a JSON configuration file. Create a `config.json` file in the project root:

```json
{
    "width": 800,
    "height": 600,
    "output_format": "PNG",
    "output_quality": 95,
    "background_color": "#87CEEB",
    "max_elements": 20,
    "min_elements": 5,
    "parallel_processing": false,
    "render_quality": "high"
}
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

<<<<<<< HEAD
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the PIL/Pillow library for image processing capabilities
- Inspired by procedural generation techniques in computer graphics
- Built with Python's rich ecosystem of libraries

## Support

If you encounter any issues or have questions, please:
1. Check the [Issues](https://github.com/yourusername/image-generator/issues) page
2. Create a new issue if your problem isn't already listed
3. Include as much detail as possible in your issue report

## Roadmap

- [ ] Add more scene elements
- [ ] Implement more advanced visual effects
- [ ] Add support for custom element styles
- [ ] Improve scene composition algorithms
- [ ] Add animation support
- [ ] Create a web interface 
=======
MIT License - see LICENSE file for details 
>>>>>>> abf0f980b4c16fa6657e38bd540b17161880e8ea
