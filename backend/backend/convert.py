import numpy as np
from deepface import DeepFace


def bytearray_to_hex(ba):
    return '0x' + ''.join(format(x, '02x') for x in ba)


def hex_to_bytearray(hex_string):
    return bytearray.fromhex(hex_string[2:])


def feat_bytearray_from_image_path(img_path):
    # Get the embeddings for the image
    embedding = DeepFace.represent(img_path)

    # Ensure embedding is an array of integers (DeepFace.represent returns a list of floats)
    int_embedding = [int(e) for e in embedding]

    # Convert to a byte array
    feat_bytearray = bytearray(np.packbits(int_embedding))

    return feat_bytearray
