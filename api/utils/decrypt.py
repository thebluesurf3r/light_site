from cryptography.fernet import Fernet

# Load the key from the file
with open("secret.key", "rb") as key_file:
    key = key_file.read()

# Initialize the cipher suite with the key
cipher_suite = Fernet(key)

# Read the encrypted credentials from the file
with open("/home/tron/Projects/data_analysis/django/emails/credentials.enc", "rb") as enc_file:
    encrypted_username, encrypted_password = enc_file.read().split(b"\n")

# Decrypt the credentials
decrypted_username = cipher_suite.decrypt(encrypted_username).decode('utf-8')
decrypted_password = cipher_suite.decrypt(encrypted_password).decode('utf-8')

print(f"Decrypted Username: {decrypted_username}")
print(f"Decrypted Password: {decrypted_password}")
