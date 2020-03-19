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

class block:
    def __init__(self, transactions, depth: int, prev_hash: (bytes, str), tid: int = 0): 
        self.transactions = transactions
        self.depth = depth
        self.prev_hash = prev_hash[1]
        self.spec_number = None
        self.hash = enc.gen_hash("sleep now in the fire".encode())
        self.tid = tid

    def get_hashable_data(self) -> str:
        data = [x.jsondump() for x in self.transactions] 
        return str(time.time()) + ' ' + str(self.depth) + ' ' + str(self.prev_hash) + ' '.join(data)

    def mine(self, beneficiary: bytes) -> None:
        self.transactions.append(transaction(self.tid + len(self.transactions), 
            13, beneficiary, MINE_REWARD))
        data = self.get_hashable_data() 

        while not self.hash[1].startswith('0' * 4):
            self.spec_number = rand.randint(1, 163527364)
            tdata = data + str(self.spec_number)
            self.hash = enc.gen_hash(tdata.encode())

