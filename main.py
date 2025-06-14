
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['POST'])
def handle_request():
    data = request.json
    products = data.get('products', [])
    if not products:
        return jsonify({"error": "No products received"}), 400

    return jsonify({
        "status": "success",
        "received_products": products
    })

@app.route('/', methods=['GET'])
def home():
    return "Flask service is running."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
