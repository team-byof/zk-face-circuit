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

# curl -X POST -H "Content-Type: application/json" -d '{"img_path":"/Users/sigridjin.eth/Documents/github/zk-face-circuit/backend/backend/dataset/img2.jpg"}' http://127.0.0.1:5000/feat_vec
# {"feat":"0xf3fffffffff7fffefffffffffdfffdfffdfffbfffffffffffffffffffffffffffffdfffbfffffffffffffffffdfdfffffffffffffdffbffdfffffffffbfffffbfffffffffffffef3fffffffddfeffffffffffffffefefffffffffdffffffffffffffffffffffffffff7ffbfffffdffbffffff7fffffffffdffffffefbffbfffbfffffffff7ffffffff7fdbffff7f7f7ffff7fdffcffffeffbbfffffffffdfffffbdbfffffeffffeffffffdfffffffffeefff7f7afffffffffdffefffffbfffb6bfefffffdfbffff7ffff7fffffffffffffdfffbfbff77ffdfffffdfdefdffffffffffffffffdefbb7fffffffffffbfff7fffffffe7ffefffffffffbbffffbfffbfeefffffdfffdfffdffdf7f7fbfdfdbffffffffdfffffffdffff7f6fffffffffffffffffefffbfefbffffffddff6efffffffbf5fff7ffffffffff7f7fffffffff7feffffffffff4","feat_xor_ecc":"0x682421a9e30233297ea476c3f57d3232d507471a0f0dbd68968c0229c0666da9e0d0e1f5f23ce70f4ec30b147e6cd376cc4a1347d1933e5f7187c1da10fd462b2f3515394e6c204d61d7d2be0464083715f4ed8ea8690fe85c398620125759d0467b3910745a870885d5c6c7b157253d8edb271d66a2c8950eb6b3a6bd8f42a2980758d350f4c171","hash_ecc":"0x153fefa1b2fedc97c0da59176e6df7379adc618aaea37afb1007a0cb979df98f","hash_feat_xor_ecc":"0x0dd91b3adb2d4558edab7429b2a3694c39c89603c9d7c7f57832da519194ad57"}
@app.route('/feat_vec', methods=['POST'])
def feat_vec():
    img_path = request.json.get('img_path')
    result = FaceComparison.feat_vec(img_path)
    return jsonify(result)

# curl -X POST -H "Content-Type: application/json" -d '{"img_path":"/Users/sigridjin.eth/Documents/github/zk-face-circuit/backend/backend/dataset/img1.jpg", "json_data": { "hash_ecc":"0x153fefa1b2fedc97c0da59176e6df7379adc618aaea37afb1007a0cb979df98f", "feat_xor_ecc":"0x682421a9e30233297ea476c3f57d3232d507471a0f0dbd68968c0229c0666da9e0d0e1f5f23ce70f4ec30b147e6cd376cc4a1347d1933e5f7187c1da10fd462b2f3515394e6c204d61d7d2be0464083715f4ed8ea8690fe85c398620125759d0467b3910745a870885d5c6c7b157253d8edb271d66a2c8950eb6b3a6bd8f42a2980758d350f4c171", "msg":"0x12345678" }}' http://127.0.0.1:5000/gen_proof
@app.route('/gen_proof', methods=['POST'])
def gen_proof():
    """
    Request Type
    {
        "hash_ecc" : hex,
        "feat_xor_ecc": hex,
        "msg": hex,
    }
    """
    img_path = request.json.get('img_path')
    json_data = request.json.get('json_data')
    result = FaceComparison.gen_proof(img_path, json_data)
    return jsonify(result)


if __name__ == '__main__':
    app.run()
