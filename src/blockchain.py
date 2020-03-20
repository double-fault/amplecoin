#
# blockchain.py
# amplecoin
#
# March 20 2020
#
#

from block import block
import encryption as enc
from transaction import transaction
import json

class blockchain:
    def __init__(self, blocks = list(), transactions = list(), tid: int = 0):
        self.blocks = blocks
        self.transactions = transactions
        self.tid = 0

    def mine(self, beneficiary: bytes):
        prev_hash = enc.gen_hash("".encode())
        if len(self.blocks): prev_hash = self.blocks[-1].hash 
        b = block(self.transactions, len(self.blocks), prev_hash, self.tid)
        self.tid += len(self.transactions) + 1
        self.transactions = []

        b.mine(beneficiary)
        self.blocks.append(b)
        # todo: transmit mined block over network

    def validate(self):
        if not len(self.blocks): return
        self.blocks[0].validate()
        L = len(self.blocks)
        for i in range(1, L):
            self.blocks[i].validate()
            assert self.blocks[i].prev_hash == self.blocks[i - 1].hash, \
                    "Invalid previous hash for block " + str(i)
    
    def gen_json(self) -> dict:
        return {
                'blocks': [x.jsondump() for x in self.blocks]
        }

    def jsondump(self) -> str:
        return json.dumps(self.gen_json())

    def balance(self, pk: bytes) -> float:
        ret = 0.0
        for each in self.blocks:
            ret += each.balance(pk)
        for each in self.transactions:
            if each.payee == pk: ret -= each.amount
            elif each.beneficiary == pk: ret += each.amount
        return ret

    # Will throw AssertionError from validation function or otherwise in case of errors
    def transact(self, payee: bytes, beneficiary: bytes, payee_sk: bytes, amount: float):
        assert amount > 0, "Transaction amount must be greater than 0"

        balance = self.balance(payee)
        assert balance >= amount, "Payee does not have sufficient balance for transaction"

        t = transaction(self.tid + len(self.transactions), payee, beneficiary, amount)
        t.sign(payee_sk)
        t.validate()

        self.transactions.append(t)

