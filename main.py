from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return "Flask service is running"

@app.route('/analyze', methods=['POST'])
def analyze_products():
    try:
        data = request.get_json(force=True, silent=True)

        if not data:
            return jsonify({"count": 0, "message": "No JSON received", "products": []})

        if isinstance(data, list):
            input_data = data[0]
        else:
            input_data = data

        raw_input = input_data.get("original_input", "")
        
        # Normalize input: split by comma or newline
        raw_products = [item.strip() for item in raw_input.replace('\n', ',').split(',') if item.strip()]

        return jsonify({
            "count": len(raw_products),
            "message": "Received products",
            "products": raw_products
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
