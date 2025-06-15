from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Flask service is running"

@app.route('/analyze', methods=['POST'])
def analyze_products():
    try:
        data = request.get_json()

        # ✅ Handle list wrapper from n8n
        if isinstance(data, list) and len(data) > 0:
            data = data[0]

        # Extract product list from JSON
        products = data.get("products", [])
        original_input = data.get("original_input", "")

        # Prepare response
        response = {
            "count": len(products),
            "message": "Received products",
            "products": products
        }

        return jsonify([response])

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
