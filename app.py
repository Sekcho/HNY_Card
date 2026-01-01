"""
Flask application for New Year Card Generator
"""
from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
import os
import json
from werkzeug.utils import secure_filename
from utils.card_generator import CardGenerator
from config import THEMES, FONTS, FONT_SIZES, DEFAULT_SETTINGS
import shutil

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
app.config['TEMPLATES_FILE'] = os.path.join(os.path.dirname(__file__), 'data', 'templates.json')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Initialize card generator
base_dir = os.path.dirname(__file__)
card_gen = CardGenerator(base_dir)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Main page with form"""
    return render_template('index.html',
                         themes=THEMES,
                         fonts=FONTS,
                         font_sizes=FONT_SIZES,
                         default_settings=DEFAULT_SETTINGS)


@app.route('/upload-photo', methods=['POST'])
def upload_photo():
    """Handle photo upload"""
    if 'photo' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['photo']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Allowed: PNG, JPG, JPEG, GIF, WEBP'}), 400

    # Save file
    filename = secure_filename(file.filename)
    # Add timestamp to avoid conflicts
    import time
    timestamp = str(int(time.time()))
    name, ext = os.path.splitext(filename)
    filename = f"{name}_{timestamp}{ext}"

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Return relative path for use in template
    relative_path = f"../static/uploads/{filename}"

    return jsonify({
        'success': True,
        'filepath': relative_path,
        'filename': filename
    })


@app.route('/generate-card', methods=['POST'])
def generate_card():
    """Generate the card (HTML + JPG)"""
    data = request.json

    try:
        # Prepare data for generator
        card_data = {
            'year_cs': int(data.get('year_cs', 2026)),
            'year_be': int(data.get('year_be', 2569)),
            'wishes': data.get('wishes', []),
            'signature': data.get('signature', ''),
            'photo_path': data.get('photo_path', ''),
            'theme': data.get('theme', 'blue-gold'),
            'thai_font': data.get('thai_font', 'noto-sans-thai'),
            'english_font': data.get('english_font', 'poppins'),
            'font_sizes': data.get('font_sizes', {})
        }

        # Generate card
        html_path, jpg_path = card_gen.generate_card(card_data)

        # Get filenames for download
        html_filename = os.path.basename(html_path)
        jpg_filename = os.path.basename(jpg_path)

        return jsonify({
            'success': True,
            'html_file': html_filename,
            'jpg_file': jpg_filename,
            'message': 'Card generated successfully!'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/download/<filename>')
def download_file(filename):
    """Download generated files"""
    directory = os.path.join(base_dir, 'static', 'generated')
    return send_from_directory(directory, filename, as_attachment=True)


@app.route('/save-template', methods=['POST'])
def save_template():
    """Save template settings"""
    data = request.json
    template_name = data.get('template_name', '')

    if not template_name:
        return jsonify({'error': 'Template name is required'}), 400

    # Load existing templates
    templates = {}
    if os.path.exists(app.config['TEMPLATES_FILE']):
        with open(app.config['TEMPLATES_FILE'], 'r', encoding='utf-8') as f:
            templates = json.load(f)

    # Save template (without photo)
    template_data = {
        'year_cs': data.get('year_cs'),
        'year_be': data.get('year_be'),
        'wishes': data.get('wishes'),
        'signature': data.get('signature'),
        'theme': data.get('theme'),
        'thai_font': data.get('thai_font'),
        'english_font': data.get('english_font'),
        'font_sizes': data.get('font_sizes')
    }

    templates[template_name] = template_data

    # Save to file
    os.makedirs(os.path.dirname(app.config['TEMPLATES_FILE']), exist_ok=True)
    with open(app.config['TEMPLATES_FILE'], 'w', encoding='utf-8') as f:
        json.dump(templates, f, ensure_ascii=False, indent=2)

    return jsonify({
        'success': True,
        'message': f'Template "{template_name}" saved successfully!'
    })


@app.route('/load-templates', methods=['GET'])
def load_templates():
    """Load saved templates"""
    if not os.path.exists(app.config['TEMPLATES_FILE']):
        return jsonify({'templates': {}})

    with open(app.config['TEMPLATES_FILE'], 'r', encoding='utf-8') as f:
        templates = json.load(f)

    return jsonify({'templates': templates})


@app.route('/delete-template', methods=['POST'])
def delete_template():
    """Delete a saved template"""
    data = request.json
    template_name = data.get('template_name', '')

    if not template_name:
        return jsonify({'error': 'Template name is required'}), 400

    if not os.path.exists(app.config['TEMPLATES_FILE']):
        return jsonify({'error': 'No templates found'}), 404

    # Load existing templates
    with open(app.config['TEMPLATES_FILE'], 'r', encoding='utf-8') as f:
        templates = json.load(f)

    # Delete template
    if template_name in templates:
        del templates[template_name]

        # Save updated templates
        with open(app.config['TEMPLATES_FILE'], 'w', encoding='utf-8') as f:
            json.dump(templates, f, ensure_ascii=False, indent=2)

        return jsonify({
            'success': True,
            'message': f'Template "{template_name}" deleted successfully!'
        })
    else:
        return jsonify({'error': 'Template not found'}), 404


@app.route('/get-theme-info/<theme_key>')
def get_theme_info(theme_key):
    """Get theme information"""
    if theme_key in THEMES:
        return jsonify(THEMES[theme_key])
    return jsonify({'error': 'Theme not found'}), 404


if __name__ == '__main__':
    # Create necessary directories
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(base_dir, 'static', 'generated'), exist_ok=True)
    os.makedirs(os.path.join(base_dir, 'data'), exist_ok=True)

    app.run(debug=True, host='0.0.0.0', port=5000)
