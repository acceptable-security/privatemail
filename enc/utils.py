from StringIO import StringIO as BytesIO
import struct
import binascii
import re
import types

def tobytes(s):
    if isinstance(s, types.UnicodeType):
        return s.encode("latin-1")
    else:
        return ''.join(s)

def tostr(bs):
    return unicode(bs, 'latin-1')

def bytes_to_long(s):
    acc = 0L
    unpack = struct.unpack
    length = len(s)
    if length % 4:
        extra = (4 - length % 4)
        s = '\000' * extra + s
        length = length + extra
    for i in range(0, length, 4):
        acc = (acc << 32) + unpack('>I', s[i:i+4])[0]
    return acc

def bytes_to_long(s):
    acc = 0L
    unpack = struct.unpack
    length = len(s)
    if length % 4:
        extra = (4 - length % 4)
        s = '\000' * extra + s
        length = length + extra
    for i in range(0, length, 4):
        acc = (acc << 32) + unpack('>I', s[i:i+4])[0]
    return acc

def inverse(u, v):
    u3, v3 = long(u), long(v)
    u1, v1 = 1L, 0L
    while v3 > 0:
        q=divmod(u3, v3)[0]
        u1, v1 = v1, u1 - v1*q
        u3, v3 = v3, u3 - v3*q
    while u1<0:
        u1 = u1 + v
    return u1
