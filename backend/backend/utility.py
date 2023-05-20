import bchlib
import os
import random
import string
import json

from bridge import poseidon_hash, evm_prove

from convert import bytearray_to_hex, hex_to_bytearray

# BCH 오브젝트를 생성합니다.
BCH_POLYNOMIAL = 8219
BCH_BITS = 64
bch = bchlib.BCH(BCH_POLYNOMIAL, BCH_BITS)
CODE_LEN = 140


def generate_filename(length):
    letters = string.ascii_lowercase
    filename = ''.join(random.choice(letters) for i in range(length))
    return filename


def bch_error_correction(packet):
    """
    BCH 코드에 의한 오류 수정

    Parameters
    ----------
    packet : bytearray
    256비트의 데이터를 BCH에 의해 인코딩 한 것. 256 비트보다 크다.
    """

    # de-packetize
    data, ecc = packet[:-bch.ecc_bytes], packet[-bch.ecc_bytes:]

    # correct
    bitflips = bch.decode_inplace(data, ecc)

    # packetize
    packet = data + ecc

    return packet


def bitflip(packet):
    byte_num = random.randint(0, len(packet) - 1)
    bit_num = random.randint(0, 7)
    packet[byte_num] ^= (1 << bit_num)


def test_bch():
    data = bytearray(os.urandom(32))

    ecc = bch.encode(data)
    packet = data + ecc
    print(type(packet))

    assert packet == bch_error_correction(packet)


def xor(a, b):
    """
    배타적 논리합을 취합니다.

    Parameters
    ----------
    a : bytearray
    b : bytearray
    """
    result = bytearray([x ^ y for x, y in zip(a, b)])
    return result


def my_hash(data):
    """
    Poseidon 해시 함수를 취합니다.

    Parameters
    ----------
    data : bytearray
    """
    return hex_to_bytearray(poseidon_hash(bytearray_to_hex(data)))


def padding(data, n):
    """
    256비트가 되도록 0을 추가합니다.

    Parameters
    ----------
    data : bytearray
    n : バイト数
    """
    padding_data = data.ljust(n, b'\x00')
    return padding_data


def fuzzy_commitment(feat_vec):
    """
    특징 벡터에서 h(w)와 c를 생성합니다.

    Parameters
    ----------
    feat_vec : bytearray
    """

    # 랜덤 벡터를 만든다.
    s = bytearray(os.urandom(32))

    ecc = bch.encode(s)
    packet = s + ecc
    print("packet is ", bytearray_to_hex(packet))
    print("len of packet is ", len(packet))

    feat_vec = padding(feat_vec, len(packet))

    c = xor(feat_vec, packet)

    h_w = my_hash(packet)

    return c, h_w


def recover(feat_vec, c, h_w, m):
    """
    특징 벡터에서 w를 복원하고 e와 hash(m,w)를 반환합니다.

    feat_vec : bytearray
    c : bytearray
    h_w : bytearray
    m : bytearray
    """
    print("len of c is ", len(c))
    print("len of feat_vec is ", len(feat_vec))
    print("len of h_w is ", len(h_w))
    print("len of m is ", len(m))
    # assert (len(c) >= len(feat_vec))
    if len(c) < len(feat_vec):
        c = padding(c, len(feat_vec))
    elif len(c) > len(feat_vec):
        feat_vec = padding(feat_vec, len(c))
    l = len(c)
    feat_vec = padding(feat_vec, l)
    w1 = xor(feat_vec, c)
    w = bch_error_correction(w1)

    e = xor(w, w1)

    h_m_w = my_hash(m + w)

    recovered_h_W = my_hash(w)
    print(recovered_h_W)

    return e, h_m_w, recovered_h_W


def generate_proof(feat_vec, err, feat_xor_ecc, message):
    session_id = generate_filename(20)
    session_dir = os.path.join("./storage", session_id)
    print(session_dir)
    # params_dir = "../build/params"
    # pk_dir = "../build/pk"

    if not os.path.exists('./storage'):
        os.mkdir('./storage')

    os.mkdir(session_dir)
    input_path = os.path.join(session_dir, "input.json")
    input_data = {
        "features": bytearray_to_hex(padding(feat_vec, CODE_LEN)),
        "errors": bytearray_to_hex(padding(err, CODE_LEN)),
        "commitment": bytearray_to_hex(padding(feat_xor_ecc, CODE_LEN)),
        "message": bytearray_to_hex(message)
    }
    input_json = json.dumps(input_data)
    with open(input_path, "w") as f:
        f.write(input_json)

    # public input을 assert하면서 실패하면 False를 반환합니다.
    proof_path = os.path.join(session_dir, "proof.hex")
    public_input_path = os.path.join(session_dir, "public.json")
    try:
        evm_prove(
            params_dir="./circuit/params",
            app_circuit_config="./circuit/configs/test1_circuit.config",
            agg_circuit_config="./circuit/configs/agg_circuit.config",
            pk_dir="./circuit/pks",
            input_path=input_path,
            proof_path=proof_path,
            public_input_path=public_input_path
        )
    except:
        return False, b'', session_id

    # hex로 된 proof를 반환합니다.
    with open(proof_path, 'r') as f:
        # hex
        proof_bin = hex_to_bytearray(f.read())
        return True, proof_bin, session_id
    # shutil.rmtree(session_dir)


# 256비트 길이의 특징 벡터를 생성합니다.
# vec = np.random.randint(0, 2, 256)
# print(vec)
# bin_vec = bytearray(np.packbits(vec))
# print("bin_vec is ",bytearray_to_hex(bin_vec))
# bin_vec = padding(bin_vec, 64)
# print("padding bin_vec is ",bin_vec)
# h_w, c = fuzzy_commitment(bin_vec)
# print ("h_w is ",h_w), print("c is ",c)


def main():
    generate_proof(
        hex_to_bytearray(
            "0xddeb3779c4515c05a06495c3ec2403655d9b784d7502a064ebf3c093474b23ce"),
        hex_to_bytearray(
            "0x00000004410000000010a16008004002028000300200000100025001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"),
        hex_to_bytearray(
            "0x7d7fbf998b8e8d29756bcea0755e51a2e7208e3d9df90aa741450ced38cddbfcc8a96ccce1daa8bff47472d07907a612a761b2a1ec37d25407a6952020e413ee12f40ca7d81cb0dcab51591c3495c4b63134518969ec7c69b6469f0ab20e3d82ceffe4eda9ed71550f0ac020061eb7907cfd6eb54849fa5c7fc882764d7f815c08f5fee653a47402"),
        hex_to_bytearray("0x9a8f43")
    )


if __name__ == '__main__':
    main()
