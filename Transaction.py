import Signitures

class TX:


    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.sigs = []  # list of signitures
        self.reqd = []  # list of required signitures, which are not inputs. This is for escrow

    def add_input(self,from_address, amount):
        pass

    def add_output(self, to_addr, amount):
        pass

    def add_reqd(self, addr):
        pass

    def sign(self, private):
        pass

    def is_valid(self):
        return False




if __name__ == "__main__":
    pr1,pu1 = Signitures.generate_keys()
    pr2,pu2 = Signitures.generate_keys()
    pr3,pu3 = Signitures.generate_keys()
    pr4,pu4 = Signitures.generate_keys()

    tx1 = TX()
    tx1.add_input(pu1, 1)
    tx1.add_output(pu2, 1)
    tx1.sign(pr1)
    if tx1.is_valid():
        print("Success, TX1 is valid")
    else:
        print("Fail, TX1 is invalid")



