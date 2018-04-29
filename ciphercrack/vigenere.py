from ciphercrack.languages import english_dict, english_freq_dict, english_alph
from ciphercrack.utils import count_words, find_all_indexes, get_divisors
from collections import Counter
import six, re

#Making it easy to switch to other latin alphabet languages in the future
language_freq_dict = english_freq_dict
alph = english_alph

#This will include letters for the key within a certain value of the lowest chi squared.
#Increasing this will find more accurate results, but will also increase runtime.
CHI_THRESHOLD = 2

#How many words must be detected in a string to validate it as a possible solution?
WORD_THRESHOLD = 5

#Encrypts a letter for Vigenere cipher
def encrypt_letter(letter, key):
    idx = alph.index(letter)
    key_idx = alph.index(key)
    new_alph = alph[idx:] + alph[:idx]
    new_letter = new_alph[key_idx]
    return new_letter

#Decrypts a letter for Vigenere cipher
def decrypt_letter(letter, key):
    key_idx = alph.index(key)
    key_alph = alph[key_idx:] + alph[:key_idx]
    og_idx = key_alph.index(letter)
    og_letter = alph[og_idx]
    return og_letter

#Input plaintext and key, output ciphertext
def encrypt(plaintext, key):
    plaintext = plaintext.replace(' ', '').upper()
    plain_len = len(plaintext)

    key = extend_key(plaintext, key).upper()

    ciphertext = ""
    for idx,c in enumerate(plaintext):
        new_letter = encrypt_letter(c, key[idx])
        ciphertext += new_letter

    return ciphertext

#Input ciphertext and key, output plaintext
def decrypt(ciphertext, key):
    key = extend_key(ciphertext, key).upper()

    plaintext = ""
    for idx,c in enumerate(ciphertext):
        og_letter = decrypt_letter(c, key[idx])
        plaintext += og_letter

    return plaintext

#Extends key to length of text; Input plaintext and key, ("PLAINTEXTMESSAGE", "BOY"); Output "BOYBOYBOYBOYBOYB"
def extend_key(text, key):
    text_len = len(text)
    while(len(key) < text_len):
        key += key
    return key[:text_len]

#Builds a dictionary of segments with 3+ characters
#If I give ABCABC
#Returns {"ABC": 2, "ABCA": 1, "ABCAB": 1, "ABCABC": 1, "BCA": 1, "BCAB": 1, "BCABC": 1, "CAB": 1, "CABC": 1}
def get_segment_freqs(ciphertext):
    segment_list = []
    total_len = len(ciphertext)
    for h in range(0, total_len -3):
        for i in range(h+3, total_len):
            word = ciphertext[h:i]
            segment_list.append(word)

    freq_dict = dict(Counter(segment_list))
    return freq_dict

#If a segment occurs more than once in ciphertext, get the GCDs of the differences
def get_diff_gcds(freq_dict, ciphertext):
    gcd_counter = Counter()
    for key,count in six.iteritems(freq_dict):
        if count > 1:
            indexes = find_all_indexes(key, ciphertext)
            gcds = get_diffs(indexes)
            gcd_counter += gcds
    return gcd_counter

#calculates the chi_squared (how close this is to english), given a coset
def calc_chi_2(content):
    total_len = len(content)
    total_x2 = 0

    counter = 0
    for k,v in six.iteritems(language_freq_dict):
        f = float(content.count(k)) / float(total_len)
        x2 = (f - float(v))**2 / float(v)
        total_x2 += x2

    return total_x2

#Given all cosets for a ciphertext, use the chi_squared algorithm to find which decryption results with a frequency analysis closest to English. (Uses CHI_THRESHOLD to include all chi values within a range of lowest chi squared)
def get_key(cosets):
    keys = [""]
    for coset in cosets:
        chis = {}
        for letter in alph:
            decrypted_coset = decrypt(coset, letter)
            chi_2 = calc_chi_2(decrypted_coset)
            chis[letter] = chi_2
        smallest_chi = min(chis.values())
        matches = [letter for letter,chi in six.iteritems(chis) if abs(chi - smallest_chi) < CHI_THRESHOLD]
        new_keys = keys
        keys = []
        for match in matches:
            keys.extend([key + match for key in new_keys])

    return keys

