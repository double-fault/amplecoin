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

val = "abcdf"
num = 0
while True:
    vhash = SHA256.new((val + str(num)).encode()).hexdigest()
    print(vhash)
    if vhash[:5] == '00000':
        print(num)
        break
    num += 1

