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
    img = Image.new('RGB', (WIDTH, HEIGHT), 'skyblue')
    draw = ImageDraw.Draw(img)

    prompt = prompt.lower()

    if 'mountain' in prompt:
        draw.polygon([(0, 300), (200, 150), (400, 300), (600, 100), (800, 300), (800, 600), (0, 600)], fill="#a0c4ff")
        draw.polygon([(0, 400), (150, 250), (300, 400), (450, 220), (600, 400), (800, 250), (800, 600), (0, 600)], fill="#6699cc")
        draw.polygon([(0, 500), (200, 350), (400, 500), (600, 350), (800, 500), (800, 600), (0, 600)], fill="#336699")
    if 'sun' in prompt or 'sunny' in prompt:
        draw.ellipse((650, 50, 750, 150), fill='orange')
        for i in range(8):
            x1 = 700 + 70 * (i % 2)
            y1 = 100 + 70 * (1 if i < 4 else -1)
            draw.line((700, 100, x1, y1), fill='orange', width=3)
    if 'cloud' in prompt:
        draw.ellipse((100, 80, 160, 120), fill='white')
        draw.ellipse((130, 60, 190, 120), fill='white')
        draw.ellipse((160, 80, 220, 120), fill='white')
    if 'river' in prompt:
        river_path = [(300, 600), (350, 500), (400, 450), (450, 400), (500, 300), (520, 200), (530, 100)]
        draw.line(river_path, fill='blue', width=40)
    if 'tree' in prompt or 'forest' in prompt:
        for x in range(50, 800, 150):
            draw.rectangle((x + 10, 490, x + 20, 530), fill='saddlebrown')
            draw.polygon([(x, 500), (x + 15, 450), (x + 30, 500)], fill='green')
    if 'bird' in prompt:
        for x in range(100, 700, 100):
            draw.arc((x, 70, x+15, 80), start=0, end=180, fill='black')
            draw.arc((x+10, 70, x+25, 80), start=0, end=180, fill='black')
            draw.ellipse((x+10, 75, x+13, 78), fill='black')
    if 'cow' in prompt:
        draw.rectangle((200, 520, 240, 540), fill='white')
        draw.rectangle((230, 525, 240, 535), fill='black')
        draw.ellipse((205, 525, 210, 530), fill='black')
    if 'goat' in prompt:
        draw.rectangle((300, 530, 330, 545), fill='lightgray')
        draw.ellipse((295, 532, 305, 540), fill='gray')


    filename = f'{safe_prompt}.png'
    filepath = os.path.join(IMAGE_FOLDER, filename)
    img.save(filepath)
    return filename

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.form['prompt']
    filename = generate_image(prompt)
    image_url = f'/{IMAGE_FOLDER}/{filename}'
    return render_template('index.html', prompt=prompt, image_url=image_url)

# Serve static files
@app.route('/static/generated_images/<path:filename>')
def static_files(filename):
    return send_from_directory(IMAGE_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
