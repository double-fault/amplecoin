#
# transaction.py
# amplecoin
#
# March 19 2020
#
#

import encryption as enc
import time
import json
from Crypto.PublicKey import RSA

MINE_REWARD=10

class transaction:
    # payee is 13 for mining reward
    def __init__(self, tid: int, payee: bytes, beneficiary: bytes, amount: float,
            signature: int = -1, tme: str = "-1"):
        self.signature = signature
        self.payee = payee
        self.beneficiary = beneficiary
        self.amount = amount
        self.time = tme
        if self.time == "-1": self.time = str(time.time())
        self.tid = tid

    def gen_hashable_data(self) -> bytes:
        data = [str(self.tid), str(self.payee), str(self.beneficiary), str(self.amount), self.time]
        return ' '.join(data).encode() 

    def gen_json(self) -> dict:
        return {
                'tid': self.tid,
                'signature': self.signature,
                'payee': str(self.payee),
                'beneficiary': str(self.beneficiary),
                'amount': self.amount,
                'time': self.time
        }

    def jsondump(self) -> str:
        return json.dumps(self.gen_json())

    def sign(self, sk: bytes):
        dhash = enc.gen_hash("bulls on parade".encode())
        signature = enc.gen_sign(dhash, RSA.importKey(sk))
        assert enc.verify_sign(dhash, RSA.importKey(self.payee), signature), \
                "Invalid Private Key"

        self.signature = enc.gen_sign(enc.gen_hash(self.gen_hashable_data()), RSA.importKey(sk))

    def validate(self):
        if self.payee == "13".encode():
            assert self.amount == MINE_REWARD, "False mining reward" 
        else:
            assert self.signature != -1, "No signature on transaction"
            assert enc.verify_sign(enc.gen_hash(self.gen_hashable_data()),
                    RSA.importKey(self.payee), self.signature), "Public Key does not match signature"

