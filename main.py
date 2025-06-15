from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import openai

app = Flask(__name__)
CORS(app)

# Load OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return 'Flask service is running'

@app.route('/analyze', methods=['POST'])
def analyze_products():
    data = request.get_json()

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

    # Call OpenAI for product trend analysis
    try:
        prompt = f"Analyze the following products for market trends, categories, and popularity:\n\n{products}"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a market research assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200
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
