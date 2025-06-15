@app.route('/analyze', methods=['POST'])
def analyze_products():
    try:
        data = request.get_json()

        # 🧪 Debug log to print raw received data
        print("📦 Raw JSON received:", data)

        # Handle n8n wrapper (list of one object)
        if isinstance(data, list) and len(data) > 0:
            data = data[0]

        # Try to extract products
        products = data.get("products") or []

        # Prepare and return the response
        response = {
            "count": len(products),
            "message": "Received products",
            "products": products
        }

        return jsonify([response])

    except Exception as e:
        return jsonify({"error": str(e)}), 500
