import click
import nacl.encoding
import nacl.exceptions
import nacl.hash
import nacl.secret
import toml


def encrypt(data):
    password = click.prompt("Password", err=True, confirmation_prompt=True, hide_input=True)
    secret_key = nacl.hash.sha256(password.encode('utf-8'), encoder=nacl.encoding.RawEncoder)

    secret_box = nacl.secret.SecretBox(secret_key)
    encrypted_data = secret_box.encrypt(data)

    del password, secret_key, secret_box

    return encrypted_data


def decrypt(fp):
    with open(fp, 'rb') as fp_:
        cipher_text = fp_.read()

    while True:
        password = click.prompt("Password", hide_input=True, err=True)
        secret_key = nacl.hash.sha256(password.encode('utf-8'), encoder=nacl.encoding.RawEncoder)
        secret_box = nacl.secret.SecretBox(secret_key)
        try:
            plain_text = secret_box.decrypt(cipher_text)
        except nacl.exceptions.CryptoError:
            click.echo("Incorrect Password", err=True, color='red')
        else:
            del password, secret_key, secret_box
            return plain_text
