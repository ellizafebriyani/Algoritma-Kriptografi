import math

ALPHABET_SIZE = 26

def inverse(m, mod=ALPHABET_SIZE):
    '''
    Find the inverse of m in modulo mod
    '''
    if(math.gcd(m, mod) > 1):
        #can't find inverse
        return -1
    m = m % mod
    if m == 1:
        return m
    return mod - inverse(mod, m)*mod//m

def multiply_matrix(r, s, mod=ALPHABET_SIZE):
    '''
    r is a matrix, s is a matrix, returns their multiplication
    '''
    product = []
    for i in range(len(r)):
        temp = []
        for j in range(len(s[0])):
            cur = 0
            for k in range(len(r[0])):
                cur += r[i][k] * s[k][j]
            temp.append(cur % mod)
        product.append(temp)
    return product

def transpose_matrix(r, size):
    '''
    r is a matrix, returns the transpose of r
    '''
    r_transpose = [[0 for i in range(size)] for j in range(size)]
    for i in range(size):
        for j in range(size):
            r_transpose[i][j] = r[j][i]
    return r_transpose

def determinant_matrix(r, size=3):
    '''
    r is a matrix, returns the determinant of r
    '''
    if size == 2:
        return r[0][0] * r[1][1] - r[0][1] * r[1][0]
    elif size == 3:
        determinant = 0
        for i in range(3):
            j = (i + 1) % 3
            k = (i + 2) % 3
            determinant += r[0][i] * (r[1][j] * r[2][k] - r[1][k] * r[2][j])
        return determinant
    return 0

def cofactor_matrix(r, size):
    '''
    r is a matrix, returns the cofactor matrix of r
    '''
    r_cofactor = [[0 for i in range(size)] for j in range(size)]
    
    if size == 2:
        r_cofactor[0][0] = r[1][1]
        r_cofactor[0][1] = -r[1][0]
        r_cofactor[1][0] = -r[0][1]
        r_cofactor[1][1] = r[0][0]
    elif size == 3:
        for i in range(size):
            for j in range(size):
                i_1 = (i + 1) % 3
                i_2 = (i + 2) % 3
                j_1 = (j + 1) % 3
                j_2 = (j + 2) % 3
                r_cofactor[i][j] = r[i_1][j_1] * r[i_2][j_2] - r[i_1][j_2] * r[i_2][j_1]
    
    return r_cofactor

def inverse_matrix(r, size, mod=ALPHABET_SIZE):
    '''
    r is a matrix, returns the inverse of r in modulo 26
    '''
    determinant = determinant_matrix(r, size)
    determinant = determinant % mod
    
    # Check if matrix has inverse in modulo arithmetic
    if math.gcd(determinant, mod) != 1:
        return None
    
    inv_determinant = inverse(determinant)
    if inv_determinant == -1:
        return None
        
    inverse_r = transpose_matrix(cofactor_matrix(r, size), size)
    for i in range(size):
        for j in range(size):
            inverse_r[i][j] = (inverse_r[i][j] * inv_determinant) % mod
    return inverse_r

def reduce_matrix(r, mod=ALPHABET_SIZE):
    '''
    returns r with all of its elements are reduced by modulo mod
    '''
    r_mod = []
    for i in range(len(r)):
        r_mod.append([])
        for j in range(len(r[0])):
            r_mod[i].append(r[i][j] % mod)
    return r_mod

def encrypt(plaintext, K, mod=ALPHABET_SIZE, size=3):
    '''
    For encrypting plaintext with Hill Cipher
    '''
    PAD = 'Z'
    while len(plaintext) % size != 0:
        plaintext += PAD
    ciphertext = ""
    for i in range(0, len(plaintext), size):
        get_slice_matrix = [[ord(plaintext[i + j]) - ord('A')] for j in range(size)]
        get_slice_cipher = reduce_matrix(multiply_matrix(K, get_slice_matrix))
        slice_cipher = [chr(get_slice_cipher[j][0] + ord('A')) for j in range(size)]
        slice_cipher_string = ''.join(slice_cipher)
        ciphertext = ''.join([ciphertext, slice_cipher_string])
    return ciphertext

def decrypt(ciphertext, K, size=3, mod=ALPHABET_SIZE):
    '''
    For decrypting plaintext with Hill Cipher
    '''
    inverse_K = inverse_matrix(K, size)
    if inverse_K is None:
        return "ERROR: Matrix has no inverse in modulo " + str(mod)
    plaintext = encrypt(ciphertext, inverse_K, mod, size)
    return plaintext

def parse_key_matrix(key_values, size):
    '''
    Parse key inputs into a matrix
    Returns None if format is invalid
    '''
    try:
        matrix = []
        for i in range(size):
            row = list(map(int, key_values[i].split(',')))
            if len(row) != size:
                return None
            matrix.append(row)
        return matrix
    except ValueError:
        return None

def is_valid_matrix(matrix, size, mod=ALPHABET_SIZE):
    '''
    Check if matrix is valid for Hill Cipher (has inverse in modulo 26)
    '''
    if not matrix:
        return False
        
    det = determinant_matrix(matrix, size)
    return math.gcd(det % mod, mod) == 1

if __name__ == '__main__':
    '''
    For testing purposes
    '''

    #Testing inverse -- done
    for i in range(26):
        if math.gcd(i, 26) == 1:
            print(i, inverse(i))

    # Testing 2x2 matrix
    r_2x2 = [[5, 8], [17, 3]]
    s_2x2 = [[1], [2]]
    print(multiply_matrix(r_2x2, s_2x2))
    print(transpose_matrix(r_2x2, 2))
    print(determinant_matrix(r_2x2, 2))
    print(cofactor_matrix(r_2x2, 2))
    print(inverse_matrix(r_2x2, 2))
    inv_2x2 = inverse_matrix(r_2x2, 2)
    if inv_2x2:
        print(multiply_matrix(r_2x2, inv_2x2))

    #Testing 3x3 matrix multiplication -- done
    s = [[1],[2],[3]]
    r = [[1,1,1],[2,0,1],[1,0,2]]
    print(multiply_matrix(r, s))
    print(transpose_matrix(r, 3))
    print(determinant_matrix(r, 3))
    print(cofactor_matrix(r, 3))
    print(inverse_matrix(r, 3))
    inv_3x3 = inverse_matrix(r, 3)
    if inv_3x3:
        print(multiply_matrix(r, inv_3x3))

    #testing cipher -- done
    plaintext = "hainamasayaojan"
    print(encrypt(plaintext, r))
    ciphertext = "pwxzmlsaamkawfj"
    print(decrypt(ciphertext, r))
    
    # Testing 2x2 cipher
    plaintext_2x2 = "test"
    print(encrypt(plaintext_2x2, r_2x2, size=2))
    ciphertext_2x2 = "GSWB"  # Example output
    print(decrypt(ciphertext_2x2, r_2x2, 2))