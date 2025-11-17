def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    keyword_index = 0
    keyword = keyword.upper()

    for char in plaintext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            key_char = keyword[keyword_index]
            shift = ord(key_char) - ord('A')
            shifted_char = chr((ord(char) - base + shift) % 26 + base)
            ciphertext += shifted_char
            keyword_index = (keyword_index + 1) % len(keyword)
        else:
            ciphertext += char
            keyword_index = (keyword_index + 1) % len(keyword)

    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    keyword_index = 0
    keyword = keyword.upper()

    for char in ciphertext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            key_char = keyword[keyword_index]
            shift = ord(key_char) - ord('A')
            shifted_char = chr((ord(char) - base - shift) % 26 + base)
            plaintext += shifted_char
            keyword_index = (keyword_index + 1) % len(keyword)
        else:
            plaintext += char
            keyword_index = (keyword_index + 1) % len(keyword)
    return plaintext