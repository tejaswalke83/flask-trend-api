from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Flask service is running."

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    products = data.get("products", [])
    return jsonify({
        "message": "Received products",
        "count": len(products),
        "products": products
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
