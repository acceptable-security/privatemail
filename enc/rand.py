import os

def generate_IV():
    return os.urandom(8)

def generate_Key():
    return os.urandom(32)
