from __future__ import division
import re
import six
from collections import Counter

#This script is compatible with Python 2 and 3 using future builtins and the six library
#Known issues: If ciphertext is not long enough or has no repeats, this will error out
#Should probably perform brute force method along with Kasiski-Babbage Method to more accurately guess key length for smaller ciphertexts

english_freq_dict = {"A": 0.08167, "B": 0.01492, "C": 0.02782, "D": 0.04253, "E": 0.12702, "F": 0.02228, "G": 0.02015, "H": 0.06094, "I": 0.06996, "J": 0.00153, "K": 0.00772, "L": 0.04025, "M": 0.02406, "N": 0.06749, "O": 0.07507, "P": 0.01929, "Q": 0.00095, "R": 0.05987, "S": 0.06327, "T": 0.09056, "U": 0.02758, "V": 0.00978, "W": 0.02360, "X": 0.00150, "Y": 0.01974, "Z": 0.00074}
alph = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

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
    key = extend_key(ciphertext, key)

    plaintext = ""
    for idx,c in enumerate(ciphertext):
        og_letter = decrypt_letter(c, key[idx])
        plaintext += og_letter

    return plaintext

#Input plaintext and key, ("PLAINTEXTMESSAGE", "BOY"); Output "BOYBOYBOYBOYBOYB"
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
            indexes = find_all(key, ciphertext)
            gcds = get_diffs(indexes)
            gcd_counter += gcds
    return gcd_counter

#calculates the chi_squared (how close this is to english), given a coset
def calc_chi_2(content):
    total_len = len(content)
    total_x2 = 0

    counter = 0
    for k,v in six.iteritems(english_freq_dict):
        f = float(content.count(k)) / float(total_len)
        x2 = (f - float(v))**2 / float(v)
        total_x2 += x2

    return total_x2

#Given all cosets for a ciphertext, use the chi_squared algorithm to find which decryption results with a frequency analysis closest to English.
def get_key(cosets):
    key = ""
    for coset in cosets:
        best_match = 0
        smallest_chi = 100
        for letter in alph:
            decrypted_coset = decrypt(coset, letter)
            chi_2 = calc_chi_2(decrypted_coset)
            if chi_2 < smallest_chi:
                best_match = letter
                smallest_chi = chi_2
        print("Best Match: {}, Smallest Chi: {}".format(best_match, smallest_chi))
        key += best_match
    return key

#Return all cosets to run Caesar rotations on.
def get_cosets(ciphertext, most_likely_length):
    num_cosets = most_likely_length
    total_len = len(ciphertext)
    cosets = []
    
    #If key length is 7, there will be 7 cosets - one for each character.
    for i in range(0, num_cosets):
        coset = ""
        #Uses key length to pick out every nth characters.
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

#Find all indexes of a string within a string 
#Input "ABCABCABC"; Output [0, 3, 6]
def find_all(word, ciphertext):
    indexes = [m.start() for m in re.finditer(word, ciphertext)]
    return indexes

#Get all divisors for a number (not including 1 and n)
def get_divisors(n):
    divisors = []
    for i in range(2, n):
        if n % i == 0:
            divisors.append(i)
    return divisors

#Input Vigenere ciphertext and this function returns the key
def break_cipher(ciphertext):
    freq_dict = get_segment_freqs(ciphertext)
    gcds = get_diff_gcds(freq_dict, ciphertext)
    most_likely_length = gcds.most_common(1)[0][0]
    print("Your key is probably {} characters long".format(most_likely_length))
    
    cosets = get_cosets(ciphertext, most_likely_length)
    key = get_key(cosets)

    return key

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

