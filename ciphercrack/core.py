import re
import six

from .languages import english_freq_dict, english_alph, english_dict
from .vigenere import vigenere_crack
from . import encoding
from . import hashing

#This script is compatible with Python 2 and 3 using the six library
#Known issues: If ciphertext is not long enough or has no repeats, this will error out
def crack(ciphertext, key_len=None):
    hash_type = hashing.check_hashes(ciphertext)
    if hash_type:
        print("This is a {} hash".format(hash_type))
        return hash_type

    # print("Ciphertext: {}".format(content))
    decoded = encoding.check_encoding(ciphertext)
    if decoded != ciphertext:
        print("Final decoded string: {}".format(decoded))
        return decoded

    solution = vigenere_crack(ciphertext)
    if solution:
        key = solution["key"]
        plaintext = solution["plaintext"]
        if len(set(key)) == 1:
            print("This was a Caesar Cipher, equivalent of Rot {}".format(english_alph.index(key[0])))
            key=key[0]
        print("Found solution with key {} and plaintext {}".format(key, plaintext))
        return plaintext
    else:
        print("Could not find any solutions")


if __name__ == "__main__":
    main()
