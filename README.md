# Email Encryption & Decryption using S/MIME Simulation

## Objective
To simulate secure email transmission using hybrid encryption (AES + RSA) and digital signatures following the S/MIME standard.

## Tools Used
- Python 3
- cryptography library

## Workflow
1. Generate RSA key pairs for sender and receiver.
2. Encrypt the email content using AES.
3. Encrypt the AES key using receiver’s RSA public key.
4. Sign the original message using sender’s private key.
5. Receiver decrypts AES key and message using their private key.
6. Receiver verifies signature using sender’s public key.

## Output Files
- `email_encrypted.bin` → Encrypted email content
- `encrypted_key.bin` → AES key encrypted with RSA
- `signature.bin` → Digital signature file
- `email_decrypted.txt` → Final decrypted email

## Run Commands
```bash
python generate_keys.py
python encrypt_email.py
python decrypt_email.py
python verify_signature.py