#This function answers both questions here https://ecen5033.org/static/5033-w18-hw2.pdf
def main():
    content = "DFSAWSXSOJSBMJUVYAUETUWWPDRUTHOOBSWUSWSQMHVSMQRVJFQOCHGFNAOYLGRUWIYLRKISJCHWVOQYZIXYJFXADVKJSMNDPCFRUOYIITOLTHWDPFYRHRVSOFWBMKJGUMRYKDCHDWVLDHCYJEEEOHLOCQJBAAUSKPQIWVXYBHIGHVTPAYEKIZOTFFHRTFCZLGZVSGUCLIJBBXHKMTIOLPUICBHYOWSMBFCZXWRTDYNWWZOWHQRVDBHCZQWVDILTWCJVQBLVHRUOWZQJZESHELECJHSODXRJBNPJVZUMUFWLVOHCNDXZPBUYGRFOFYAXHZBHCZQQFESLYFVPQHIRUEGIMCYWIITSWEVXYFRCDFMGMWHPVSWNONSHQRUWWDFSDQINPUWTJSHNHEEESFPFXIJQUWHRXJBYPUMEHAIOHVEDFSAWSXSOJSBMJISUGLPPCOMPGSENONSHQRUWWLOXYFCLJDRUDCGAXXVSGWTHRTFDLLFXZDSWCBTKPULLSLZDOFRRVZUVGDDVVESMTJRVEOLZXRUDCGAXXRUWIYDPYBFXYHWJBGMFPTKJCHDPEBJBADXGYBZAZUMKIAMSDVUUCVCHEBJBJCDGKJQYMBEEZOXGHVJBFSTWMJUVYZUIKJQUWOCGPGMTEPVUCVCHEBTIWSDWPTHYXEYKJHCDLRWFOMTEPVUCXZVSSZOHJNRFXBJCDGKJQUWPIROGWCBTKPZIRBVVMONPGXVDVHZOSXZVUDUEZTSXLQYDCSLZIPVHOFTVWLFGNSHICFQNCRRZDTLZQXZFFZZXRUBHCZQARTWHGRPMFRCYDGRTSCYWLVVBCEHHJUONPVAYJQBBXIJUWIYHHNISNSHVIFEOTUMEHGODSITUSXNUMDJBUWVXFQFIGLHVUVYTUHVDFSAWMFOYYJVXFMOQPQJFSQYXHRKJGOYFSETHCEXXZPBUWWLVFTZLUKLFRNSDXKIWMTVEMJCFLWMFOCZEKIIJUBERJEPHVPLRXGCLNHHKPWHNUMDJBUEHSEFGYWIEJHWPPQMEUVYQLJKIOGPQHD"

    print("Ciphertext: {}".format(content))

    key = break_cipher(content)
    print("Key: {}".format(key))

    plaintext = decrypt(content, key)
    print("Plaintext: {}".format(plaintext))

    #English letter frequency population variance
    norm_vals = [val*100 for val in six.viewvalues(english_freq_dict)]
    pop_var = population_variance(norm_vals)
    print("English Dictionary Population Variance is: {}".format(pop_var))

    #Plaintext population variance
    content = "ethicslawanduniversitypoliciestodefendasystemyouneedtobeabletothinklikeanattackerandthatincludesunderstandingtechniquesthatcanbeusedtocompromisesecurityhoweverusingthosetechniquesintherealworldmayviolatethelawortheuniversitysrulesanditmaybeunethicalundersomecircumstancesevenprobingforweaknessesmayresultinseverepenaltiesuptoandincludingexpulsioncivilfinesandjailtimeourpolicyineecsisthatyoumustrespecttheprivacyandpropertyrightsofothersatalltimesorelseyouwillfailthecourseactinglawfullyandethicallyisyourresponsibilitycarefullyreadthecomputerfraudandabuseactcfaaafederalstatutethatbroadlycriminalizescomputerintrusionthisisoneofseverallawsthatgovernhackingunderstandwhatthelawprohibitsyoudontwanttoenduplikethisguyifindoubtwecanreferyoutoanattorneypleasereviewitsspoliciesonresponsibleuseoftechnologyresourcesandcaenspolicydocumentsforguidelinesconcerningproperuseofinformationtechnologyatumaswellastheengineeringhonorcodeasmembersoftheuniversitycommunityyouarerequiredtoabideby"
    pop_var = get_letter_freq_population_variance(content)
    print("Plaintext Population Variance is: {}".format(pop_var))
    
    #For these keys, determine ciphertext and coset population variance
    keys = ["yz", "xyz", "wxyz", "vwxyz", "uvwxyz"]
    for key in keys:
        print("Key is: {}".format(key))
        ciphertext = encrypt(content, key)
        pop_var = get_letter_freq_population_variance(ciphertext)
        print("Ciphertext Population Variance is: {}".format(pop_var))

        cosets = get_cosets(ciphertext, len(key))
        total_coset_pop_var = 0
        for coset in cosets:
            coset_pop_var = get_letter_freq_population_variance(coset)
            print("Coset Population Variance is: {}".format(coset_pop_var))
            total_coset_pop_var += coset_pop_var
        print("Total Coset Population Variance is {}".format(total_coset_pop_var/len(cosets)))

    #Show that brute forcing the key length provides obvious results
    key = keys[-1]
    ciphertext = encrypt(content, key)
    print("Brute force method to get key length")
    for i in range(2, len(key)+1):
        cosets = get_cosets(ciphertext, i)
        total_coset_pop_var = 0
        for coset in cosets:
            coset_pop_var = get_letter_freq_population_variance(coset)
            total_coset_pop_var += coset_pop_var
        print("Key Length: {}, Coset Mean Population Variance: {}".format(i, total_coset_pop_var/len(cosets)))

if __name__ == "__main__":
    main()
