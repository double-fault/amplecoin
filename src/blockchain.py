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
    # todo: makes adj_list work on hashes not indexes for uniformity between nodes
    def __init__(self, genesis_block: block = None,
            adj_list = {'0': []}, blocks = list(), transactions = list()):
        self.genesis_block = genesis_block        # Indexed 0 
        self.adj_list = adj_list
        self.blocks = [genesis_block]
        self.blocks.extend(blocks)
        self.transactions = transactions

        self.block_broadcast = []

    # O(n)
    def find_block(self, hash: (bytes, str), curr: int = 0) -> int:
        if self.blocks[curr].hash == hash: return curr
        for each in adj_list[curr]:
            assert self.blocks[each].depth > self.blocks[curr].depth, \
                    "what the fuck"
            pos = find_block(hash, each)
            if pos != -1: return pos
        return -1

    # todo: returns random chain if multiple ones with equal lengths exist; fix this (maybe store the
    #       longest chain in some sort of cache?)
    # Finds chain with most Proof of Work
    def longest_chain(self, curr: int = 0) -> list:
        ret = []
        for each in adj_list[curr]:
            assert self.blocks[each].depth > self.blocks[curr].depth, \
                    "and the rain will kill us all"
            tret = longest_chain(each)
            if len(tret) > len(ret): ret = tret
        ret.insert(0, curr)
        return ret

    def mine(self, beneficiary: bytes):
        assert self.genesis_block != None, "No genesis block"
        idx = self.longest_chain()[-1]

        b = block(self.transactions, self.blocks[idx].depth + 1, self.blocks[idx].hash,
                self.blocks[idx].hash.tid + len(self.blocks[idx].transactions) +
                len(self.transactions))
        self.transactions = []
        b.mine(beneficiary)
        b.validate()

        self.add_block(b)
        self.block_broadcast.append(b)

    def add_block(self, b: block):
        idx = find_block(b.prev_hash)
        b.validate()
        assert idx != -1, "Block parent not found"

        self.blocks.append(b)
        num = len(self.blocks) - 1
        adj_list[idx].append(num)
        adj_list[num] = []

    def validate(self, curr: int = 0):
        self.blocks[curr].validate()
        for each in adj_list[curr]:
            assert self.blocks[each].prev_hash == self.blocks[curr].hash, \
                    "Invalid previous hash"
            self.validate(each)
    
    def gen_json(self) -> dict:
        assert self.genesis_block != None, "No genesis block"
        return {
                'adj_list': adj_list,
                'blocks': [x.jsondump() for x in self.blocks]
        }

    def jsondump(self) -> str:
        return json.dumps(self.gen_json())

    def balance(self, pk: bytes) -> float:
        assert self.genesis_block != None, "No genesis block"
        blocks = self.longest_chain()
        ret = 0.0
        for each in blocks:
            ret += each.balance(pk)
        for each in self.transactions:
            if each.payee == pk: ret -= each.amount
            elif each.beneficiary == pk: ret += each.amount
        return ret

    # Will throw AssertionError from validation function or otherwise in case of errors
    def transact(self, payee: bytes, beneficiary: bytes, payee_sk: bytes, amount: float):
        assert self.genesis_block != None, "No genesis block"
        assert amount > 0, "Transaction amount must be greater than 0"

        balance = self.balance(payee)
        assert balance >= amount, "Payee does not have sufficient balance for transaction"

        t = transaction(self.tid + len(self.transactions), payee, beneficiary, amount)
        t.sign(payee_sk)
        t.validate()

        self.transactions.append(t)

    def load_block(self, json: dict) -> block:
        transactions = [transaction(et['tid'], et['payee'].encode(), et['beneficiary'].encode(),
             et['amount'], et['signature'], et['time']) for et in each['transactions']]
        b = block(transactions, each['depth'], 
                (each['prev_hash'][0].encode(), each['prev_hash'][1]), each['tid'], 
                each['nonce'],
                (each['hash'][0].encode(), each['hash'][1]), each['time'])
        return b

    def load_blocks(self, json: dict, rewrite: bool = False):
        assert rewrite or self.genesis_block == None, "Blockchain not empty" 

        self.adj_list = json['adj_list']
        self.transactions = []
        self.blocks = [self.load_block(x) for x in json['blocks']]
        self.genesis_block = self.blocks[0]
        
        self.validate()

