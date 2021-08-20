from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography import exceptions
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature


# returning a serialized public key and the raw private key for now
def generate_keys():
    '''
     Serialized public key. For now, private key is not serialized. We will do that later
    '''
    private = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private.public_key()
    pu = public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                  format=serialization.PublicFormat.SubjectPublicKeyInfo)
    print(f"public key {pu.splitlines()[0]}")
    return private, pu


# in a way, signing is like decrypting a message
def sign(message, private_key):
    message = bytes(str(message), 'utf-8')
    signature = private_key.sign(message, padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                                                      salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
    return signature


def serialize_pr_key(private_key, message: str):
    pm = private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                   format=serialization.PrivateFormat.PKCS8,
                                   encryption_algorithm=serialization.BestAvailableEncryption(bytes(message)))
    return pm.splitlines()[0]


def old_verify(message, signature, public_key):
    '''
    At this moment, public key is serialized. We need the following logic to work with serialized key
    '''
    try:
        message = bytes(str(message), 'utf-8')
        public_key.verify(signature, message, padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                                                          salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
        return True
    except exceptions.InvalidSignature:
        return False
    except:
        print("Error executing public key verify")
        return False


def verify(message, signiture, public_ser_key):
    public = serialization.load_pem_public_key(public_ser_key,backend=default_backend())
    message = bytes(str(message),'utf-8')
    try:
        public.verify(signiture,message,
                      padding.PSS(
                          mgf=padding.MGF1(hashes.SHA256()),
                          salt_length=padding.PSS.MAX_LENGTH),
                      hashes.SHA256())
        return True
    except exceptions.InvalidSignature:
        return False
    except:
        print("Error executing public key verify")
        return False







if __name__ == '__main__':
    pr, pu = generate_keys()
    message = b"This is a secret message"
    signature = sign(message, pr)
    correct = verify(message, signature, pu)

    if correct:
        print("Success, good signature")
    else:
        print("Bad signature")

    # todo:simulate attacks
    pr_fake, pu_fake = generate_keys()
    fake_test = verify(message, signature, pu_fake)
    print(f"fake test is: {fake_test}")

    print(pu.public_numbers())
