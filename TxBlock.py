from BasicBlockChain import CBlock
import Signitures
from Transaction import TX
import pickle

class TxBlock(CBlock):
    def __init__(self, previousBlock):
        pass

    def addTx(self, Tx_in):
        pass

    def is_valid(self):
        return False


if __name__ == "__main__":
    pr1, pu1 = Signitures.generate_keys()
    pr2, pu2 = Signitures.generate_keys()
    pr3, pu3 = Signitures.generate_keys()

    Tx1 = TX()
    Tx1.add_input(pu1,3)
    Tx1.add_output(pu2,5)
    Tx1.sign(pr1)
    print(Tx1.is_valid())

    message = b"some message"
    sig = Signitures.sign(message,private_key=pr1)

    savefile = open('save.dat','wb')
    pickle.dump(Tx1,savefile)

    savefile.close()

    loadfile = open("save.dat","rb")
    newTx = pickle.load(loadfile)
    print(newTx.is_valid())


