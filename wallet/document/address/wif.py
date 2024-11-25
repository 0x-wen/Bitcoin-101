#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import hashlib
import base58
from typing import Union


def scrub_input(hex_str_or_bytes: Union[str, bytes]) -> bytes:
    if isinstance(hex_str_or_bytes, str):
        hex_str_or_bytes = bytes.fromhex(hex_str_or_bytes)
    return hex_str_or_bytes


# wallet import format key - base58 encoded format
# https://bitcoin.stackexchange.com/questions/9244/private-key-to-wif
def gen_wif_key(private_key: Union[str, bytes], compressed_WIF: bool = False) -> bytes:
    private_key = scrub_input(private_key)

    # prepended mainnet version byte to private key
    mainnet_private_key = b'\x80' + private_key
    if compressed_WIF:
        mainnet_private_key = b'\x80' + private_key + b'\x01'
    # perform SHA-256 hash on the mainnet_private_key
    sha256 = hashlib.sha256()
    sha256.update(mainnet_private_key)
    hash = sha256.digest()

    # perform SHA-256 on the previous SHA-256 hash
    sha256 = hashlib.sha256()
    sha256.update(hash)
    hash = sha256.digest()

    # create a checksum using the first 4 bytes of the previous SHA-256 hash
    # append the 4 checksum bytes to the mainnet_private_key
    checksum = hash[:4]

    hash = mainnet_private_key + checksum

    # convert mainnet_private_key + checksum into base58 encoded string
    return base58.b58encode(hash)


def decode_wif(wif: str) -> bytes:
    compressed = False
    if wif.startswith('K') or wif.startswith('L'):
        compressed = True
    decoded = base58.b58decode(wif)
    if compressed:
        private_key = decoded[1:-5]  # [80 xxx 1 checksum]
    else:
        private_key = decoded[1:-4]  # [80 xxx checksum]
    return private_key


prikey = '0c28fca386c7a227600b2fe50b7cae11ec86d3bf1fbe471be89827e19d72aa1d'  # hex
wif = gen_wif_key(prikey)
print(wif)  # 5HueCGU8rMjxEXxiPuD5BDku4MkFqeZyd4dZ1jvhTVqvbTLvyTJ
wif_compressed = gen_wif_key(prikey, True)
print(wif_compressed)  # KwdMAjGmerYanjeui5SHS7JkmpZvVipYvB2LJGU1ZxJwYvP98617

prikey = decode_wif('5HueCGU8rMjxEXxiPuD5BDku4MkFqeZyd4dZ1jvhTVqvbTLvyTJ')
print(prikey.hex())  # 0c28fca386c7a227600b2fe50b7cae11ec86d3bf1fbe471be89827e19d72aa1d
