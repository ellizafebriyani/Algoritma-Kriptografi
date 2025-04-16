def blockify(text):
    '''
    Return blocked text in 5 letters each
    '''
    blocked_text = ""
    for i in range(len(text)):
        blocked_text += text[i]

        if i % 5 == 4:
            blocked_text += ' '
    
    return blocked_text

def alphabetify(text):
    '''
    Return text with only capitalized alphabet
    '''
    return ''.join(c for c in text if c.isalpha()).upper()