from block import block
import encryption as enc

b = block([], 2, enc.gen_hash("hello".encode()), 101)
sk1, pk1 = enc.gen_keys()

b.mine(pk1)
print(b.transactions)
print(b.hash[1])
print(b.spec_number)

