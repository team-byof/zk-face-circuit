import numpy as np
from deepface import DeepFace


class FaceComparison:

    @staticmethod
    def verify_faces(img1_path, img2_path):
        """Verify if two faces are the same"""
        result = DeepFace.verify(img1_path, img2_path)
        return result

    @staticmethod
    def represent_face(img_path):
        """Get the face embeddings for the image at img_path"""
        embedding = DeepFace.represent(img_path)
        return embedding

    @staticmethod
    def calculate_distance(embedding1, embedding2):
        """Calculate Euclidean distance between two embeddings"""
        a = np.array(embedding1)
        b = np.array(embedding2)
        dist = np.linalg.norm(a - b)
        return dist

    @staticmethod
    def calculate_cosine_similarity(embedding1, embedding2):
        """Calculate Cosine similarity between two embeddings"""
        a = np.array(embedding1)
        b = np.array(embedding2)
        cos_sim = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
        return 1 - cos_sim

#
# # Usage:
# face_comparator = FaceComparison()
#
# img1_path = "./dataset/img1.jpg"
# img1_path_2 = "./dataset/img1.jpg"
# img2_path = "./dataset/img2.jpg"
#
# # Verify faces
# result = face_comparator.verify_faces(img1_path, img1_path_2)
# print(result)
#
# # Get face embeddings
# embedding_img1 = face_comparator.represent_face(img1_path)
# embedding_img2 = face_comparator.represent_face(img1_path_2)
#
# print(embedding_img1)
# print(embedding_img2)
#
# # Calculate distance and cosine similarity between embeddings
# dist = face_comparator.calculate_distance(embedding_img1, embedding_img2)
# cos_sim = face_comparator.calculate_cosine_similarity(embedding_img1, embedding_img2)
#
# print(dist)
# print(cos_sim)
