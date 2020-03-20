import encryption as enc
import blockchain

sk1, pk1 = enc.gen_keys()
sk2, pk2 = enc.gen_keys()
sk3, pk3 = enc.gen_keys()
sk4, pk4 = enc.gen_keys()

bc = blockchain.blockchain()
bc.mine(pk1)
bc.mine(pk2)
bc.mine(pk3)
bc.mine(pk4)

# Now all accounts have 10 coins
print(bc.balance(pk1), bc.balance(pk2), bc.balance(pk3), bc.balance(pk4))
# => 10 10 10 10

bc.transact(pk1, pk2, sk1, 10)
bc.transact(pk3, pk2, sk3, 5.5)
bc.transact(pk4, pk3, sk4, 10)

print(bc.balance(pk1), bc.balance(pk2), bc.balance(pk3), bc.balance(pk4))
# should be: 0, 25.5, 15.5, 0

bc.mine(pk1)
print(bc.balance(pk1), bc.balance(pk2), bc.balance(pk3), bc.balance(pk4))
# should be: 10, 25.5, 14.5, 0

# Invalid transactions test

try:
    bc.transact(pk2, pk1, sk2, 25.51)
    print('wtf')
except AssertionError as err:
    print(err)

try:
    bc.transact(pk1, pk4, sk4, 2)
    print('wtf')
except AssertionError as err:
    print(err)

try:
    bc.transact(pk4, pk2, sk4, 0)
    print('wtf')
except AssertionError as err:
    print(err)

