from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# Initialize OpenAI client using environment variable from Railway
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/')
def home():
    return 'Flask service is running'

@app.route('/analyze', methods=['POST'])
def analyze_products():
    data = request.get_json()

    # Fix: Ensure data is a dict
    if not isinstance(data, dict):
        return jsonify({
            "count": 0,
            "message": "Invalid JSON format. Expected an object with a 'products' key.",
            "products": [],
            "analysis": ""
        })

    original_input = data.get("products", "")
    if not original_input:
        return jsonify({
            "count": 0,
            "message": "No input received",
            "products": [],
            "analysis": ""
        })

    # Clean and split product list
    if isinstance(original_input, str):
        products = [item.strip() for item in original_input.replace("\n", ",").split(",") if item.strip()]
    elif isinstance(original_input, list):
        products = [str(item).strip() for item in original_input]
    else:
        products = []

    # Generate prompt for GPT
    prompt = f"Analyze the following products for market trends, categories, and popularity:\n\n{products}"

    # Call OpenAI GPT-4 API
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a market research assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300
        )
        analysis = response.choices[0].message.content.strip()
    except Exception as e:
        analysis = f"Error generating analysis: {str(e)}"

    return jsonify({
        "count": len(products),
        "message": "Received products",
        "products": products,
        "analysis": analysis
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
