from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from PIL import Image
from io import BytesIO
import os
import base64
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# API Configuration
NANO_GPT_API_KEY = os.getenv('NANO_GPT_API_KEY')
NANO_GPT_API_URL = "https://nano-gpt.com/v1/images/generations"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Check if API key is configured
        if not NANO_GPT_API_KEY:
            return jsonify({'error': 'API 키가 설정되지 않았습니다. .env 파일에 NANO_GPT_API_KEY를 추가해주세요.'}), 500

        # Get text prompt
        prompt = request.form.get('prompt')
        if not prompt:
            return jsonify({'error': '텍스트 프롬프트를 입력해주세요.'}), 400

        # Get uploaded images for image-to-image generation
        image_data_urls = []
        if 'images' in request.files:
            files = request.files.getlist('images')
            for file in files:
                if file and allowed_file(file.filename):
                    # Open and process image
                    img = Image.open(file.stream)
                    # Convert to RGB if necessary
                    if img.mode not in ('RGB', 'RGBA'):
                        img = img.convert('RGB')

                    # Convert to base64 data URL
                    buffered = BytesIO()
                    img.save(buffered, format='PNG')
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    image_data_url = f"data:image/png;base64,{img_str}"
                    image_data_urls.append(image_data_url)

        # Prepare API request
        headers = {
            'Authorization': f'Bearer {NANO_GPT_API_KEY}',
            'Content-Type': 'application/json'
        }

        # Build request payload
        payload = {
            'model': 'hidream',  # You can change this to other models
            'prompt': prompt,
            'n': 1,
            'size': '1024x1024',
            'response_format': 'b64_json'
        }

        # Add image data if available (for image-to-image)
        if image_data_urls:
            if len(image_data_urls) == 1:
                payload['imageDataUrl'] = image_data_urls[0]
            else:
                payload['imageDataUrls'] = image_data_urls

        # Call Nano-GPT API
        response = requests.post(NANO_GPT_API_URL, headers=headers, json=payload)

        if response.status_code == 200:
            result = response.json()

            # Extract base64 image from response
            if 'data' in result and len(result['data']) > 0:
                b64_json = result['data'][0].get('b64_json')

                if b64_json:
                    # Decode base64 to image
                    img_data = base64.b64decode(b64_json)

                    # Save image
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    output_filename = f'generated_{timestamp}.png'
                    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

                    with open(output_path, 'wb') as f:
                        f.write(img_data)

                    # Get cost information if available
                    cost_info = ""
                    if 'cost' in result:
                        cost_info = f" (비용: {result['cost']})"

                    return jsonify({
                        'success': True,
                        'message': f'이미지가 성공적으로 생성되었습니다!{cost_info}',
                        'filename': output_filename,
                        'prompt_response': f'Nano-GPT API를 사용하여 이미지를 생성했습니다.'
                    })

            return jsonify({'error': '이미지 생성 응답을 처리할 수 없습니다.'}), 500

        else:
            error_msg = response.json().get('error', '알 수 없는 오류') if response.text else f'HTTP {response.status_code}'
            return jsonify({'error': f'API 오류: {error_msg}'}), 500

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': f'오류가 발생했습니다: {str(e)}'}), 500

@app.route('/download/<filename>')
def download(filename):
    try:
        filepath = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        return send_file(filepath, as_attachment=True, download_name=filename)
    except Exception as e:
        return jsonify({'error': f'파일을 찾을 수 없습니다: {str(e)}'}), 404

@app.route('/output/<filename>')
def serve_output(filename):
    try:
        return send_file(os.path.join(app.config['OUTPUT_FOLDER'], filename))
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