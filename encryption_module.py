import random
from cryptography.fernet import Fernet
from data.constants import KEY_SET


def encrypt_password(password):
    key = random.choice(KEY_SET)
    encrypted_psw = Fernet(key).encrypt(str.encode(password)) + \
        str(KEY_SET.index(key)).zfill(2).encode()
    return encrypted_psw


def decrypt_password(password):
    key_index = int(password[-2:])
    key = KEY_SET[key_index]
    decrypted_password = Fernet(key).decrypt(password[:-2])
    return decrypted_password.decode()
