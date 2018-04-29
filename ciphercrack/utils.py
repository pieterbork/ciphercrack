import re

#Counts how many words from dictionary are contained in a string, returns int.
def count_words(content, words):
    total = 0
    for word in words:
        total += content.count(word.upper())
    return total

#Find all indexes of a string within a string 
#Input "ABCABCABC"; Output [0, 3, 6]
def find_all_indexes(word, ciphertext):
    indexes = [m.start() for m in re.finditer(word, ciphertext)]
    return indexes

#Get all divisors for a number (not including 1 and n)
def get_divisors(n):
    divisors = []
    for i in range(2, n):
        if n % i == 0:
            divisors.append(i)
    return divisors
