from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/analyze", methods=["POST"])
def analyze_products():
    try:
        data = request.get_json()

        # In case data is a list (which it is)
        if isinstance(data, list):
            data = data[0]

        products = data.get("products", [])
        original_input = data.get("original_input", "")

        return jsonify([{
            "count": len(products),
            "message": "Received products",
            "products": products
        }])

    except Exception as e:
        return jsonify({"error": str(e)}), 500
