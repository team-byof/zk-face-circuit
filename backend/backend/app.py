from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


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


if __name__ == '__main__':
    app.run()
