#
# encryption.py
# amplecoin
#
# March 19 2020
#
#

import Crypto as cry
from Crypto import Random
from Crypto.PublicKey import RSA

# ret: private key, public key
def gen_keys() -> (bytes, bytes):
    rand_gen = Random.new().read
    key = RSA.generate(2048, rand_gen)
    return (key.exportKey(), key.publickey().exportKey())

# ret: digest, hexdigest
def gen_hash(data: bytes) -> (bytes, str):
    datahash = cry.Hash.SHA256.new(data)
    return (datahash.digest(), datahash.hexdigest())

def gen_sign(hash: (bytes, str), key) -> (int,):
    return key.sign(hash[0], '')

def verify_sign(hash: (bytes, str), pk, sign: (int,)) -> bool:
    return pk.verify(hash[0], sign)

