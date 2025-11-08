from Crypto.PublicKey import RSA
import os
import sys

# ✅ Ensure correct encoding
sys.stdout.reconfigure(encoding='utf-8')

def generate_keypair(name):
    # ✅ Use the current workspace keys directory
    keys_dir = "keys"
    os.makedirs(keys_dir, exist_ok=True)

    print(f"\n⚙️ Generating {name} keys inside: {keys_dir}")

    # ✅ Generate a strong RSA key
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    private_path = os.path.join(keys_dir, f"{name}_private.pem")
    public_path = os.path.join(keys_dir, f"{name}_public.pem")

    # ✅ Write private key
    print(f"Writing private key to: {os.path.abspath(private_path)}")
    print(f"Private key length: {len(private_key)} bytes")
    with open(private_path, "wb") as f:
        bytes_written = f.write(private_key)
        f.flush()
        os.fsync(f.fileno())
        print(f"Bytes written to private key: {bytes_written}")
    
    if os.path.exists(private_path):
        actual_size = os.path.getsize(private_path)
        print(f"✅ {name} private key written ({actual_size} bytes)")
    else:
        print(f"❌ Private key file not found after writing!")

    # ✅ Write public key
    print(f"Writing public key to: {os.path.abspath(public_path)}")
    print(f"Public key length: {len(public_key)} bytes")
    with open(public_path, "wb") as f:
        bytes_written = f.write(public_key)
        f.flush()
        os.fsync(f.fileno())
        print(f"Bytes written to public key: {bytes_written}")
    
    if os.path.exists(public_path):
        actual_size = os.path.getsize(public_path)
        print(f"✅ {name} public key written ({actual_size} bytes)")
    else:
        print(f"❌ Public key file not found after writing!")


if __name__ == "__main__":
    print("🔐 Starting RSA key generation...")

    generate_keypair("sender")
    generate_keypair("receiver")

    print("\n✅ Done generating all key pairs successfully.")
