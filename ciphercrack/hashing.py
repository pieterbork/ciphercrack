import re

#Get type of hash
def check_hashes(ciphertext):
    cipher_len = len(ciphertext)

    md5_regex = "^\w{32}$"
    sha1_regex = "^\w{40}$"
    sha256_regex = "^\w{64}$"
    sha512_regex = "^\w{128}$"
    lens = [32, 40, 64, 128]

    sha256crypt_regex = "^\$5\$.{0,16}\$.{43}$"
    sha512crypt_regex = "^\$6\$.{0,16}\$.{86}$"
    crypt_prefixes = ["$5", "$6"]

    if cipher_len in lens:
        if re.match(md5_regex, ciphertext):
            return "MD5"
        elif re.match(sha1_regex, ciphertext):
            return "SHA1"
        elif re.match(sha256_regex, ciphertext):
            return "SHA256"
        elif re.match(sha512_regex, ciphertext):
            return "SHA512"
    elif ciphertext[0:2] in crypt_prefixes:
        if re.match(sha256crypt_regex, ciphertext):
            return "SHA256Crypt"
        elif re.match(sha512crypt_regex, ciphertext):
            return "SHA512Crypt"

    return None
