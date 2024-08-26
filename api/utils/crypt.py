from cryptography.fernet import Fernet

# Load or generate a key
try:
    with open("/home/tron/Projects/data_analysis/django/job_django/config/secret.key", "rb") as key_file:
        key = key_file.read()
except FileNotFoundError:
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

# Encrypt the credentials
cipher_suite = Fernet(key)
username = b"vyomdeepansh@gmail.com"
password = b"ozkr daqc upaj tryq"

encrypted_username = cipher_suite.encrypt(username)
encrypted_password = cipher_suite.encrypt(password)

# Save the encrypted credentials to a file
with open("/home/tron/Projects/data_analysis/django/emails/credentials.enc", "wb") as enc_file:
    enc_file.write(encrypted_username + b"\n" + encrypted_password)

print("Credentials encrypted and saved to credentials.enc")
