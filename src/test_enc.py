from Crypto.PublicKey import RSA
import encryption as enc

sk1, pk1 = enc.gen_keys()
sk2, pk2 = enc.gen_keys()

rand_hash = enc.gen_hash("hello world".encode())
sign = enc.gen_sign(rand_hash, RSA.importKey(sk2))

print(enc.verify_sign(rand_hash, RSA.importKey(pk2), sign))
print(enc.verify_sign(rand_hash, RSA.importKey(pk1), sign))

