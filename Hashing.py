from cryptography.hazmat.primitives import hashes

digest = hashes.Hash(hashes.SHA256())
digest.update(b"This is a test")
digest.update(b"1234")
hashed = digest.finalize()
print(hashed)

digest2 = hashes.Hash(hashes.SHA256())
digest2.update(b"This is another test")
hashed2 = digest2.finalize()
print(hashed2)