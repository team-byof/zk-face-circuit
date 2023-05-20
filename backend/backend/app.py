from flask import Flask, jsonify, request
from flask_cors import CORS
from ml_model import FaceComparison

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
face_comparator = FaceComparison()

@app.route('/api/data')
def get_data():
    data = {'name': 'John', 'age': 30}
    return jsonify(data)


@app.route('/api/upload-wav', methods=['POST'])
def upload():
    return {'message': 'File uploaded successfully'}


@app.route('/api/feature-vector', methods=['POST'])
def feat_vec():
    mock_response = {
        "feat": "mock_feat",
        "hash_ecc": "mock_hash_ecc",
        "hash_feat_xor_ecc": "mock_hash_feat_xor_ecc",
        "feat_xor_ecc": "mock_feat_xor_ecc",
    }

    return jsonify(mock_response)


@app.route('/api/gen-proof', methods=['POST'])
def gen_proof():
    mock_response = {
        "new_feat": "mock_new_feat",
        "recovered_hash_ecc": "mock_recovered_hash_ecc",
        "hash_ecc_msg": "mock_hash_ecc_msg",
        "code_error": "mock_code_error",
        "proof": "mock_proof",
        "session_id": "mock_session_id",
    }

    return jsonify(mock_response)

# curl -X POST http://127.0.0.1:5000/api/compare-faces -H "Content-Type: application/json" -d '{"img1_path": "/Users/sigridjin.eth/Documents/github/zk-face-circuit/backend/backend/dataset/img1.jpg", "img2_path": "/Users/sigridjin.eth/Documents/github/zk-face-circuit/backend/backend/dataset/img1.jpg"}'
# {"cosine_similarity":2.220446049250313e-16,"distance":0.0,"verification_result":{"distance":2.220446049250313e-16,"max_threshold_to_verify":0.4,"model":"VGG-Face","similarity_metric":"cosine","verified":true}}
@app.route('/api/compare-faces', methods=['POST'])
def compare_faces():
    if request.method == 'POST':
        data = request.get_json()
        img1_path = data.get('img1_path')
        img2_path = data.get('img2_path')

        if not img1_path or not img2_path:
            return jsonify({"error": "img1_path or img2_path not provided"}), 400

        # Verify faces
        result = face_comparator.verify_faces(img1_path, img2_path)

        # Get face embeddings
        embedding_img1 = face_comparator.represent_face(img1_path)
        embedding_img2 = face_comparator.represent_face(img2_path)

        # Calculate distance and cosine similarity between embeddings
        dist = face_comparator.calculate_distance(embedding_img1, embedding_img2)
        cos_sim = face_comparator.calculate_cosine_similarity(embedding_img1, embedding_img2)

        response = {
            "verification_result": result,
            "distance": dist,
            "cosine_similarity": cos_sim
        }

        return jsonify(response)


if __name__ == '__main__':
    app.run()
