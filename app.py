from flask import Flask, render_template, request
import requests
import io
from PIL import Image
import base64

app = Flask(__name__)

# API configuration
API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"
headers = {"Authorization": "Bearer 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"}

def query(prompt):
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    return response.content

# Home route for intro
@app.route('/')
def home():
    return render_template('index.html')

# Chatbot route for generating images
@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    image_data = None
    if request.method == 'POST':
        prompt = request.form.get('prompt')
        image_bytes = query(prompt)
        
        # Convert the image to base64 to display on the page
        image = Image.open(io.BytesIO(image_bytes))
        img_io = io.BytesIO()
        image.save(img_io, 'PNG')
        img_io.seek(0)
        img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')

        image_data = f"data:image/png;base64,{img_base64}"

    return render_template('chatbot.html', image_data=image_data)

if __name__ == "__main__":
    app.run(debug=True)
