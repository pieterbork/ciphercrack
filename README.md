# ciphercrack
A project to detect and crack ciphers

Eventually, I want this project to be capable of detecting and cracking all common hashes, encoding, and ciphers.

Inspiration for adding encoding came from (here)[https://github.com/UltimateHackers/Decodify/blob/master/README.md]

### Encoding

Currently, ciphercrack can decode binary, hex, base64, and decimal strings. Hex/Decimal encoding detection needs a bit of work still.

### Vigenere

ciphercrack can solve Vigenere ciphers using the Kasiski/Babbage method. 

Wikipedia has a decent definition (here)[https://en.wikipedia.org/wiki/Kasiski_examination]

The important thing to note here is that the string must be long enough to have repeats or this method will not be able to find a solution.

If you want to just test simple encryption and decryption with vigenere, you can do this:
```python
>>> from ciphercrack.vigenere import encrypt, decrypt
>>> encrypt("helloworld", "secret")
'ZINCSPGVNU'
>>> decrypt("ZINCSPGVNU", "secret")
'HELLOWORLD'
```

For vigenere, all spaces will be removed and encryption/decryption will be all uppercase.

### Caesar

Vigenere is just a Caesar cipher for each letter, so it ciphercrack can by default do Caesar ciphers as well.

```python
>>> from ciphercrack.vigenere import encrypt
#Rot 1:
>>> encrypt("test", "b")
'UFTU'
#Rot 25:
>>> encrypt("test", "z")
'SDRS'
```

## Examples
```python
$ python examples/encoding_example.py
Decoded base64 string to b'%30%78%37%30%36%39%36%35%37%34%36%35%37%32%36%32%36%66%37%32%36%62'
Decoded url string to 0x706965746572626f726b
Decoded hex string to pieterbork
There you have it!  
```

```python
$ python
>>> from ciphertext.vigenere import encrypt
>>> from ciphertext import crack
>>> ciphertext = encrypt("thisisaverysecretstringthatmustbelongenoughtohaveduplicatessothaticancrackthecipherwhichismuchmoredifficultwhenthetextisshort", "secret")
>>> crack(ciphertext)
Found 35 possible keys!
Found 1 possible solutions.                                                                           
Found solution with key SECRET and plaintext THISISAVERYSECRETSTRINGTHATMUSTBELONGENOUGHTOHAVEDUPLICATESSOTHATICANCRACKTHECIPHERWHICHISMUCHMOREDIFFICULTWHENTHETEXTISSHORT                                  
```
