def stretch_key(key, length):
    key_length = len(key)
    if key_length < length:
        repetitions = length // key_length
        remainder = length % key_length
        stretched_key = (key * repetitions) + key[:remainder]
    elif key_length > length:
        stretched_key = key[:length]
    else:
        stretched_key = key
    return stretched_key


def advanced_xor_encrypt(message, key):
    nonce = len(message)
    extended_key = stretch_key(key, len(message))
    message_bytes = message.encode()
    key_bytes = extended_key.encode()
    encrypted_bytes = bytearray(message_bytes)
    for i in range(len(message_bytes)):
        encrypted_bytes[i] ^= key_bytes[i % len(key_bytes)]
        encrypted_bytes[i] ^= nonce
        encrypted_bytes[i] = (encrypted_bytes[i] + i) % 256
    return encrypted_bytes.hex()


def advanced_xor_decrypt(encrypted_message, key):
    encrypted_bytes = bytes.fromhex(encrypted_message)
    nonce = len(encrypted_bytes)
    extended_key = stretch_key(key, len(encrypted_bytes))
    key_bytes = extended_key.encode()
    decrypted_bytes = bytearray(encrypted_bytes)
    for i in range(len(encrypted_bytes)):
        decrypted_bytes[i] = (decrypted_bytes[i] - i) % 256
        decrypted_bytes[i] ^= nonce
        decrypted_bytes[i] ^= key_bytes[i % len(key_bytes)]
    decrypted_message = decrypted_bytes.decode()
    return decrypted_message
