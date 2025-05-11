alpha="abcdefghijklmnopqrstuvwxyz"

def encrypt(cleartext):
    cyphertext=""
    for char in cleartext:
        if char in alpha:
            newpos=(alpha.find(char)+13)%26
            cyphertext+=alpha[newpos]
        else:
            cyphertext+=char
    return cyphertext

cleartext=input("Cleartext: ")
cleartext=cleartext.lower()
print(encrypt(cleartext))
