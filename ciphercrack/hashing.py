
#Get type of hash
def check_hashes(ciphertext):
    md5_regex = "^[0-9a-f]{32}$"
    sha1_regex = "^[0-9a-f]{40}"
    lens = [32, 40]
    cipher_len = len(ciphertext)

    if cipher_len in lens:
        if re.match(md5_regex, ciphertext):
            return "MD5"
        elif re.match(sha1_regex, ciphertext):
            return "SHA1"
    return None
