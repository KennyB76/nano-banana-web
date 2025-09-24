from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import google.generativeai as genai
from PIL import Image
from io import BytesIO
import os
import base64
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Configure Gemini API
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash-exp')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Get text prompt
        prompt = request.form.get('prompt')
        if not prompt:
            return jsonify({'error': '텍스트 프롬프트를 입력해주세요.'}), 400

        # Get uploaded images
        images = []
        if 'images' in request.files:
            files = request.files.getlist('images')
            for file in files:
                if file and allowed_file(file.filename):
                    # Open and process image
                    img = Image.open(file.stream)
                    # Convert to RGB if necessary
                    if img.mode not in ('RGB', 'RGBA'):
                        img = img.convert('RGB')
                    images.append(img)

        # Prepare content for Gemini API
        content_parts = []

        # Add images to content
        for img in images:
            # Convert PIL image to bytes
            img_byte_arr = BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            content_parts.append(img)

        # Add text prompt
        final_prompt = f"""Based on the provided images (if any), {prompt}

        Generate a new image following these instructions.
        If no images are provided, create an image based solely on the text description."""

        content_parts.append(final_prompt)

        # Generate content using Gemini
        response = model.generate_content(content_parts)

        # For text-to-image, we'll use a different approach
        # Since Gemini 2.0 Flash doesn't generate images directly,
        # we'll create a placeholder response for now

        # Save a placeholder or process the response
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = f'generated_{timestamp}.png'
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

        # For demonstration, save the first uploaded image or create a placeholder
        if images:
            images[0].save(output_path)
            success_message = "이미지가 처리되었습니다. (데모: 첫 번째 이미지 저장)"
        else:
            # Create a placeholder image
            placeholder = Image.new('RGB', (512, 512), color='#FFD548')
            placeholder.save(output_path)
            success_message = "플레이스홀더 이미지가 생성되었습니다."

        return jsonify({
            'success': True,
            'message': success_message,
            'filename': output_filename,
            'prompt_response': response.text if response.text else "이미지 생성 프롬프트 처리 완료"
        })

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': f'오류가 발생했습니다: {str(e)}'}), 500

@app.route('/download/<filename>')
def download(filename):
    try:
        filepath = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        return jsonify({'error': f'파일을 찾을 수 없습니다: {str(e)}'}), 404

@app.route('/result')
def result():
    filename = request.args.get('filename')
    return render_template('result.html', filename=filename)

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

    app.run(debug=True, port=5000)