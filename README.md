# ciphercrack
A python3 project to detect and crack ciphers

Inspiration for adding encoding came from [Decodify](https://github.com/UltimateHackers/Decodify/blob/master/README.md)


## How it works

Run this to try it out with a simple flask server
```
git clone https://github.com/pieterbork/ciphercrack.git && cd ciphercrack && pip install -e . && python run.py
```

Here are a few things you can paste in the web server to test deciphering different things:

Multi-encoded string

`JTMwJTc4JTM3JTMwJTM2JTM5JTM2JTM1JTM3JTM0JTM2JTM1JTM3JTMyJTM2JTMyJTM2JTY2JTM3JTMyJTM2JTYy`

Vigenere encrypted string

`LLKJMLSZGICLWGTVXLLVKEKMZEVDYLLFGCSGYIPFYZZXQYEOWHWGPBUEVVWLGXJRXBUEPTVTUOVYIVATJVVPZMEYMLEYEYQHJIFZJYAGWCXPZIPKLXLIZKMLKLQIX`

MD5 Hash

`d8e8fca2dc0f896fd7cb4cb0031ba249`


Encoding

```python
$ python
>>> from ciphercrack import crack
>>> import base64
>>> og_str = "pieterbork"
>>> hex_str = '0x' + ''.join(hex(ord(c))[2:] for c in og_str)
>>> url_str = ''.join('%' + hex(ord(c))[2:] for c in hex_str)
>>> b64_str = base64.b64encode(url_str.encode())
>>> print(b64_str)
b'JTMwJTc4JTM3JTMwJTM2JTM5JTM2JTM1JTM3JTM0JTM2JTM1JTM3JTMyJTM2JTMyJTM2JTY2JTM3JTMyJTM2JTYy'
>>> crack(b64_str)
Decoded base64 string to b'%30%78%37%30%36%39%36%35%37%34%36%35%37%32%36%32%36%66%37%32%36%62'
Decoded url string to 0x706965746572626f726b
Decoded hex string to pieterbork
Final decoded string: pieterbork
```

Vigenere

```python
$ python
>>> from ciphercrack.vigenere import encrypt
>>> from ciphercrack import crack
>>> ciphertext = encrypt("thisisaverysecretstringthatmustbelongenoughtohaveduplicatessothaticancrackthecipherwhichismuchmoredifficultwhenthetextisshort", "secret")
>>> crack(ciphertext)
Found 35 possible keys!
Found 1 possible solutions.                                                                           
Found solution with key SECRET and plaintext THISISAVERYSECRETSTRINGTHATMUSTBELONGENOUGHTOHAVEDUPLICATESSOTHATICANCRACKTHECIPHERWHICHISMUCHMOREDIFFICULTWHENTHETEXTISSHORT                                  
```

Hashing

```python
$ echo "test" | md5sum
d8e8fca2dc0f896fd7cb4cb0031ba249
$ python
>>> from ciphercrack import crack
>>> crack('d8e8fca2dc0f896fd7cb4cb0031ba249')
This is a MD5 hash
```

### Encoding

Currently, ciphercrack can decode binary, hex, base64, and decimal strings. Hex/Decimal encoding detection needs a bit of work still.

### Hashing

This is just simple detection right now, more to come.

### Vigenere

ciphercrack can solve Vigenere ciphers using the Kasiski/Babbage method. 

Wikipedia has a decent definition [here](https://en.wikipedia.org/wiki/Kasiski_examination)

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

Vigenere is just a Caesar cipher for each letter, so ciphercrack can do Caesar ciphers as well.

```python
>>> from ciphercrack.vigenere import encrypt
#Rot 1:
>>> encrypt("test", "b")
'UFTU'
#Rot 25:
>>> encrypt("test", "z")
'SDRS'
```

