import sys
sys.stdout.reconfigure(encoding='utf-8')

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

os.makedirs("messages", exist_ok=True)

# Load keys
def load_key(path):
    with open(path, "rb") as f:
        return f.read()

sender_private_key = serialization.load_pem_private_key(
    load_key("keys/sender_private.pem"), password=None
)
receiver_public_key = serialization.load_pem_public_key(
    load_key("keys/receiver_public.pem")
)

# Read message
with open("messages/email.txt", "rb") as f:
    plaintext = f.read()

# AES encryption
aes_key = os.urandom(32)
iv = os.urandom(16)
cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv))
encryptor = cipher.encryptor()
ciphertext = encryptor.update(plaintext) + encryptor.finalize()

# Save encrypted message
with open("messages/email_encrypted.bin", "wb") as f:
    f.write(iv + ciphertext)

# Encrypt AES key with receiver’s public key
encrypted_aes_key = receiver_public_key.encrypt(
    aes_key,
    padding.OAEP(
        mgf=padding.MGF1(hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

with open("messages/encrypted_key.bin", "wb") as f:
    f.write(encrypted_aes_key)

# Digital signature (signing plaintext)
signature = sender_private_key.sign(
    plaintext,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

with open("messages/signature.bin", "wb") as f:
    f.write(signature)

print("✅ Email encrypted, AES key secured, and signature generated.")

print("✅ Email successfully encrypted and signed.\nFiles saved in 'messages/' folder.")
