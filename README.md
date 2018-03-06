# ciphercrack
A project to detect and crack ciphers

Eventually, I want this project to be capable of detecting and cracking common hashes, encoding, and ciphers

### Vigenere

Right now, `crack.py` is only capable of solving Vigenere ciphers.

```python
$ python
>>> import crack
>>> ciphertext = crack.encrypt("thisisaverysecretstringthatmustbelongenoughtohaveduplicatessothaticancrackthecipherwhichismuchmoredifficultwhenthetextisshort", "secret")
>>> crack.main(ciphertext)
Found 35 possible keys!
Found 1 possible solutions.                                                                           
Found solution with key SECRET and plaintext THISISAVERYSECRETSTRINGTHATMUSTBELONGENOUGHTOHAVEDUPLICATESSOTHATICANCRACKTHECIPHERWHICHISMUCHMOREDIFFICULTWHENTHETEXTISSHORT                                  
Found 11 dictionary words in content, with a population variance of 13.047100591715978
```
