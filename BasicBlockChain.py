import numbers

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes


class CBlock:
    data = None
    previous_hash = None
    previous_block = None
    __hash__ = None

    def __init__(self, data, previous_block):
        self.data = data
        self.previous_block = previous_block
        self.__hash__ = self.compute_hash()
        if previous_block is not None:
            self.previous_hash = previous_block.current_block_hash()

    def compute_hash(self):
        digest = hashes.Hash(hashes.SHA256())
        digest.update(bytes(str(self.data), 'utf-8'))
        digest.update(bytes(str(self.previous_hash),'utf-8'))
        return digest.finalize()

    def current_block_hash(self):
        return self.__hash__


    def is_valid(self):
        if self.previous_block == None:
            return True
        return self.previous_block.compute_hash() == self.current_block_hash()



class someClass():
    num = numbers
    def __init__(self, mystring):
        self.string = mystring

    def __repr__(self):
        return f"{self.string}{self.num}"


if __name__ == '__main__':
    root = CBlock("I am root", None)
    B1 = CBlock("I am a child", root)
    if B1.previous_block.compute_hash() == root.current_block_hash():
        print("Success, hash is good")
    else:
        print("Error! hash is no good")
    B2 = CBlock("I am B1 brother", root)
    B3 = CBlock(12345, B1)
    B4 = CBlock(someClass("Hi there"), B3)
    if B4.previous_hash == B3.current_block_hash():
        print("Success, B4-B2")
    else:
        print("B4-2 failed")

    B3.data = 123456
    if B4.previous_hash == B4.previous_block.compute_hash():
        print("Failed, tampering didn't get detected")
    else:
        print("Success, tampering detected")

    print(B4.data)
    s = someClass("Hi there")
    s.num = 1234
    B4 = CBlock(s,B3)
    print(B4.data)
    if B4.previous_hash == B4.previous_block.compute_hash():
        print("Failed, tampering didn't get detected")
    else:
        print("Success, tampering detected")