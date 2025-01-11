import getpass
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64

def encrypt(data: str, key: bytes) -> str:
    """
    Encrypt data using AES-256 in CBC mode with PKCS7 padding
    
    Args:
        data: String to encrypt
        key: 32-byte encryption key
    
    Returns:
        Base64 encoded encrypted string
    """
    # Convert string to bytes
    data_bytes = data.encode('utf-8')
    
    # Generate random IV
    iv = get_random_bytes(AES.block_size)
    
    # Create cipher object and encrypt the data
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_bytes = cipher.encrypt(pad(data_bytes, AES.block_size))
    
    # Combine IV and encrypted data and encode as base64
    encrypted_data = base64.b64encode(iv + encrypted_bytes).decode('utf-8')
    return encrypted_data

def decrypt(encrypted_data: str, key: bytes) -> str:
    """
    Decrypt AES-256 encrypted data
    
    Args:
        encrypted_data: Base64 encoded encrypted string
        key: 32-byte decryption key
    
    Returns:
        Decrypted string
    """
    # Decode the base64 string
    encrypted_bytes = base64.b64decode(encrypted_data.encode('utf-8'))
    
    # Extract IV and ciphertext
    iv = encrypted_bytes[:AES.block_size]
    ciphertext = encrypted_bytes[AES.block_size:]
    
    # Create cipher object and decrypt the data
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_bytes = unpad(cipher.decrypt(ciphertext), AES.block_size)
    
    # Convert bytes back to string
    return decrypted_bytes.decode('utf-8')


def decrypt_from_file(file_path: str, key: bytes) -> str:
    with open(file_path, "r") as file:
        encrypted_data = file.read()
        encrypted_data = encrypted_data.replace("\n", "")
        encrypted_data = encrypted_data.replace("\r", "")
        encrypted_data = encrypted_data.replace("\t", "")
        encrypted_data = encrypted_data.replace(" ", "")
    return decrypt(encrypted_data, key)


def encrypt_file_and_cover(file_path: str, key: bytes) -> str:
    with open(file_path, "r") as file:
        data = file.read()
        data = data.replace("\n", "")
        data = data.replace("\r", "")
        data = data.replace("\t", "")
        data = data.replace(" ", "")
    encrypted = encrypt(data, key)
    with open(file_path, "w") as file:
        file.write(encrypted)
        

def encrypt_from_input() -> None:
    """
    Get input data and hex key from terminal and show encrypted result
    """
    data = getpass.getpass("Enter data to encrypt: ")
    key_hex = getpass.getpass("Enter 32-byte hex key: ")
    
    try:
        key = bytes.fromhex(key_hex)
        if len(key) != 32:
            raise ValueError("Key must be 32 bytes (64 hex characters)")
            
        encrypted = encrypt(data, key)
        print(f"Encrypted: {encrypted}")
        
    except ValueError as e:
        raise ValueError(f"Invalid hex key - {str(e)}")
        

def decrypt_from_input() -> None:
    """
    Get encrypted data and hex key from terminal and show decrypted result
    """
    encrypted = getpass.getpass("Enter encrypted data: ")
    key_hex = getpass.getpass("Enter 32-byte hex key: ")
    
    try:
        key = bytes.fromhex(key_hex)
        if len(key) != 32:
            raise ValueError("Key must be 32 bytes (64 hex characters)")
            
        decrypted = decrypt(encrypted, key)
        print(f"Decrypted: {decrypted}")
        
    except ValueError as e:
        raise ValueError(f"Invalid hex key - {str(e)}")
        

def decrypt_file_from_input_hex_key() -> str:
    """
    Get file path and hex key from terminal, decrypt file contents and return decrypted string
    """
    file_path = input("Enter file path: ")
    key_hex = getpass.getpass("Enter 32-byte hex key: ")
    
    try:
        key = bytes.fromhex(key_hex)
        if len(key) != 32:
            raise ValueError("Key must be 32 bytes (64 hex characters)")
            
        with open(file_path, "r") as file:
            encrypted = file.read()
            
        decrypted = decrypt(encrypted, key)
        return decrypted
        
    except ValueError as e:
        raise ValueError(f"Invalid hex key - {str(e)}")
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found - {file_path}")
    except Exception as e:
        raise Exception(f"Error decrypting file: {str(e)}")


if __name__ == "__main__":
    encrypt_from_input()