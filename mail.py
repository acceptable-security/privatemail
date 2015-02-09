from enc import PureSalsa20, rand, public
from hashlib import sha256
from gmpy2 import mpz

import gmpy2
import struct
import base64
import hmac
import datetime
import os
import logins

def crypto_int(s):
    return int(s.encode('hex'), 16)

def rsa(m, e, n):
    return gmpy2.powmod(m, e, n)

def encrypt_msg(message, n, e):
    key = rand.generate_Key()
    ver_key = rand.generate_Key()
    nonce = rand.generate_IV()

    ekey = rsa(crypto_int(key), e, n)
    enon = crypto_int(nonce)

    s = PureSalsa20.Salsa20(key = key, IV = nonce)

    enc_msg   = base64.b64encode(s.encryptBytes(message))
    enc_key   = base64.b64encode(str(int(ekey)))
    enc_nonce = base64.b64encode(str(int(enon)))

    ver = hmac.HMAC(ver_key.encode('hex'), enc_msg, sha256)
    enc_ver_key = base64.b64encode(str(int(rsa(crypto_int(ver_key), e, n))))

    return enc_msg, enc_key, enc_nonce, ver.hexdigest(), enc_ver_key

def receive_message(email, key, msg, encrypted=False):
    if not encrypted:
        key = key.replace("\r\n", "\n")
        key = key.replace("\n\n", "\n")

        try:
            r = public.decode_key(str(key))
        except:
            return False

        if not r:
            return False

        n, e = r
        enc_msg, enc_key, enc_nonce, ver, enc_ver_key = encrypt_msg(str(msg), n, e)
        msg = '\n'.join(["MAILVER1", enc_msg, enc_key, enc_nonce, ver, enc_ver_key])

    path = logins.uhash(email)
    path = logins.mail_path(path)

    try:
        fid = int(open(path + "/ID").read())#len(os.listdir("mail/" + sha256(email).hexdigest()))
    except:
        fid = 0

    timestamp = str(datetime.datetime.now()).split('.')[0].replace(":", ".")

    mpath = path + "/" + str(fid) + "_" + timestamp

    f = open(mpath, 'w')
    f.write(msg)
    f.close()

    fid += 1
    f = open(path + "/ID", 'w')
    f.write(str(fid))
    f.close()

    return True

def key_good(pk):
    return public.identify_key(pk) == "PEM"

if __name__ == "__main__":
    n, e = public.decode_key(open("keys/example.txt").read())

    enc_msg, enc_key, enc_nonce, ver, enc_ver_key = encrypt_msg("test", n, e)
    print enc_msg
    print
    print enc_key
    print
    print enc_nonce
    print
    print ver
    print
    print enc_ver_key
