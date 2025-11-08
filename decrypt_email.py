import sys
sys.stdout.reconfigure(encoding='utf-8')

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def load_key(path):
    with open(path, "rb") as f:
        return f.read()

receiver_private_key = serialization.load_pem_private_key(
    load_key("keys/receiver_private.pem"), password=None
)

# Load encrypted AES key
with open("messages/encrypted_key.bin", "rb") as f:
    encrypted_aes_key = f.read()

# Decrypt AES key
aes_key = receiver_private_key.decrypt(
    encrypted_aes_key,
    padding.OAEP(
        mgf=padding.MGF1(hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Load and decrypt email
with open("messages/email_encrypted.bin", "rb") as f:
    data = f.read()
iv, ciphertext = data[:16], data[16:]

cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv))
decryptor = cipher.decryptor()
plaintext = decryptor.update(ciphertext) + decryptor.finalize()

# Save decrypted message
with open("messages/email_decrypted.txt", "wb") as f:
    f.write(plaintext)

print("✅ Email decrypted successfully.")
