
import classic.vigenere

PAD = 'Z'

def encrypt(plaintext, key_col, key_vigenere):
    '''
    For encrypting plaintext with Super Encryption (Vigenere Standard + Transposition)
    '''
    #padding dulu sama special character di akhir if len(plaintext) is not divisible by k
    while(len(plaintext) % key_col != 0):
      plaintext += PAD
    temp_ciphertext = classic.vigenere.encrypt(plaintext, key_vigenere)
    table_transposition = [temp_ciphertext[i:i+key_col] for i in range(0,len(plaintext),key_col)]
    ciphertext = ""
    for i in range(len(table_transposition)):
      for j in range(key_col):
        ciphertext += table_transposition[i][j]
    return ciphertext

def decrypt(ciphertext, key_col, key_vigenere):
    '''
    For decrypting plaintext with Super Encryption (Vigenere Standard + Transposition)
    '''
    col = len(ciphertext) // key_col
    table_transposition = [ciphertext[i:i+col] for i in range(0,len(ciphertext),col)]
    temp_plaintext = ""
    for i in range(len(table_transposition)):
      for j in range(col):
        temp_plaintext += table_transposition[i][j]
    plaintext = classic.vigenere.decrypt(temp_plaintext, key_vigenere)
    return plaintext


if __name__ == '__main__':
  plaintext = "HAINAMASAYAUPININIADIKSAYAIPIN"
  key = 5
  key_vigenere = "meimei"
  ciphertext = encrypt(plaintext, key, key_vigenere)
  print(ciphertext)
  print(decrypt(ciphertext, key, key_vigenere))
