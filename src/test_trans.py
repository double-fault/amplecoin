from transaction import transaction
import encryption as enc

sk1, pk1 = enc.gen_keys()
sk2, pk2 = enc.gen_keys()

trans = transaction(1234, pk1, pk2, 5)
trans.sign(sk1)
print(trans.validate())
#trans.sign(sk2)
#print(trans.validate())

trans = transaction(1234, "14".encode(), pk1, 5)
print(trans.validate())

