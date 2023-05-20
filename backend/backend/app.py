from flask import Flask, jsonify, request
from flask_cors import CORS
from ml_model import FaceComparison

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
face_comparator = FaceComparison()


@app.route('/api/data')
def get_data():
    data = {'name': 'dannaward', 'age': 23}
    return jsonify(data)


@app.route('/api/upload-image', methods=['POST'])
def upload():
    return {'message': 'File uploaded successfully'}


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


@app.route('/feat_vec', methods=['POST'])
def feat_vec():
    img_path = request.json.get('img_path')
    result = FaceComparison.feat_vec(img_path)
    return jsonify(result)


@app.route('/gen_proof', methods=['POST'])
def gen_proof():
    img_path = request.json.get('img_path')
    json_data = request.json.get('json_data')
    result = FaceComparison.gen_proof(img_path, json_data)
    return jsonify(result)


if __name__ == '__main__':
    app.run()
