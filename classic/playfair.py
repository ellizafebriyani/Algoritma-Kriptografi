def generate_matrix(key):
    '''
    Generating matrix for playfair
    '''
    mat = []
    
    # Replace J and duplicates
    keyword = key.replace('J', '')
    keyword = "".join(dict.fromkeys(keyword))

    # Append the rest of alphabet except J
    for i in range(26):
        if i == 9:
            continue
        c_val = chr(i + ord('A'))
        if c_val not in keyword:
            keyword += c_val
    
    row = []
    for i in range(25):
        row.append(keyword[i])
        if i % 5 == 4:
            mat.append(row)
            row = []
    
    return mat


def find_coord(c, matrix):
    '''
    Finding coordinate of character c in matrix
    '''
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == c:
                return i, j
    return -1, -1

def find_enc_pair(bigram, mat):
    '''
    Finding encrypted pair of a bigram
    '''
    c1 = bigram[0]
    c2 = bigram[1]
    row1, col1 = find_coord(c1, mat)
    row2, col2 = find_coord(c2, mat)

    if row1 == row2:
        return mat[row1][(col1 + 1) % 5] + mat[row2][(col2 + 1) % 5]
    elif col1 == col2:
        return mat[(row1 + 1) % 5][col1] + mat[(row2 + 1) % 5][col2]
    else:
        return mat[row1][col2] + mat[row2][col1]

def find_dec_pair(bigram, mat):
    '''
    Finding decrypted pair of a bigram
    '''
    c1 = bigram[0]
    c2 = bigram[1]
    row1, col1 = find_coord(c1, mat)
    row2, col2 = find_coord(c2, mat)

    if row1 == row2:
        return mat[row1][(col1 - 1) % 5] + mat[row2][(col2 - 1) % 5]
    elif col1 == col2:
        return mat[(row1 - 1) % 5][col1] + mat[(row2 - 1) % 5][col2]
    else:
        return mat[row1][col2] + mat[row2][col1]


def encrypt(plaintext, key):
    '''
    For encrypting plaintext with Playfair Cipher
    '''
    plaintext = plaintext.replace("J", "")
    mat = generate_matrix(key)
    ciphertext = ""

    bigram = ""
    i = 0
    while i < len(plaintext):
        bigram += plaintext[i]
        i += 1

        if i >= len(plaintext):
            bigram += 'X'

        if len(bigram) < 2:
            if plaintext[i] == plaintext[i-1]:
                bigram += 'X'
            else:
                bigram += plaintext[i]
                i += 1
        
        ciphertext += find_enc_pair(bigram, mat)
        bigram = ""

    return ciphertext



def decrypt(ciphertext, key):
    '''
    For decrypting plaintext with Playfair cipher
    '''
    mat = generate_matrix(key)
    plaintext = ""

    bigram = ""
    i = 0
    for i in range(0, len(ciphertext), 2):
        bigram += ciphertext[i] + ciphertext[i+1]
        
        plaintext += find_dec_pair(bigram, mat)
        bigram = ""
    
    return plaintext