#Return all cosets to run Caesar rotations on.
def get_cosets(ciphertext, most_likely_length):
    num_cosets = most_likely_length
    total_len = len(ciphertext)
    cosets = []

    #If key length is n, there will be n cosets - one for each character.
    for i in range(0, num_cosets):
        coset = ""
        #Uses key length to pick out every nth character.
        for j in range(i, total_len, num_cosets):
            coset += ciphertext[j]
        cosets.append(coset)
    return cosets

#Takes differences between segment indexes and returns a counter of GCDs.
#The most popular GCD is most likely the key length
def get_diffs(indexes):
    diffs = []
    for i in range(0, len(indexes)-1, 2):
        diff = indexes[i+1] - indexes[i]
        divs = get_divisors(diff)
        diffs.extend(divs)
    return Counter(diffs)

#Calculated the population variance given a list of values
def population_variance(vals):
    pop_var = float(0)
    mean = float(sum(vals)/len(vals))
    for v in vals:
        pop_var += (float(v) - mean)**2
    return pop_var/len(vals)

#Returns a dictionary with the frequency of letters given a string
def get_letter_freqs(text):
    freq_dict = {}
    normalized = text.upper()
    total_len = len(text)
    for letter in alph:
        freq_dict[letter] = float(normalized.count(letter))/float(total_len)
    return freq_dict

#Given a string, get letter frequencies, normalize, and calculate population variance.
def get_letter_freq_population_variance(text):
    freq_dict = get_letter_freqs(text)
    norm_vals = [val*100 for val in six.viewvalues(freq_dict)]
    pop_var = population_variance(norm_vals)
    return pop_var

#Given a list of GCDs, this will find the divisors that do not have any smaller divisors in the list.
def get_most_likely_divisors(gcds):
    largest_count = max(gcds.values())
    best_counts = [num for num,count in six.iteritems(gcds) if abs(largest_count - count) <= 1]

    best_counts = sorted(best_counts, reverse=True)
    most_likely = []

    for candidate in best_counts:
        if candidate < 10 or (not any((candidate % divisor == 0) and candidate != divisor for divisor in best_counts)):
            most_likely.append(candidate)

    return most_likely

#Input Vigenere ciphertext and this function returns the key
def break_cipher(ciphertext, key_len=None):
    if not key_len:
        freq_dict = get_segment_freqs(ciphertext)
        gcds = get_diff_gcds(freq_dict, ciphertext)
        #print("GCDs {}".format(gcds))
        if not gcds:
            return []
        most_likely_length = get_most_likely_divisors(gcds)
    else:
        most_likely_length = [key_len]
    keys = []
    for length in most_likely_length:
        #print("Testing length {}".format(length))
        cosets = get_cosets(ciphertext, length)
        keys.extend(get_key(cosets))
        # key = get_key(cosets)
        # keys.append(key)

        return keys

def get_solution(ciphertext, keys):
    #English letter frequency population variance
    norm_vals = [val*100 for val in six.viewvalues(language_freq_dict)]
    english_pop_var = population_variance(norm_vals)
    solutions = {}
    best_sol = {}
    if keys:
        for key in keys:
            #print("Key is possibly: {}".format(key))
            plaintext = decrypt(ciphertext, key)
            pop_var = get_letter_freq_population_variance(plaintext)
            #diff_pop_var = abs(english_pop_var - pop_var)
            num_words = count_words(plaintext, english_dict)

            if num_words > WORD_THRESHOLD:
                solutions[key] = {"key": key, "pop_var":pop_var, "plaintext":plaintext, "num_words":num_words}

    if solutions:
        best_sol_count = 0
        print("Found {} possible solutions.".format(len(solutions)))
        for key, sol_dict in six.iteritems(solutions):
            if sol_dict["num_words"] > best_sol_count:
                best_sol = sol_dict
                best_sol_count = sol_dict["num_words"]

    return best_sol

def vigenere_crack(ciphertext, key_len=None):
    ciphertext = ciphertext.replace(' ', '').upper()

    #print("English Dictionary Population Variance is: {}".format(english_pop_var))

    keys = break_cipher(ciphertext, key_len)
    print("Found {} possible keys!".format(len(keys)))

    solution = get_solution(ciphertext, keys)
    return solution
