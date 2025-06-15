from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return 'Flask service is running.'

@app.route('/analyze', methods=['POST'])
def analyze_product():
    data = request.get_json()
    product = data.get('product', '').lower()

    if not product:
        return jsonify({"error": "No product provided"}), 400

    # Simulated logic – later we’ll connect to Google Trends / Apify
    mock_response = {
        "product": product,
        "trend": "rising",
        "suggestion": f"Try eco-friendly {product}s",
        "category": "Apparel" if "shirt" in product or "jeans" in product else "General"
    }

    return jsonify(mock_response)
