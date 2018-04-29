import re
import base64
from urllib.parse import unquote


def binary_encode(string):
    return ''.join(format(ord(x), 'b') for x in st)

def binary_decode(string):
    return ''.join(chr(int(string[i*8:i*8+8], 2)) for i in range(len(string)//8))

def hex_encode(string):
    return '0x' + ''.join(hex(ord(c))[2:] for c in string)

def hex_decode(string):
    return bytes.fromhex(string.replace('0x', '')).decode('utf-8')

def url_encode(string):
    return ''.join('%' + hex(ord(c))[2:] for c in string)

def url_decode(string):
    return unquote(string)

def b64_encode(string):
    return base64.b64encode(string)

def b64_decode(string):
    return base64.b64decode(string)

def decimal_encode(string):
    return ' '.join(ord(c) for c in string)

def decimal_decode(string):
    return ''.join(chr(int(c)) for c in string.split())

def decode(string, encode_type):
    if encode_type == "hex":
        return hex_decode(string)
    elif encode_type == "binary":
        return binary_decode(string)
    elif encode_type == "url":
        return url_decode(string)
    elif encode_type == "base64":
        return b64_decode(string)
    elif encode_type == "decimal":
        return decimal_decode(string)
    else:
        print("WHAT IS THIS {}".format(encode_type))
        return

def detect_encoding(string):
    base64_regex = "^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{4}|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)$"
    binary_regex = "^(1(01*0)*1|0)+$"
    hex_regex = "^0[xX][0-9a-fA-F]+$"
    decimal_regex = "^([0-9]{2,3}.?)+$"
    url_regex = "^(%..%..)+$"

    if re.match(hex_regex, string):
        return "hex"
    elif re.match(binary_regex, string):
        return "binary"
    elif re.match(url_regex, string):
        return "url"
    elif re.match(base64_regex, string):
        return "base64"
    elif re.match(decimal_regex, string):
        return "decimal"
    else:
        return None

def check_encoding(string):
    if type(string) == bytes:
        string = string.decode()

    encode_type = detect_encoding(string)
    if encode_type:
        decoded = decode(string, encode_type)
        print("Decoded {} string to {}".format(encode_type, decoded))
    else:
        return string

    return check_encoding(decoded)
