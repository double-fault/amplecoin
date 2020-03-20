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

class block:
    def __init__(self, transactions, depth: int, prev_hash: (bytes, str), tid: int = 0): 
        self.transactions = transactions
        self.depth = depth
        self.prev_hash = prev_hash
        self.spec_number = None
        self.hash = enc.gen_hash("sleep now in the fire".encode())
        self.tid = tid
        self.time = time.time()

    def get_hashable_data(self) -> str:
        data = [x.jsondump() for x in self.transactions] 
        return str(self.time) + ' ' + str(self.depth) + ' ' + str(self.prev_hash[1]) + ' '.join(data)

    def mine(self, beneficiary: bytes) -> None:
        self.time = time.time()
        self.transactions.append(transaction(self.tid + len(self.transactions), 
            "13".encode(), beneficiary, MINE_REWARD))
        data = self.get_hashable_data() 

        while not self.hash[1].startswith('0' * NUM_ZEROES):
            self.spec_number = rand.randint(1, 163527364)
            tdata = data + str(self.spec_number)
            self.hash = enc.gen_hash(tdata.encode())

    def validate(self):
        data = self.get_hashable_data() + str(self.spec_number)
        hash = enc.gen_hash(data.encode())
        assert hash == self.hash, "Invalid block hash"
        assert hash[1].startswith('0' * NUM_ZEROES), "Block has does not start with " + str(NUM_ZEROES)+\
            " zeroes"

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
                'prev_hash': [str(self.prev_hash[0]), self.prev_hash[1]],
                'spec_number': self.spec_number,
                'hash': [str(self.hash[0]), self.hash[1]],
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

