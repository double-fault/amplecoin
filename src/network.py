#
# network.py
# amplecoin
#
# March 20 2020
#
#

import socket
import string
import random
import logging

NETWORK_PORT=3993

PACKET_PREFIX = "AMPLECOIN"
PACKET_CHAIN_SYNC = PACKET_PREFIX + "_CHAIN_SYNC"
PACKET_CHAIN_SYNC_CONF = PACKET_CHAIN_SYNC + "_CONF"
PACKET_NEW_BLOCK = PACKET_PREFIX + "_NEW_BLOCK"

class network:
    def __init__(self):
        self.stop = False
        self.ident = self.gen_ident()

    # returns identifier of length 64
    def gen_ident(self) -> str:
        ret = ""
        for i in range(64):
            ret += random.choice(string.ascii_letters)
        return ret

    def send(self, ip: str, msg: str):
        ss = socket.socket(SOCKET.AF_INET, socket.SOCK_DGRAM)
        ss.sendto(msg.encode(), (ip, NETWORK_PORT))

    def setup(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(("", NETWORK_PORT))
        self.socket.settimeout(4)

    def broadcast(self, packet):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(packet.encode(), ('255.255.255.255', NETWORK_PORT))

    def sync(self):
        logging.info("Blockchain sync request broadcasted")
        self.broadcast(self.ident + PACKET_CHAIN_SYNC)

    def run(self, blockchain) -> bool:
        if self.stop:
            self.socket.close()
            return False

        while len(blockchain.block_broadcast):
            msg = self.ident + PACKET_NEW_BLOCK + blockchain.block_broadcast[-1].jsondump()
            self.broadcast(msg)
            logging.info("Broadcasting new block")
            del blockchain.block_broadcast[-1]

        try:
            d, addr = self.socket.recvfrom(4096)
            data = str(d)
        except:
            return True
        if data.startswith(self.ident): return True
        data = data[64:]

        if data.startswith(PACKET_CHAIN_SYNC):
            logging.info("Sending blockchain to %d".format(addr[0]))
            self.send(addr[0], self.ident + PACKET_CHAIN_SYNC_CONF + blockchain.jsondump())
        elif data.startswith(PACKET_CHAIN_SYNC_CONF):
            logging.info("Blockchain received for sync")
            assert not len(blockchain.blocks), \
                    "Blockchain not empty; sync failure"
            data = data[len(PACKET_CHAIN_SYNC_CONF):]
            blockchain.load_blocks(json.loads(data))
        elif data.startswith(PACKET_NEW_BLOCK):
            logging.info("Received new block")
            assert blockchain.genesis_block != None, "Genesis block does not exist"
            data = data[len(PACKET_NEW_BLOCK):]
            b = blockchain.load_block(json.loads(data))
            blockchain.add_block(b)
        return True


