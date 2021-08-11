from BasicBlockChain import CBlock
import Signitures
from Transaction import TX
import pickle


class TxBlock(CBlock):
    def __init__(self, previousBlock: CBlock):
        self.previous_block = previousBlock
        self.incoming_tx = []

    def addTx(self, Tx_in):
        self.incoming_tx.append(Tx_in)

    def is_valid(self):
        previous_hash = self.previous_block.previous_hash
        print("False")


if __name__ == "__main__":
    try:

        # generate private and public keys
        pr1, pu1 = Signitures.generate_keys()
        pr2, pu2 = Signitures.generate_keys()
        pr3, pu3 = Signitures.generate_keys()

        def load_serialized_key(data_file):
             with open(data_file, 'rb') as loadfile:
                   ser_pu = pickle.load(loadfile)
                   return ser_pu


        # creating some transactions
        Tx1 = TX()
        Tx1.add_input(pu1, 3)
        Tx1.add_output(pu2, 5)
        message = b"simple message"
        # Tx1.sign(serialize_pr_key(pr1, message))
        print(Tx1.is_valid())

        sig = Signitures.sign(message, private_key=pr1)

        # using pickle module to write the transactions to a file as binary
        save_file = open('save.dat', 'wb')
        pickle.dump(Tx1, save_file)

        Tx1 = TX()
        Tx1.add_input(pu1, 3)
        Tx1.add_output(pu2, 5)
        Tx1.sign(pr1)
        print(Tx1.is_valid())

        message = b"some message"
        sig = Signitures.sign(message,private_key=pr1)

        savefile = open('save.dat','wb')
        pickle.dump(Tx1,savefile)

        savefile.close()

        loadfile = open("save.dat", "rb")
        newTx = pickle.load(loadfile)
        print(newTx.is_valid())

        save_file.close()

        # read the file again as binary read using pickle module
        loaded_pu = load_serialized_key("save.dat")
        print(loaded_pu)

    except Exception as e:
            print(f"Exception has occured: {e}")
            print(e.__traceback__.tb_lineno)