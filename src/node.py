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
logging.basicConfig(format='%(asctime)-15s %(clientip)s %(user)-8s %(message)s')

bc = blockchain()

node = network()
node.setup()

node.sync()

try:
    while node.run(bc): pass
except AssertionError as err:
    print(err)

def signal_handler(sig, frame):
    global node
    node.stop = True

