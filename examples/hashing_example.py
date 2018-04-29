from ciphercrack import crack

#test
md5 = "d8e8fca2dc0f896fd7cb4cb0031ba249"
sha1 = "4e1243bd22c66e76c2ba9eddc1f91394e57f9f83"
sha256 = "f2ca1bb6c7e907d06dafe4687e579fce76b37e4e93b7605022da52e6ccc26fd2"
sha512 = "0e3e75234abc68f4378a86b3f4b32a198ba301845b0cd6e50106e874345700cc6663a86c1ea125dc5e92be17c98f9a0f85ca9d5f595db2012f7cc3571945c123"
sha256crypt = "$5$Pc5N.PsVpjYONHS$Q.9eVY6SKZKW0CnyKF1gtRea2OlV/ofaky6VP6rGzoB"
sha512crypt = "$6$QCS9yH9vf8pS3/Q$LoFNNOmYzV.FFgBBfiAiVwEB3.xGi7GUdm/1bxExxjiGUol0oEl4bY9XqQibrctZnL8OfSL3ycuW6uIxNHepF/"

crack(md5)
crack(sha1)
crack(sha256)
crack(sha512)
crack(sha256crypt)
crack(sha512crypt)
