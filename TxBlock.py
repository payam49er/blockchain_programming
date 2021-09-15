from BasicBlockChain import CBlock
import Signitures
from Transaction import TX
import pickle


class TxBlock(CBlock):
    def __init__(self, previous_block: CBlock):
        super(TxBlock, self).__init__([], previous_block)

    def is_valid(self):
        if not super(TxBlock, self).is_valid():
            return False
        for tx in self.data:
            if not tx.is_valid():
                return False
        return True

    def add_tx(self, tx_in):
        self.data.append(tx_in)


if __name__ == "__main__":
    try:

        # generate private and public keys
        pr1, pu1 = Signitures.generate_keys()
        pr2, pu2 = Signitures.generate_keys()
        pr3, pu3 = Signitures.generate_keys()


        def load_serialized_key(data_file):
            with open(data_file, 'rb') as loaded_file:
                ser_pu = pickle.load(loaded_file)
                return ser_pu


        # creating some transactions
        Tx1 = TX()
        Tx1.add_input(pu1, 1)
        Tx1.add_output(pu2, 1)
        Tx1.sign(pr1)
        if Tx1.is_valid():
            print("Success, Tx1 is valid")
        else:
            print("ERROR! Tx1 is invalid")

        Tx2 = TX()
        Tx2.add_input(pu1, 2)
        Tx2.add_output(pu2, 1)
        Tx2.add_output(pu3, 1)
        Tx2.sign(pr1)

        for t in [Tx1, Tx2]:
            if t.is_valid():
                print("Success! Tx is valid")
            else:
                print("ERROR: Tx is invalid")

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
        save_file = open('save.dat', 'wb')
        pickle.dump(Tx1, save_file)

        save_file.close()

        loadfile = open("save.dat", "rb")
        newTx = pickle.load(loadfile)
        print(newTx.is_valid())

        save_file.close()

        # read the file again as binary read using pickle module
        loaded_pu = load_serialized_key("save.dat")
        print(loaded_pu)

        # Test mining rewards and tx fees
        Tx3 = TX()
        Tx3.add_input(pu3, 1.1)
        Tx3.add_output(pu1, 1)
        Tx3.sign(pr3)

        root = TxBlock(None)
        root.add_tx(Tx1)
        B1 = TxBlock(root)
        B1.add_tx(Tx1)
        B1.add_tx(Tx2)

        pr4,pu4 = Signitures.generate_keys()
        B2 = TxBlock(B1)
        Tx5 = TX()
        Tx5.add_input(pu3, 1)
        Tx5.add_output(pu1, 100)
        Tx5.sign(pr3)
        B2.add_tx(Tx5)







    except Exception as e:
        print(f"Exception has occurred: {e}")
        raise e
        print(e.__traceback__.tb_lineno)
