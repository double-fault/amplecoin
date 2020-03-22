#
# block.py
# amplecoin
#
# Created on March 18 2020.
#
#

from transaction import transaction
from transaction import MINE_REWARD
import time
import random as rand
import encryption as enc
import json

NUM_ZEROES = 4
DEF_HASH = ("abcd".encode(), "abcd")

class block:
    def __init__(self, transactions, depth: int, prev_hash: (bytes, str), 
            tid: int = 0, nonce: int = -1, 
            hash: (bytes, str) = DEF_HASH, ctime: str = '-1'): 
        self.transactions = transactions
        self.depth = depth
        self.prev_hash = prev_hash
        self.nonce = nonce
        self.hash = hash
        self.tid = tid
        self.time = ctime

    def get_hashable_data(self) -> str:
        data = [x.jsondump() for x in self.transactions] 
        return self.time + ' ' + str(self.depth) + ' ' + \
                str(self.prev_hash[1]) + ' '.join(data)

    def mine(self, beneficiary: bytes) -> None:
        self.time = str(time.time())
        self.transactions.append(transaction(self.tid + len(self.transactions), 
            "13".encode(), beneficiary, MINE_REWARD))
        data = self.get_hashable_data() 

        while not self.hash[1].startswith('0' * NUM_ZEROES):
            self.nonce = rand.randint(1, 163527364)
            tdata = data + str(self.nonce)
            self.hash = enc.gen_hash(tdata.encode())

    def validate(self):
        data = self.get_hashable_data() + str(self.nonce)
        print(data.encode())
        hash = enc.gen_hash(data.encode())
        print(hash)
        print(self.hash)
        assert hash == self.hash, "Invalid block hash"
        assert hash[1].startswith('0' * NUM_ZEROES), \
                "Block has does not start with " + str(NUM_ZEROES)+ " zeroes"

        reward = 0
        for each in self.transactions:
            if each.payee == "13".encode():
                assert not reward, "Too many reward transactions in block"
                reward = 1
        assert reward, "No reward transaction in block"

    def gen_json(self) -> dict:
        ratm = [x.gen_json() for x in self.transactions]
        return {
                'transactions': ratm,
                'depth': self.depth,
                'prev_hash': [self.prev_hash[0].decode('utf-8'), self.prev_hash[1]],
                'nonce': self.nonce,
                'hash': [self.hash[0].decode('utf-8'), self.hash[1]],
                'tid': self.tid,
                'time': self.time
        }

    def balance(self, pk: bytes) -> float:
        ret = 0.0
        for each in self.transactions:
            if each.payee == pk: ret -= each.amount
            elif each.beneficiary == pk: ret += each.amount
        return ret

    def jsondump(self) -> str:
        return json.dumps(self.gen_json())

