import nacl.encoding
import nacl.exceptions
import nacl.hash
import nacl.secret


def encrypt(data, *, password):
    secret_key = nacl.hash.sha256(
        password.encode("utf-8"), encoder=nacl.encoding.RawEncoder
    )
    secret_box = nacl.secret.SecretBox(secret_key)
    encrypted_data = secret_box.encrypt(data)
    del secret_key, secret_box
    return encrypted_data


def decrypt(data, *, password):
    secret_key = nacl.hash.sha256(
        password.encode("utf-8"), encoder=nacl.encoding.RawEncoder
    )
    secret_box = nacl.secret.SecretBox(secret_key)
    plain_text = secret_box.decrypt(data)
    del secret_key, secret_box
    return plain_text
