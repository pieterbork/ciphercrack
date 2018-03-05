# ciphercrack
A project to detect and crack ciphers

Eventually, I want this project to be capable of detecting and cracking common hashes, encoding, and ciphers

### Vigenere

Right now, `crack.py` is only capable of solving Vigenere ciphers.

```python
$ python
>>> import crack
>>> crack.main(crack.encrypt("thisisaverysecretstringthatmustbelongenoughtohaveduplicatessothaticancrackthecipherwhichismuchmoredifficultwhenthetextisshort", "secret"))

Found solution with key SECRET and plaintext THISISAVERYSECRETSTRINGTHATMUSTBELONGENOUGHTOHAVEDUPLICATESSOTHATICANCRACKTHECIPHERWHICHISMUCHMOREDIFFICULTWHENTHETEXTISSHORT
```
