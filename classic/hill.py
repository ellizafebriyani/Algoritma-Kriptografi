import math

ALPHABET_SIZE = 26

def inverse(m, mod=ALPHABET_SIZE):
    '''
    Find the inverse of m in modulo mod
    '''
    if(math.gcd(m, mod) > 1):
        #can't find inverse
        return -1
        pass
    m = m % mod
    if m == 1:
        return m
    return mod - inverse(mod, m)*mod//m

def multiply_matrix(r, s, mod=ALPHABET_SIZE):
  '''
  r is an 3x3 matrix, s is an 3x1 matrix, returns their multiplication
  '''
  product = []
  for i in range(len(r)):
    temp = []
    for j in range(len(s[0])):
      cur = 0
      for k in range(len(r[0])):
        cur += r[i][k] * s[k][j]
      temp.append(cur)
    product.append(temp)
  return product

def transpose_matrix(r, size=3):
  '''
  r is an 3x3 matrix, returns the transpose of r
  '''
  r_transpose = [[0 for i in range(size)] for j in range(size)]
  for i in range(size):
    for j in range(size):
      r_transpose[i][j] = r[j][i]
  return r_transpose

def determinant_matrix(r):
  '''
  r is an 3x3 matrix, returns the determinant of r
  '''
  determinant = 0
  for i in range(3):
    j = (i + 1) % 3
    k = (i + 2) % 3
    determinant += r[0][i] * (r[1][j] * r[2][k] - r[1][k] * r[2][j])
  return determinant

def cofactor_matrix(r, size=3):
  '''
  r is an 3x3 matrix, returns the determinant of r
  '''
  r_cofactor = [[0 for i in range(size)] for j in range(size)]
  for i in range(size):
    for j in range(size):
      i_1 = (i + 1) % 3
      i_2 = (i + 2) % 3
      j_1 = (j + 1) % 3
      j_2 = (j + 2) % 3
      r_cofactor[i][j] = r[i_1][j_1] * r[i_2][j_2] - r[i_1][j_2] * r[i_2][j_1]
  return r_cofactor

def inverse_matrix(r, mod=ALPHABET_SIZE):
  '''
  r is an 3x3 matrix, returns the inverse of r in modulo 26
  '''
  determinant = determinant_matrix(r)
  assert(math.gcd(determinant, mod) == 1)
  inv_determinant = inverse(determinant)
  inverse_r = transpose_matrix(cofactor_matrix(r))
  for i in range(3):
    for j in range(3):
      inverse_r[i][j] = inverse_r[i][j] * inv_determinant % mod
  return inverse_r

def reduce_matrix(r, mod=ALPHABET_SIZE):
  '''
  returns r with all of its elements are reduced by modulo mod
  '''
  r_mod = r
  for i in range(len(r_mod)):
    for j in range(len(r_mod[0])):
      r_mod[i][j] = r[i][j] % mod;
  return r_mod

def encrypt(plaintext, K, mod=ALPHABET_SIZE, size=3):
  '''
  For encrypting plaintext with Hill Cipher
  '''
  PAD = 'Z'
  while len(plaintext) % 3 != 0:
    plaintext += PAD
  ciphertext = ""
  for i in range(0, len(plaintext), size):
    get_slice_matrix = [[ord(plaintext[i + j]) - ord('A')] for j in range(size)]
    get_slice_cipher = reduce_matrix(multiply_matrix(K, get_slice_matrix))
    slice_cipher = [chr(get_slice_cipher[j][0] + ord('A')) for j in range(size)]
    # print(slice_cipher)
    slice_cipher_string = ''.join(slice_cipher)
    ciphertext = ''.join([ciphertext, slice_cipher_string])
  return ciphertext

def decrypt(ciphertext, K, mod=ALPHABET_SIZE, size=3):
  '''
  For decrypting plaintext with Hill Cipher
  '''
  inverse_K = inverse_matrix(K)
  plaintext = encrypt(ciphertext, inverse_K)
  return plaintext


if __name__ == '__main__':
  '''
  For testing purposes
  '''

  #Testing inverse -- done
  for i in range(26):
    if math.gcd(i, 26) == 1:
      print(i, inverse(i))


  #Testing matrix multiplication -- done
  s = [[1],[2],[3]]
  r = [[1,1,1],[2,0,1],[1,0,2]]
  print(multiply_matrix(r, s))
  print(transpose_matrix(r))
  print(determinant_matrix(r))
  print(cofactor_matrix(r))
  print(inverse_matrix(r))
  print(multiply_matrix(r, inverse_matrix(r)))

  #testing cipher -- done
  plaintext = "hainamasayaojan"
  print(encrypt(plaintext, r))
  ciphertext = "pwxzmlsaamkawfj"
  print(decrypt(ciphertext, r))
