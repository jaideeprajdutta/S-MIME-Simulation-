import sys
sys.stdout.reconfigure(encoding='utf-8')

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

def load_key(path):
    with open(path, "rb") as f:
        return f.read()

sender_public_key = serialization.load_pem_public_key(
    load_key("keys/sender_public.pem")
)

with open("messages/email.txt", "rb") as f:
    original_message = f.read()

with open("messages/signature.bin", "rb") as f:
    signature = f.read()

try:
    sender_public_key.verify(
        signature,
        original_message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    print("✅ Signature is valid (message integrity and authenticity verified).")
except Exception as e:
    print("❌ Signature invalid:", e)
