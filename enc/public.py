from der import *
import utils

oid = "1.2.840.113549.1.1.1"

algorithmIdentifier = DerSequence(
  [DerObjectId(oid).encode(),      # algorithm field
  DerNull().encode()]              # parameters field
  ).encode()

def decode_obj(obj_class, binstr):
    der = obj_class()
    der.decode(binstr)
    return der

def identify_key(key_data):
    key_data = tobytes(key_data)

    if key_data.startswith('-----'):
        return "PEM"

    elif key_data.startswith('ssh-rsa '):
        return "SSH"

    elif ord(key_data[0]) == 0x30:
        return "DER"

    return None

def decode_ssh(key_data):
    key_data = tobytes(key_data)

    keystring = binascii.a2b_base64(key_data.split(' ')[1])
    keyparts = []

    while len(keystring) > 4:
        l = struct.unpack(">I", keystring[:4])[0]
        keyparts.append(keystring[4:4 + l])
        keystring = keystring[4 + l:]

    e = bytes_to_long(keyparts[1])
    n = bytes_to_long(keyparts[2])

    return n, e

def decode_pem(key_data):
    r = re.compile("\s*-----BEGIN (.*)-----\n")
    m = r.match(key_data)
    if not m:
        raise ValueError("Not a valid PEM pre boundary")
    marker = m.group(1)

    # Verify Post-Encapsulation Boundary
    r = re.compile("-----END (.*)-----\s*$")
    m = r.search(key_data)
    if not m or m.group(1) != marker:
        raise ValueError("Not a valid PEM post boundary")

    # Removes spaces and slit on lines
    lines = key_data.replace(" ", '').split()

    # Decrypts, if necessary
    if lines[1].startswith('Proc-Type:4,ENCRYPTED'):
        return None
    else:
        objdec = None

    # Decode body
    data = binascii.a2b_base64(''.join(lines[1:-1]))
    enc_flag = False

    return decode_der(data)

def decode_der(key_data):
    try:
        der = decode_obj(DerSequence, key_data)

        # Try PKCS#1 first, for a private key
        if len(der) == 9 and der.hasOnlyInts() and der[0] == 0:
            # ASN.1 RSAPrivateKey element
            del der[6:]     # Remove d mod (p-1),
                            # d mod (q-1), and
                            # q^{-1} mod p
            der.append(inverse(der[4], der[5]))  # Add p^{-1} mod q
            del der[0]      # Remove version
            return der[:]

        # Keep on trying PKCS#1, but now for a public key
        if len(der) == 2:
            try:
                # The DER object is an RSAPublicKey SEQUENCE with
                # two elements
                if der.hasOnlyInts():
                    return der[:]
                # The DER object is a SubjectPublicKeyInfo SEQUENCE
                # with two elements: an 'algorithmIdentifier' and a
                # 'subjectPublicKey'BIT STRING.
                # 'algorithmIdentifier' takes the value given at the
                # module level.
                # 'subjectPublicKey' encapsulates the actual ASN.1
                # RSAPublicKey element.
                if der[0] == algorithmIdentifier:
                    bitmap = decode_obj(DerBitString, der[1])
                    rsaPub = decode_obj(DerSequence, bitmap.value)
                    if len(rsaPub) == 2 and rsaPub.hasOnlyInts():
                        return rsaPub[:]
            except (ValueError, EOFError):
                pass

        return None # fuck PKCS8

    except (ValueError, EOFError):
        pass

    return None

def decode_key(key_data):
    funcs = {
        "SSH": decode_ssh,
        "PEM": decode_pem,
        "DER": decode_der
    }

    k = identify_key(key_data)

    if not k:
        return None

    return funcs[k](key_data)
