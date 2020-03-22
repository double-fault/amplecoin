#
# run.py
# amplecoin
#
# March 22 2020
#
#

from blockchain import blockchain
from network import network
from block import block
import encryption as enc
import time

import signal
import logging
logging.basicConfig(format='%(asctime)-15s %(clientip)s %(user)-8s %(message)s')

alice_sk, alice_pk = enc.gen_keys()
bob_sk, bob_pk = enc.gen_keys()

genesis_block = block([], 0, ("".encode(), ""))
genesis_block.mine(alice_pk)
bc = blockchain(genesis_block)

node = network()
node.setup()

try:
    while node.run(bc): pass
except AssertionError as err:
    print(err)

def signal_handler(sig, frame):
    global node
    node.stop = True

