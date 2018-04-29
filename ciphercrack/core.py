import re
import six

from ciphercrack.languages import english_freq_dict, english_alph, english_dict
from ciphercrack.vigenere import vigenere_crack
from ciphercrack import encoding
from ciphercrack import hashing

#This script is compatible with Python 2 and 3 using the six library
#Known issues: If ciphertext is not long enough or has no repeats, this will error out
def crack(ciphertext=None, key_len=None):
	if not ciphertext:
		print("No ciphertext provided.")
		return

    # print("Ciphertext: {}".format(content))
	decoded = encoding.check_encoding(ciphertext)
	if decoded != ciphertext:
		print("There you have it!")
		return

	hash_type = hashing.check_hashes(ciphertext)
	if hash_type:
		print("This is a {} hash".format(hash_type))
		return

	vigenere_crack(ciphertext)

if __name__ == "__main__":
	main()
