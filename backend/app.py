from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pickle
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)  # Enable CORS for frontend requests

# Load the model and vectorizer
model_path = 'model/model.pkl'
vectorizer_path = 'model/vectorizer.pkl'

model = None
vectorizer = None

try:
    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    with open(vectorizer_path, 'rb') as f:
        vectorizer = pickle.load(f)
    print("Model and vectorizer loaded successfully")
except FileNotFoundError:
    print("Model files not found. Please run train.py first.")

@app.route('/predict', methods=['POST'])
def predict():
    if model is None or vectorizer is None:
        return jsonify({'error': 'Model not loaded. Please train the model first.'}), 500

    try:
        data = request.get_json()
        text = data.get('text', '')

        if not text:
            return jsonify({'error': 'No text provided'}), 400

        # Vectorize the input text
        text_vec = vectorizer.transform([text])

        # Make prediction
        prediction = model.predict(text_vec)[0]

        return jsonify({'sentiment': int(prediction)})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('../frontend', path)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)