import ecdsa
from ecdsa.ellipticcurve import PointJacobi


def derive_public_key(private_key: bytes, compressed: bool = False) -> bytes:
    Q: PointJacobi = int.from_bytes(private_key, byteorder='big') * ecdsa.curves.SECP256k1.generator
    xstr: bytes = Q.x().to_bytes(32, byteorder='big')
    ystr: bytes = Q.y().to_bytes(32, byteorder='big')
    if compressed:
        parity: int = Q.y() & 1
        return (2 + parity).to_bytes(1, byteorder='big') + xstr
    else:
        return b'\04' + xstr + ystr


prikey = bytearray.fromhex('1e99423a4ed27608a15a2616a2b0e9e52ced330ac530edcc32c8ffc6a526aedd')
uncompressed_pubkey = derive_public_key(prikey, False)
print("uncompressed public key =", uncompressed_pubkey.hex())
compressed_pubkey = derive_public_key(prikey, True)
print("compressed public key =", compressed_pubkey.hex())
