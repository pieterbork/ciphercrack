import crack
import base64
from urllib.parse import quote

og_str = "teamultimate.in"
hex_str = '0x' + ''.join(hex(ord(c))[2:] for c in og_str)
print(hex_str)
url_str = ''.join('%' + hex(ord(c))[2:] for c in hex_str)
print(url_str)
b64_str = base64.b64encode(url_str.encode())
print(b64_str)

crack.main(b64_str)

crack.main()