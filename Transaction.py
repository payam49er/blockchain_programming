import Signitures

class TX:

    def __init__(self):
        self.inputs = []  # holds tuple of from address and amount
        self.outputs = []  # holds tuple of to addresses and amount
        self.sigs = []  # list of signatures
        self.reqd = []  # list of required signatures, which are not inputs. This is for escrow

    def add_input(self,from_address, amount):
        self.inputs.append((from_address,amount))

    def add_output(self, to_addr, amount):
        self.outputs.append((to_addr,amount))

    def add_reqd(self, addr):
        self.reqd.append(addr)

    def sign(self, private):
        message = self.__gather()
        newsig = Signitures.sign(message, private)
        self.sigs.append(newsig)

    def is_valid(self):
        total_input = 0
        total_output = 0
        for (addr, amount) in self.outputs:
            if amount < 0:
                return False
            total_output += amount
        if total_output > total_input:
            return False
        message = self.__gather()
        for (addr, amount) in self.inputs:
            total_input += amount
            if amount < 0:
                return False
            for s in self.sigs:
                found = False
                if Signitures.verify(message, s, addr):  # message, private key, public key
                    found = True
                if not found:
                    return False
        for (addr, amount) in self.outputs:
            if amount < 0:
                return False
        return True



    def __gather(self):
        data = []
        data.append(self.inputs)
        data.append(self.outputs)
        data.append(self.reqd)
        return data


if __name__ == "__main__":
    pr1, pu1 = Signitures.generate_keys()
    pr2, pu2 = Signitures.generate_keys()
    pr3, pu3 = Signitures.generate_keys()
    pr4, pu4 = Signitures.generate_keys()

    tx1 = TX()
    tx1.add_input(pu1, 1)
    tx1.add_output(pu2, 1)
    tx1.sign(pr1)
    if tx1.is_valid():
        print("Success, TX1 is valid")
    else:
        print("Fail, TX1 is invalid")

    tx2 = TX()
    tx2.add_input(pu2,5)
    tx2.add_input(pu2,2)
    tx2.add_output(pu3,5)
    tx2.add_output(pu1,2)
    tx2.sign(pr2)
    if tx2.is_valid():
        print("Success, TX2 is valid")
    else:
        print("Fail, TX2 is invalid")


