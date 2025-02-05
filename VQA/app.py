from flask import Flask, render_template, request, jsonify
import os
from PIL import Image
import google.generativeai as genai

app = Flask(__name__)

# Set your API key
os.environ['GOOGLE_API_KEY'] = "AIzaSyD5LzD14to-tQWALMfya2E_I5OvT08qiaU"
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze_image', methods=['POST'])
def analyze_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    image = request.files['image']
    question = request.form.get('question', '')  # Get the user-provided question
    image_path = 'uploads/' + image.filename
    image.save(image_path)

    description = image_analysis_request(image_path, question)  # Pass the question to image_analysis_request
    return jsonify({'description': description})

def image_analysis_request(image_path, question):
    image = Image.open(image_path)
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([question, image])  # Include the user-provided question in the content
    return response.text

if __name__ == '__main__':
    app.run(debug=True)
