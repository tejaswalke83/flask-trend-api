from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load .env file if available (optional, helpful during local dev)
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize OpenAI client with your API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set in environment variables")
client = OpenAI(api_key=api_key)

@app.route('/')
def home():
    return 'Flask service is running'

@app.route('/analyze', methods=['POST'])
def analyze_products():
    try:
        data = request.get_json(force=True)

        if isinstance(data, dict):
            original_input = data.get("products", [])
        else:
            return jsonify({
                "count": 0,
                "message": "Invalid input format. Expected JSON with a 'products' key.",
                "products": [],
                "analysis": ""
            })

        # Clean and validate input
        if isinstance(original_input, str):
            products = [item.strip() for item in original_input.replace("\n", ",").split(",") if item.strip()]
        elif isinstance(original_input, list):
            products = [str(item).strip() for item in original_input if str(item).strip()]
        else:
            products = []

        if not products:
            return jsonify({
                "count": 0,
                "message": "No products provided.",
                "products": [],
                "analysis": ""
            })

        # Prompt
        prompt = f"Analyze the following products for market trends, categories, and popularity:\n\n{products}"

        # GPT call
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a market research assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300
        )
        analysis = response.choices[0].message.content.strip()

        return jsonify({
            "count": len(products),
            "message": "Received products",
            "products": products,
            "analysis": analysis
        })

    except Exception as e:
        return jsonify({
            "count": 0,
            "message": f"Server error: {str(e)}",
            "products": [],
            "analysis": ""
        })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
