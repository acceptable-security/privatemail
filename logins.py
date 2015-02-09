from hashlib import sha256
import sqlite3
import os
import hmac

PSALT = "ASD&dijklj128APd-120p[;]"
USALT = "AKSJDA*S7S098&)*(&*()&15h)"
FSALT = "AS(7S&)(*;'eryyyw$#@ASD325')"

# This needs to be changed to use PBKDF2

def phash(pasw):
    return hmac.HMAC(str(pasw), PSALT, sha256).hexdigest()

def uhash(pasw):
    return hmac.HMAC(str(pasw), USALT, sha256).hexdigest()


def login(user, pasw):
    user = uhash(user)
    pasw = phash(pasw)

    conn = sqlite3.connect("database.db")
    curr = conn.cursor()

    curr.execute("SELECT * FROM users WHERE user=? AND password=?", (user, pasw))
    sel = curr.fetchone()

    conn.close()

    return sel != None

def register(user, pasw, pk):
    user = uhash(user)
    pasw = phash(pasw)

    conn = sqlite3.connect("database.db")
    curr = conn.cursor()

    curr.execute("SELECT * FROM users WHERE user=?", (user,))
    sel = curr.fetchone()

    if sel:
        conn.close()
        return "User or Public Key is in use."

    curr.execute("INSERT INTO users VALUES (?, ?)", (user, pasw))

    os.makedirs(mail_path(user))
    f = open(mail_path(user) + "/PK",'w')
    f.write(pk)
    f.close()

    conn.commit()
    conn.close()

    return "Success"

def public_key(user):
    user = uhash(user)

    return open(mail_path(user) + "/PK").read()

def mail_path(user):
    return "mail/" + sha256(user + FSALT).hexdigest()
