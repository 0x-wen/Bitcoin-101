import ecdsa
from ecdsa.ellipticcurve import PointJacobi


def derive_public_key(private_key: bytes, compressed: bool = False) -> bytes:
    Q: PointJacobi = int.from_bytes(
        private_key, byteorder='big') * ecdsa.curves.SECP256k1.generator
    xstr: bytes = Q.x().to_bytes(32, byteorder='big')
    ystr: bytes = Q.y().to_bytes(32, byteorder='big')
    if compressed:
        parity: int = Q.y() & 1
        return (2 + parity).to_bytes(1, byteorder='big') + xstr
    else:
        return b'\04' + xstr + ystr


prikey = bytearray.fromhex(
    '1e99423a4ed27608a15a2616a2b0e9e52ced330ac530edcc32c8ffc6a526aedd')
uncompressed_pubkey = derive_public_key(prikey, False)
print("uncompressed public key =", uncompressed_pubkey.hex())
compressed_pubkey = derive_public_key(prikey, True)
print("compressed public key =", compressed_pubkey.hex())


def create_private_key():
    # 使用 SECP256k1 曲线生成私钥
    private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    # 从私钥生成公钥
    public_key = private_key.get_verifying_key()

    # 导出私钥和公钥（十六进制形式）
    private_key_hex = private_key.to_string().hex()
    public_key_hex = public_key.to_string().hex()

    # 公钥非压缩格式 (04 + x + y)
    public_key_uncompressed = "04" + public_key_hex
    print(f"-----------------------------------------------------------")
    print(f"Private Key (hex): {private_key_hex}")
    print(f"Public Key (uncompressed hex): {public_key_uncompressed}")
    print(f"-----------------------------------------------------------")
    private_key_bytes = private_key.to_string()
    uncompressed_pubkey = derive_public_key(private_key_bytes, False)
    print("uncompressed public key =", uncompressed_pubkey.hex())
    compressed_pubkey = derive_public_key(private_key_bytes, True)
    print("compressed public key =", compressed_pubkey.hex())

    return private_key_hex, public_key_uncompressed


def public_key():
    """
    比特币中使用 Schnorr 签名时，编码的公钥只是表示为 32 字节十六进制字符串的 x 坐标：
    """
    public_key = {
        "x": 94143704248521553317086831157498059579898345832673799690735511018320990355030,
        "y": 44438543306112247703620323006762464482367802894269621488396118668492541437765,
    }

    hex_string = hex(public_key.get("x"))
    print(f"Schnorr 签名使用公钥: {hex_string[2:]}")


if __name__ == "__main__":
    public_key()
    create_private_key()
