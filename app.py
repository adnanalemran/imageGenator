from flask import Flask, render_template, request, send_from_directory
from PIL import Image, ImageDraw
import os
import re
import colorsys
import random

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
        img = Image.new('RGB', (WIDTH, HEIGHT), 'white')
        draw = ImageDraw.Draw(img)
        
        create_gradient(draw, 0, HEIGHT//2, (135, 206, 235), (65, 105, 225))
        
        prompt = prompt.lower()
        
        if any(word in prompt for word in ['cow', 'table', 'computer', 'book', 'man', 'woman', 'person', 'grass', 'flower', 'bird']):
            create_gradient(draw, HEIGHT//2, HEIGHT, (34, 139, 34), (85, 107, 47))
        
        if 'mountain' in prompt:
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
            for radius in range(60, 30, -5):
                draw.ellipse((650-radius, 50-radius, 750+radius, 150+radius), 
                           fill=(255, 255, min(255, 200 + radius)))
            draw.ellipse((650, 50, 750, 150), fill='yellow')
            for i in range(12):
                angle = i * 30
                x = 700 + 80 * (1 if i < 6 else -1)
                y = 100 + 80 * (1 if i < 6 else -1)
                draw.line((700, 100, x, y), fill='yellow', width=4)
        
        if 'cloud' in prompt:
            for x in [100, 300, 500]:
                for offset in [(0,0), (20,-10), (40,0), (20,10)]:
                    draw.ellipse((x+offset[0], 80+offset[1], x+offset[0]+40, 120+offset[1]), 
                               fill='white')
        
        if 'tree' in prompt:
            for x in range(100, 700, 200):
                for y in range(400, 500):
                    ratio = (y - 400) / 100
                    brown = (139, 69, 19)
                    dark_brown = (101, 67, 33)
                    r = int(brown[0] + (dark_brown[0] - brown[0]) * ratio)
                    g = int(brown[1] + (dark_brown[1] - brown[1]) * ratio)
                    b = int(brown[2] + (dark_brown[2] - brown[2]) * ratio)
                    draw.line([(x, y), (x + 20, y)], fill=(r, g, b))
                
                foliage_colors = [(34, 139, 34), (0, 100, 0), (0, 128, 0)]
                for i, color in enumerate(foliage_colors):
                    points = [
                        (x - 30 + i*10, 400 - i*20),
                        (x + 10, 300 - i*30),
                        (x + 50 - i*10, 400 - i*20)
                    ]
                    draw.polygon(points, fill=color)
        
        if 'river' in prompt:
            river_points = [(300, HEIGHT), (350, HEIGHT-100), (400, HEIGHT-150),
                          (450, HEIGHT-200), (500, HEIGHT-250), (550, HEIGHT-200),
                          (600, HEIGHT-150), (650, HEIGHT-100), (700, HEIGHT)]
            for i in range(len(river_points)-1):
                x1, y1 = river_points[i]
                x2, y2 = river_points[i+1]
                for width in range(40, 0, -5):
                    draw.line([(x1, y1), (x2, y2)], 
                             fill=(0, 0, min(255, 200 + width)), width=width)
        
        if 'cow' in prompt:
            x, y = 200, 450
            draw.ellipse((x, y, x+80, y+50), fill='white')
            draw.ellipse((x+70, y-10, x+100, y+20), fill='white')
            for leg_x in [x+20, x+60]:
                draw.rectangle((leg_x, y+50, leg_x+10, y+80), fill='black')
            for spot_x, spot_y in [(x+20, y+10), (x+50, y+20), (x+30, y+30)]:
                draw.ellipse((spot_x, spot_y, spot_x+20, spot_y+15), fill='black')
            draw.ellipse((x+85, y, x+90, y+5), fill='black')
            draw.polygon([(x+75, y-10), (x+85, y-20), (x+95, y-10)], fill='pink')

        if 'table' in prompt:
            x, y = 400, 400
            draw.rectangle((x, y, x+120, y+10), fill='brown')
            for leg_x in [x+20, x+100]:
                draw.rectangle((leg_x, y+10, leg_x+10, y+60), fill='brown')

        if 'computer' in prompt:
            x, y = 420, 380
            draw.rectangle((x, y, x+80, y+60), fill='gray')
            draw.rectangle((x+5, y+5, x+75, y+55), fill='black')
            draw.rectangle((x+35, y+60, x+45, y+80), fill='gray')
            draw.ellipse((x+20, y+80, x+60, y+90), fill='gray')

        if 'book' in prompt:
            x, y = 300, 450
            draw.rectangle((x, y, x+60, y+80), fill='red')
            draw.rectangle((x+5, y+5, x+55, y+75), fill='white')
            for i in range(5):
                draw.line((x+10, y+15+i*12, x+50, y+15+i*12), fill='black', width=1)

        if 'man' in prompt or 'person' in prompt:
            x, y = 500, 400
            draw.ellipse((x, y, x+30, y+30), fill='peachpuff')
            draw.rectangle((x+10, y+30, x+20, y+80), fill='blue')
            draw.line((x+10, y+40, x-10, y+60), fill='blue', width=5)
            draw.line((x+20, y+40, x+40, y+60), fill='blue', width=5)
            draw.line((x+10, y+80, x+5, y+100), fill='black', width=5)
            draw.line((x+20, y+80, x+25, y+100), fill='black', width=5)

        if 'woman' in prompt:
            x, y = 600, 400
            draw.ellipse((x, y, x+30, y+30), fill='peachpuff')
            draw.polygon([(x+5, y+30), (x+25, y+30), (x+30, y+80), (x, y+80)], fill='pink')
            draw.line((x+5, y+40, x-10, y+60), fill='pink', width=5)
            draw.line((x+25, y+40, x+40, y+60), fill='pink', width=5)
            draw.line((x+10, y+80, x+8, y+100), fill='black', width=5)
            draw.line((x+20, y+80, x+22, y+100), fill='black', width=5)
            draw.arc((x-5, y, x+35, y+20), 180, 0, fill='brown', width=5)

        if 'house' in prompt:
            x, y = 100, 300
            draw.rectangle((x, y, x+120, y+100), fill='beige')
            draw.polygon([(x-10, y), (x+60, y-50), (x+130, y)], fill='brown')
            draw.rectangle((x+40, y+50, x+80, y+100), fill='brown')
            draw.rectangle((x+15, y+30, x+35, y+50), fill='lightblue')
            draw.rectangle((x+85, y+30, x+105, y+50), fill='lightblue')

        if 'flower' in prompt:
            for x in range(100, 700, 100):
                draw.line((x, 450, x, 500), fill='green', width=3)
                for angle in range(0, 360, 60):
                    rad = angle * 3.14159 / 180
                    petal_x = x + 15 * (1 if angle < 180 else -1)
                    petal_y = 450 + 15 * (1 if angle < 90 or angle > 270 else -1)
                    draw.ellipse((petal_x-5, petal_y-5, petal_x+5, petal_y+5), fill='yellow')
                draw.ellipse((x-5, 445, x+5, 455), fill='orange')

        if 'bird' in prompt:
            for x in range(100, 700, 150):
                draw.arc((x, 100, x+30, 120), 0, 180, fill='black', width=2)
                draw.arc((x+10, 95, x+25, 110), 0, 180, fill='black', width=2)
                draw.arc((x+15, 95, x+30, 110), 0, 180, fill='black', width=2)

        if 'star' in prompt or 'stars' in prompt:
            for _ in range(20):
                x = random.randint(50, WIDTH-50)
                y = random.randint(50, HEIGHT//3)
                size = random.randint(2, 4)
                for angle in range(0, 360, 72):
                    rad = angle * 3.14159 / 180
                    end_x = x + size * 3 * (1 if angle < 180 else -1)
                    end_y = y + size * 3 * (1 if angle < 90 or angle > 270 else -1)
                    draw.line((x, y, end_x, end_y), fill='yellow', width=1)
                draw.ellipse((x-size, y-size, x+size, y+size), fill='yellow')

        if 'moon' in prompt:
            x, y = 100, 100
            draw.ellipse((x, y, x+60, y+60), fill='lightyellow')
            for crater_x, crater_y in [(x+20, y+20), (x+40, y+30), (x+30, y+45)]:
                draw.ellipse((crater_x, crater_y, crater_x+10, crater_y+10), fill='gray')

        if 'grass' in prompt:
            for x in range(0, WIDTH, 5):
                height = random.randint(10, 30)
                draw.line((x, HEIGHT, x, HEIGHT-height), fill='green', width=2)
                for blade in range(3):
                    angle = random.randint(-30, 30)
                    end_x = x + angle
                    end_y = HEIGHT - height + random.randint(-5, 5)
                    draw.line((x, HEIGHT-height, end_x, end_y), fill='lightgreen', width=1)

        if 'butterfly' in prompt:
            for x in range(200, 600, 150):
                y = random.randint(150, 250)
                for wing_x, wing_y in [(x-20, y-20), (x+20, y-20)]:
                    draw.ellipse((wing_x, wing_y, wing_x+40, wing_y+30), fill='purple')
                    draw.ellipse((wing_x+5, wing_y+5, wing_x+35, wing_y+25), fill='pink')
                draw.line((x, y, x, y+30), fill='black', width=2)
                draw.line((x, y, x-10, y-10), fill='black', width=1)
                draw.line((x, y, x+10, y-10), fill='black', width=1)

        if 'fence' in prompt:
            for x in range(0, WIDTH, 30):
                draw.rectangle((x, HEIGHT-100, x+5, HEIGHT-50), fill='brown')
                draw.rectangle((x, HEIGHT-90, x+30, HEIGHT-85), fill='brown')
                draw.rectangle((x, HEIGHT-70, x+30, HEIGHT-65), fill='brown')
                draw.rectangle((x, HEIGHT-50, x+30, HEIGHT-45), fill='brown')

        if 'path' in prompt:
            path_points = [(100, HEIGHT), (200, HEIGHT-50), (300, HEIGHT-100),
                          (400, HEIGHT-50), (500, HEIGHT-100), (600, HEIGHT-50),
                          (700, HEIGHT)]
            for i in range(len(path_points)-1):
                x1, y1 = path_points[i]
                x2, y2 = path_points[i+1]
                draw.line([(x1, y1), (x2, y2)], fill='sandybrown', width=40)
                draw.line([(x1, y1-20), (x2, y2-20)], fill='saddlebrown', width=2)
                draw.line([(x1, y1+20), (x2, y2+20)], fill='saddlebrown', width=2)

        if 'bench' in prompt:
            x, y = 300, 450
            draw.rectangle((x, y, x+120, y+10), fill='brown')
            draw.rectangle((x, y-40, x+120, y-35), fill='brown')
            for leg_x in [x+20, x+100]:
                draw.rectangle((leg_x, y+10, leg_x+10, y+40), fill='brown')

        safe_prompt = re.sub(r'[^a-z0-9]', '_', prompt)[:30]
        filename = f'{safe_prompt}.png'
        filepath = os.path.join(IMAGE_FOLDER, filename)
        
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

@app.route('/static/generated_images/<path:filename>')
def static_files(filename):
    return send_from_directory(IMAGE_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
