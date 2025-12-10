from PIL import Image
import os
import hashlib  # Library for password hashing

def get_integer_key(password):
    """
    Turns a text password into an integer key using SHA-256 hashing.
    This ensures 'MySecretPass' always becomes the same number (e.g., 184).
    """
    # 1. Hash the password
    sha_signature = hashlib.sha256(password.encode()).hexdigest()
    # 2. Convert hex hash to an integer
    key_int = int(sha_signature, 16)
    # 3. Return a number between 0-255 so it fits in a pixel byte
    return key_int % 256

def encrypt_image(image_path, password):
    try:
        print(f"Encrypting {image_path}...")
        img = Image.open(image_path)
        img = img.convert("RGB")
        pixels = img.load()

        width, height = img.size
        
        # Get integer key from password
        key = get_integer_key(password)

        for i in range(width):
            for j in range(height):
                r, g, b = pixels[i, j]

                # STEP 1: Swap Red and Blue channels (Obfuscation)
                # (R, G, B) becomes (B, G, R)
                r, b = b, r

                # STEP 2: Mathematical Encryption
                pixels[i, j] = ((r + key) % 256, (g + key) % 256, (b + key) % 256)

        # Smart Renaming
        file_dir, full_name = os.path.split(image_path)
        file_name, file_ext = os.path.splitext(full_name)
        clean_ext = file_ext.replace('.', '')
        new_filename = f"{file_name}_encrypted_{clean_ext}.png"
        new_path = os.path.join(file_dir, new_filename)

        img.save(new_path, format="PNG")
        print(f"✅ Encrypted using password! Saved as: {new_filename}")

        if os.path.exists(image_path):
            os.remove(image_path)
            print("Original file 🗑️  Deleted.")

    except Exception as e:
        print(f"❌ Error: {e}")

def decrypt_image(image_path, password):
    try:
        print(f"Decrypting {image_path}...")
        img = Image.open(image_path)
        img = img.convert("RGB")
        pixels = img.load()

        width, height = img.size
        
        # Get same integer key from password
        key = get_integer_key(password)

        for i in range(width):
            for j in range(height):
                r, g, b = pixels[i, j]

                # STEP 1: Reverse Math
                r = (r - key) % 256
                g = (g - key) % 256
                b = (b - key) % 256

                # STEP 2: Swap Red and Blue back
                # (B, G, R) becomes (R, G, B)
                r, b = b, r

                pixels[i, j] = (r, g, b)

        # Smart Renaming (Restore)
        file_dir, full_name = os.path.split(image_path)
        
        if "_encrypted_" in full_name:
            temp_name = os.path.splitext(full_name)[0] 
            parts = temp_name.split("_encrypted_")
            original_name = parts[0]
            original_ext = parts[1]
            
            restore_name = f"{original_name}.{original_ext}"
            restore_path = os.path.join(file_dir, restore_name)
            
            if original_ext.lower() in ['jpg', 'jpeg']:
                img.save(restore_path, format="JPEG", quality=100, subsampling=0)
            else:
                img.save(restore_path, format="PNG")
                
            print(f"✅ Decrypted using password! Restored: {restore_name}")

            if os.path.exists(image_path):
                os.remove(image_path)
                print("Encrypted file 🗑️  Deleted.")
        else:
            print("❌ Error: Filename format incorrect.")

    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("========================================")
    print("   CyberSec Image Encryptor   ")
    print("========================================")

    while True:
        print("\n----------------------------------------")
        choice = input("Do you want to (E)ncrypt, (D)ecrypt, or (Q)uit? ").upper()
        
        if choice == 'Q':
            break

        if choice not in ['E', 'D']:
            continue

        path = input("Enter the path to the image: ").strip('"')
        
        if not os.path.exists(path):
            print("❌ File not found!")
            continue

        # We ask for a Password
        password = input("Enter your secret password: ")

        if choice == 'E':
            encrypt_image(path, password)
        elif choice == 'D':
            decrypt_image(path, password)

if __name__ == "__main__":
    main()