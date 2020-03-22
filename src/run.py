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

def signal_handler(sig, frame):
    global node
    node.stop = True

import signal
signal.signal(signal.SIGINT, signal_handler)

import logging
logging.basicConfig(format='%(asctime)-15s %(message)s')
logging.getLogger().setLevel(logging.INFO)

alice_sk, alice_pk = enc.gen_keys()
bob_sk, bob_pk = enc.gen_keys()

genesis_block = block([], 0, ("".encode('utf-16'), ""))
genesis_block.mine(alice_pk)
bc = blockchain(genesis_block)

node = network()
node.setup()

try:
    while node.run(bc): pass
except AssertionError as err:
    logging.error(err)


