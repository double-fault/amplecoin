#
# network.py
# amplecoin
#
# March 20 2020
#
#

import socket
import random

NETWORK_PORT=3993

PACKET_PREFIX = "AMPLECOIN"
PACKET_CHAIN_SYNC = PACKET_PREFIX + "_CHAIN_SYNC"
PACKET_CHAIN_SYNC_CONF = PACKET_CHAIN_SYNC + "_CONF"
PACKET_NEW_BLOCK = PACKET_PREFIX + "_NEW_BLOCK"

class network:
    def __init__(self):
        self.stop = False
        self.ident = str(random.randint(0, 100000000)) # todo: constant length random gen 

    def send(self, ip: str, msg: str):
        ss = socket.socket(SOCKET.AF_INET, socket.SOCK_DGRAM)
        ss.sendto(msg, (ip, NETWORK_PORT))

    def setup(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(("", NETWORK_PORT))
        self.socket.settimeout(4)

    def run(self, blockchain) -> bool:
        if self.stop:
            self.socket.close()
            return False

        try:
            data, addr = self.socket.recvfrom(4096)
        except:
            return True
        if data.startswith(self.ident): return True
        data = data[len(self.ident)]

        if data.startswith(PACKET_CHAIN_SYNC):
            self.send(addr[0], self.ident + PACKET_CHAIN_SYNC_CONF + blockchain.jsondump())
        elif data.startswith(PACKET_CHAIN_SYNC_CONF):
            assert not len(blockchain.blocks), \
                    "Blockchain not empty; sync failure"
            data = data[len(PACKET_CHAIN_SYNC_CONF)]
            blockchain.load_blocks(json.loads(data))
        elif data.startswith(PACKET_NEW_BLOCK):

