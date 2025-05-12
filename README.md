# Simple Image Generator AI

A Python-based image generator that creates simple, artistic images based on text prompts. This project uses Flask for the web interface and PIL (Python Imaging Library) for image generation.

## Features

- Generate images from text prompts
- Support for multiple elements and combinations
- Simple and intuitive web interface
- Real-time image generation
- Customizable scene elements
- Support for both indoor and outdoor scenes

## Supported Elements

### Nature Elements
- Mountains
- Sun
- Clouds
- Trees
- Rivers
- Flowers

### Animals
- Cows

### People
- Man
- Woman
- Generic person

### Objects
- House
- Table
- Computer
- Book

## Requirements

- Python 3.7 or higher
- Flask
- Pillow (PIL)
- A modern web browser

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/imageGenatorAI.git
cd imageGenatorAI
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Flask server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Enter a prompt in the text field and click "Generate" to create an image.

## Example Prompts

The project includes a `prompts.txt` file with example prompts. Here are some categories:

### Simple Scenes
- mountain
- sun
- cloud
- tree
- river

### Nature Scenes
- mountain with sun
- mountain with river
- sunny day with clouds

### Indoor Scenes
- table with computer
- person reading book
- woman at table

### Complex Scenes
- mountain with sun and clouds
- house with garden and flowers
- person reading book under tree

## How It Works

1. The user enters a text prompt through the web interface
2. The application processes the prompt and identifies keywords
3. The image generator creates a new image based on the identified elements
4. The generated image is saved and displayed to the user

## Project Structure

```
imageGenatorAI/
├── app.py              # Main Flask application
├── prompts.txt         # Example prompts
├── requirements.txt    # Python dependencies
├── static/
│   └── generated_images/  # Generated images storage
└── templates/
    └── index.html      # Web interface template
```

## Customization

You can customize the image generator by:
- Modifying the element drawing functions in `app.py`
- Adding new elements to the generator
- Adjusting colors and sizes of existing elements
- Creating new prompt combinations

## Contributing

Feel free to contribute to this project by:
1. Forking the repository
2. Creating a new branch
3. Making your changes
4. Submitting a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Flask for the web framework
- Pillow (PIL) for image generation
- Python community for various libraries and tools

## Support

If you encounter any issues or have questions:
1. Check the existing issues
2. Create a new issue with a detailed description
3. Include steps to reproduce the problem

## Future Improvements

- Add more elements and scenes
- Implement color customization
- Add animation support
- Improve image quality
- Add more complex scene combinations
- Implement user accounts and image saving
- Add export options for different image formats 