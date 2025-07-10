from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Allow React frontend to access this backend

@app.route('/chat', methods=['POST'])
def chat():
    prompt = request.json.get('prompt')
    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400

    try:
        # Use Ollama HTTP API instead of subprocess
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': 'phi',
                'prompt': prompt,
                'stream': False
            }
        )
        data = response.json()
        return jsonify({'response': data.get('response', '⚠️ No reply from model')})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
