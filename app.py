from flask import Flask, render_template, request, send_from_directory
from PIL import Image, ImageDraw
import os
import re
import colorsys

app = Flask(__name__)
IMAGE_FOLDER = 'static/generated_images'
PROMPTS_FILE = 'prompts.txt'
os.makedirs(IMAGE_FOLDER, exist_ok=True)

WIDTH, HEIGHT = 800, 600

def create_gradient(draw, y_start, y_end, color1, color2):
    for y in range(y_start, y_end):
        ratio = (y - y_start) / (y_end - y_start)
        r1, g1, b1 = color1
        r2, g2, b2 = color2
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

def generate_image(prompt):
    try:
        # Create a new image with a gradient sky background
        img = Image.new('RGB', (WIDTH, HEIGHT), 'white')
        draw = ImageDraw.Draw(img)
        
        # Create sky gradient
        create_gradient(draw, 0, HEIGHT//2, (135, 206, 235), (65, 105, 225))
        
        # Convert prompt to lowercase for easier matching
        prompt = prompt.lower()
        
        # Improved drawing based on prompt keywords
        if 'mountain' in prompt:
            # Create multiple mountain layers with different colors
            mountain_colors = [(101, 67, 33), (139, 69, 19), (160, 82, 45)]
            for i, color in enumerate(mountain_colors):
                points = [
                    (0, HEIGHT - 100 + i*50),
                    (WIDTH//4, HEIGHT//2 - i*30),
                    (WIDTH//2, HEIGHT - 150 + i*40),
                    (3*WIDTH//4, HEIGHT//3 - i*20),
                    (WIDTH, HEIGHT - 200 + i*60),
                    (WIDTH, HEIGHT),
                    (0, HEIGHT)
                ]
                draw.polygon(points, fill=color)
        
        if 'sun' in prompt:
            # Create a glowing sun effect
            for radius in range(60, 30, -5):
                draw.ellipse((650-radius, 50-radius, 750+radius, 150+radius), 
                           fill=(255, 255, min(255, 200 + radius)))
            draw.ellipse((650, 50, 750, 150), fill='yellow')
            # Sun rays
            for i in range(12):
                angle = i * 30
                x = 700 + 80 * (1 if i < 6 else -1)
                y = 100 + 80 * (1 if i < 6 else -1)
                draw.line((700, 100, x, y), fill='yellow', width=4)
        
        if 'cloud' in prompt:
            # Create fluffy clouds
            for x in [100, 300, 500]:
                for offset in [(0,0), (20,-10), (40,0), (20,10)]:
                    draw.ellipse((x+offset[0], 80+offset[1], x+offset[0]+40, 120+offset[1]), 
                               fill='white')
        
        if 'tree' in prompt:
            # Create more natural-looking trees
            for x in range(100, 700, 200):
                # Tree trunk with gradient
                for y in range(400, 500):
                    ratio = (y - 400) / 100
                    brown = (139, 69, 19)
                    dark_brown = (101, 67, 33)
                    r = int(brown[0] + (dark_brown[0] - brown[0]) * ratio)
                    g = int(brown[1] + (dark_brown[1] - brown[1]) * ratio)
                    b = int(brown[2] + (dark_brown[2] - brown[2]) * ratio)
                    draw.line([(x, y), (x + 20, y)], fill=(r, g, b))
                
                # Tree foliage with multiple layers
                foliage_colors = [(34, 139, 34), (0, 100, 0), (0, 128, 0)]
                for i, color in enumerate(foliage_colors):
                    points = [
                        (x - 30 + i*10, 400 - i*20),
                        (x + 10, 300 - i*30),
                        (x + 50 - i*10, 400 - i*20)
                    ]
                    draw.polygon(points, fill=color)
        
        if 'river' in prompt:
            # Create a winding river with gradient
            river_points = [(300, HEIGHT), (350, HEIGHT-100), (400, HEIGHT-150),
                          (450, HEIGHT-200), (500, HEIGHT-250), (550, HEIGHT-200),
                          (600, HEIGHT-150), (650, HEIGHT-100), (700, HEIGHT)]
            for i in range(len(river_points)-1):
                x1, y1 = river_points[i]
                x2, y2 = river_points[i+1]
                for width in range(40, 0, -5):
                    draw.line([(x1, y1), (x2, y2)], 
                             fill=(0, 0, min(255, 200 + width)), width=width)
        
        # Create a safe filename from the prompt
        safe_prompt = re.sub(r'[^a-z0-9]', '_', prompt)[:30]
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
