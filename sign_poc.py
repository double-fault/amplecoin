# Modified from source: https://gist.github.com/petri/650e27c712888bf4cb27c99716d36e45
# Digital Signature POC

import sys

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random

def generate_keys():
   random_generator = Random.new().read
   key = RSA.generate(2048, random_generator)
   return (key.exportKey(), key.publickey().exportKey())

def generate_hash(data):
   return SHA256.new(data).digest()

def generate_signature(hash, key):
   return key.sign(hash, '')

def verify_signature(hash, public_key, signature):
   return public_key.verify(hash, signature)

sk, pk = generate_keys()
sk2, pk2 = generate_keys()

dhash = generate_hash("abcd".encode()) # Basic convert to string
enc = generate_signature(dhash, RSA.importKey(sk2))
print(verify_signature(dhash, RSA.importKey(pk), enc))   # => False
print(verify_signature(dhash, RSA.importKey(pk2), enc))  # => True

