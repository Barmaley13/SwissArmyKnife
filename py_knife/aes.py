"""
AES Encrypt/Decrypt Library
"""

### IMPORTS ###
from hashlib import md5

from Crypto.Cipher import AES
from Crypto import Random


### FUNCTIONS ###
def encrypt(in_filename, out_filename, password):
    """ External Encrypt function """
    try:
        in_file = open(in_filename, 'rb')
        out_file = open(out_filename, 'wb')
        in_file.seek(0)
        out_file.seek(0)
        _encrypt(in_file, out_file, password)
    except:
        return False
    else:
        in_file.close()
        out_file.close()
        return True


def _encrypt(in_file, out_file, password, key_length=32):
    """ Internal Encrypt function """
    bs = AES.block_size
    salt = Random.new().read(bs - len('Salted__'))
    key, iv = _derive_key_and_iv(password, salt, key_length, bs)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    out_file.write('Salted__' + salt)
    finished = False
    while not finished:
        chunk = in_file.read(1024 * bs)
        if len(chunk) == 0 or len(chunk) % bs != 0:
            padding_length = bs - (len(chunk) % bs)
            chunk += padding_length * chr(padding_length)
            finished = True
        out_file.write(cipher.encrypt(chunk))


def decrypt(in_filename, out_filename, password):
    """ External Decrypt function """
    try:
        in_file = open(in_filename, 'rb')
        out_file = open(out_filename, 'wb')
        in_file.seek(0)
        out_file.seek(0)
        _decrypt(in_file, out_file, password)
    except:
        return False
    else:
        in_file.close()
        out_file.close()
        return True


def _decrypt(in_file, out_file, password, key_length=32):
    """ Internal Decrypt function """
    bs = AES.block_size
    salt = in_file.read(bs)[len('Salted__'):]
    key, iv = _derive_key_and_iv(password, salt, key_length, bs)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    next_chunk = ''
    finished = False
    while not finished:
        chunk, next_chunk = next_chunk, cipher.decrypt(in_file.read(1024 * bs))
        if len(next_chunk) == 0:
            padding_length = ord(chunk[-1])
            if padding_length < 1 or padding_length > bs:
                raise ValueError("bad decrypt pad (%d)" % padding_length)
            # all the pad-bytes must be the same
            if chunk[-padding_length:] != (padding_length * chr(padding_length)):
                # this is similar to the bad decrypt:evp_enc.c from openssl program
                raise ValueError("bad decrypt")
            chunk = chunk[:-padding_length]
            finished = True
        out_file.write(chunk)


def _derive_key_and_iv(password, salt, key_length, iv_length):
    """ Derive Key and IV """
    d = d_i = ''
    while len(d) < key_length + iv_length:
        d_i = md5(d_i + password + salt).digest()
        d += d_i
    return d[:key_length], d[key_length:key_length + iv_length]
