from flask import Flask, jsonify, request
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mock database for demonstration
user_profiles = {
    "user1": {"name": "John Doe", "email": "john@example.com", "role": "user"},
    "user2": {"name": "Jane Smith", "email": "jane@example.com", "role": "admin"}
}

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/api/profiles', methods=['GET'])
def get_profiles():
    logger.info("Retrieving all profiles")
    return jsonify(list(user_profiles.values())), 200

@app.route('/api/profiles/<user_id>', methods=['GET'])
def get_profile(user_id):
    logger.info(f"Retrieving profile for user {user_id}")
    if user_id in user_profiles:
        return jsonify(user_profiles[user_id]), 200
    return jsonify({"error": "User not found"}), 404

@app.route('/api/profiles/<user_id>', methods=['PUT'])
def update_profile(user_id):
    logger.info(f"Updating profile for user {user_id}")
    if user_id in user_profiles:
        data = request.json
        user_profiles[user_id].update(data)
        return jsonify(user_profiles[user_id]), 200
    return jsonify({"error": "User not found"}), 404

@app.route('/api/profiles', methods=['POST'])
def create_profile():
    data = request.json
    user_id = data.get('user_id')
    logger.info(f"Creating profile for user {user_id}")
    
    if user_id in user_profiles:
        return jsonify({"error": "User already exists"}), 409
        
    user_profiles[user_id] = {
        "name": data.get('name', ''),
        "email": data.get('email', ''),
        "role": data.get('role', 'user')
    }
    return jsonify(user_profiles[user_id]), 201

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)