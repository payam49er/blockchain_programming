from BasicBlockChain import CBlock
import Signitures
from Transaction import TX
import pickle
from cryptography.hazmat.primitives import serialization

class TxBlock(CBlock):
    def __init__(self, previousBlock: CBlock):
        self.previous_block = previousBlock
        self.incoming_tx = []

    def addTx(self, Tx_in):
       self.incoming_tx.append(Tx_in)

    def is_valid(self):
        previous_hash = self.previous_block.previous_hash


if __name__ == "__main__":
    pr1, pu1 = Signitures.generate_keys()
    pr2, pu2 = Signitures.generate_keys()
    pr3, pu3 = Signitures.generate_keys()

def serialize_pr_key(private_key, message:str):
    pm = private_key.private_bytes(encoding=serialization.Encoding.PEM,
                              format=serialization.PrivateFormat.PKCS8,
                              encryption_algorithm=serialization.BestAvailableEncryption(f"{bytes(message)}"))
    return pm.splitlines()[0]


def serialize_pu_key(public_key):
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo)
    return pem.splitlines()[0]

    Tx1 = TX()
    Tx1.add_input(serialize_pu_key(pu1), 3)
    Tx1.add_output(serialize_pu_key(pu2), 5)
    Tx1.sign(serialize_pr_key(pr1))
    print(Tx1.is_valid())

    message = b"some message"
    sig = Signitures.sign(message,private_key=pr1)

    savefile = open('save.dat','wb')
    pickle.dump(Tx1,savefile)

    savefile.close()

    loadfile = open("save.dat", "rb")
    newTx = pickle.load(loadfile)
    print(newTx.is_valid())


