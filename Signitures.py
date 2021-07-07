from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography import exceptions

def generate_keys():
    private = rsa.generate_private_key(public_exponent=65537,key_size=2048)
    public = private.public_key()
    return private, public

# in a way, signing is like decrypting a message
def sign(message,private_key):
    message = bytes(str(message),'utf-8')
    signature = private_key.sign(message, padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                                                     salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256())
    return signature

def verify(message, signature, public_key):
    try:
        message = bytes(str(message),'utf-8')
        public_key.verify(signature, message, padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                                                          salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
        return True
    except exceptions.InvalidSignature:
        return False
    except:
        print("Error executing public key verify")
        return False

if __name__ == '__main__':
    pr,pu = generate_keys()
    message = b"This is a secret message"
    signature = sign(message, pr)
    correct = verify(message, signature, pu)

    if correct:
        print("Success, good signature")
    else:
        print("Bad signature")

    #todo:simulate attacks
    pr_fake,pu_fake = generate_keys()
    fake_test = verify(message,signature,pu_fake)
    print(f"fake test is: {fake_test}")

    print(pu.public_numbers())


