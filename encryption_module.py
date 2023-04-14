import random
from cryptography.fernet import Fernet
from data.constants import KEY_SET


def encrypt_info(info):
    key = random.choice(KEY_SET)
    encrypted_psw = Fernet(key).encrypt(str.encode(info)) + \
                    str(KEY_SET.index(key)).zfill(2).encode()
    return encrypted_psw


def decrypt_info(info):
    key_index = int(info[-2:])
    key = KEY_SET[key_index]
    decrypted_password = Fernet(key).decrypt(info[:-2])
    return decrypted_password.decode()
