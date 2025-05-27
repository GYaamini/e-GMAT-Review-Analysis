from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
import dashboard
from summarise_analyse import process_reviews, process_gathering

load_dotenv()

# Flash app initialization
flask_app = Flask(__name__)

# Dash app initialization
dash_app = dashboard.create_dash(flask_app)

# Comment this out for production
CORS(flask_app)

#API routes
@flask_app.route('/api/gather', methods=['POST'])
def gather():
    data = request.json
    type = data.get('type')
    
    try:
        combined_text = process_gathering(type)
        return jsonify({
            "text": combined_text,
            "status": "success"
        })
    except Exception as e:
        return jsonify({"error": str(e), "status": "failed"}), 500

@flask_app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.json
    analysis_type = data.get('type')
    
    try:
        analysis = process_reviews(analysis_type)
        return jsonify({
            "analysis": analysis,
            "status": "success"
        })
    except Exception as e:
        return jsonify({"error": str(e), "status": "failed"}), 500


if __name__ == "__main__":
    flask_app.run(debug=True, port=5000)
