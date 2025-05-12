from flask import Flask, render_template, request, send_from_directory
from PIL import Image, ImageDraw
import os
import re
import random
app = Flask(__name__)
IMAGE_FOLDER = 'static/generated_images'
os.makedirs(IMAGE_FOLDER, exist_ok=True)

WIDTH, HEIGHT = 800, 600

# (Include your existing image generation logic here)
def generate_image(prompt):
    try:
        # Create a new image with a sky blue background
        img = Image.new('RGB', (WIDTH, HEIGHT), 'skyblue')
        draw = ImageDraw.Draw(img)
        
        # Convert prompt to lowercase for easier matching
        prompt = prompt.lower()
        
        # Simple drawing based on prompt keywords
        if 'mountain' in prompt:
            draw.polygon([(0, 300), (400, 150), (800, 300), (800, 600), (0, 600)], fill="#6699cc")
        
        if 'sun' in prompt:
            draw.ellipse((650, 50, 750, 150), fill='yellow')
            for i in range(8):
                angle = i * 45
                x = 700 + 70 * (1 if i < 4 else -1)
                y = 100 + 70 * (1 if i < 4 else -1)
                draw.line((700, 100, x, y), fill='yellow', width=3)
        
        if 'cloud' in prompt:
            draw.ellipse((100, 80, 200, 120), fill='white')
            draw.ellipse((150, 60, 250, 120), fill='white')
        
        if 'tree' in prompt:
            for x in range(100, 700, 200):
                # Tree trunk
                draw.rectangle((x, 400, x + 20, 500), fill='brown')
                # Tree top
                draw.polygon([(x - 30, 400), (x + 10, 300), (x + 50, 400)], fill='green')
        
        # Create a safe filename from the prompt
        safe_prompt = re.sub(r'[^a-z0-9]', '_', prompt)[:30]  # Limit length and remove special chars
        filename = f'{safe_prompt}.png'
        filepath = os.path.join(IMAGE_FOLDER, filename)
        
        # Save the image
        img.save(filepath)
        return filename
        
    except Exception as e:
        print(f"Error generating image: {str(e)}")
        return None

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        prompt = request.form.get('prompt', '').strip()
        if not prompt:
            return render_template('index.html', error="Please enter a prompt")
            
        filename = generate_image(prompt)
        if filename:
            image_url = f'/{IMAGE_FOLDER}/{filename}'
            return render_template('index.html', prompt=prompt, image_url=image_url)
        else:
            return render_template('index.html', error="Failed to generate image")
            
    except Exception as e:
        return render_template('index.html', error="An error occurred")

# Serve static files
@app.route('/static/generated_images/<path:filename>')
def static_files(filename):
    return send_from_directory(IMAGE_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
