# 
# node.py
# amplecoin
#
# March 22 2020
#
#

from blockchain import blockchain
from network import network
from block import block
import encryption as enc
import logging
logging.basicConfig(format='%(asctime)-15s %(message)s')
logging.getLogger().setLevel(logging.INFO)

def signal_handler(sig, frame):
    global node
    node.stop = True

import signal
signal.signal(signal.SIGINT, signal_handler)

bc = blockchain()

node = network()
node.setup()

node.sync()
sk, pk = enc.gen_keys()

try:
    while bc.genesis_block == None and not node.stop: node.run(bc)
    if not node.stop:
        bc.mine(pk)
        while node.run(bc): pass
except AssertionError as err:
    logging.error(err)

