from flask import Flask, render_template, request, jsonify, send_from_directory
from image_generator.generator import ImageGenerator
import os
from datetime import datetime
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/generated'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize image generator
generator = ImageGenerator()

# Gallery data file
GALLERY_DATA_FILE = 'gallery_data.json'

def load_gallery_data():
    if os.path.exists(GALLERY_DATA_FILE):
        with open(GALLERY_DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_gallery_data(data):
    with open(GALLERY_DATA_FILE, 'w') as f:
        json.dump(data, f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate_image():
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        # Get generation parameters
        width = int(data.get('width', 800))
        height = int(data.get('height', 600))
        quality = data.get('quality', 'medium')
        output_format = data.get('format', 'PNG')
        
        # Generate image
        image_path = generator.generate(
            prompt=prompt,
            width=width,
            height=height,
            quality=quality,
            output_format=output_format
        )
        
        # Save to gallery
        gallery_data = load_gallery_data()
        gallery_data.append({
            'url': f'/static/generated/{os.path.basename(image_path)}',
            'prompt': prompt,
            'timestamp': datetime.now().isoformat()
        })
        save_gallery_data(gallery_data)
        
        return jsonify({
            'imageUrl': f'/static/generated/{os.path.basename(image_path)}',
            'prompt': prompt
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/gallery')
def get_gallery():
    try:
        gallery_data = load_gallery_data()
        return jsonify(gallery_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/static/generated/<filename>')
def serve_generated_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
