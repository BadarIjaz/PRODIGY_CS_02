# Pixel Manipulation: Code Analysis & Walkthrough

This document provides a technical deep-dive into the `pixel_manipulation.py` implementation. It outlines the algorithmic logic, Python libraries, and design decisions used to secure image data.

## Core Concepts
To implement image encryption effectively, three key technical concepts were utilized:

1. **RGB Color Model**: Every pixel is represented as a tuple of three integers `(Red, Green, Blue)`, each ranging from `0` to `255`.
2. **SHA-256 Hashing**: To turn a text password into a usable mathematical key, we use a hashing algorithm. This ensures the same password always produces the same integer key.
3. **Modulo Arithmetic (`%`)**: Similar to the Caesar Cipher, we use `% 256` to ensure that after adding/subtracting values, the pixel color remains within the valid byte range (0-255).

---

## Logic Breakdown

### 1. Password Hashing (Key Generation)
Instead of asking for a raw integer, we derive a key from a user string.

```
def get_integer_key(password):
    sha_signature = hashlib.sha256(password.encode()).hexdigest()
    key_int = int(sha_signature, 16)
    return key_int % 256
```

Step-by-Step Execution:

hashlib.sha256(...): Converts the password into a secure, fixed-length hexadecimal string.

int(..., 16): Converts that hex string into a massive integer.

% 256: Compresses that massive integer down to a number between 0-255. This acts as our "shift" value for the pixels.


---

### 2. Opening the Image
We use the Pillow (PIL) library to access the raw data.

```
img = Image.open(image_path)
img = img.convert("RGB")
pixels = img.load()
```

convert("RGB"): Ensures the image is in 3-channel mode (Red, Green, Blue), handling cases where the input might be Grayscale or CMYK.

pixels = img.load(): Creates a 2D matrix of pixel data that we can modify directly.

---

### 3. Encryption Loop (Swap & Math)
We iterate through the image grid (width x height) and apply two layers of obfuscation.


# STEP 1: Swap Red and Blue channels
r, b = b, r

# STEP 2: Mathematical Encryption
pixels[i, j] = ((r + key) % 256, (g + key) % 256, (b + key) % 256)
Why Swap Channels?

Simply adding a number changes the color, but outlines of objects often remain visible (ghosting). Swapping Red and Blue (R, G, B) -> (B, G, R) disrupts the visual structure significantly.

Why % 256?

If a pixel value is 250 and the key is 50, the result is 300. This is invalid for a byte. 300 % 256 = 44. This "wraps" the value around, keeping the file valid.

---

### 4. Smart Renaming & Format Protection
One of the biggest challenges in image cryptography is Lossy Compression (JPEG).

```
new_filename = f"{file_name}_encrypted_{clean_ext}.png"
img.save(new_path, format="PNG")
```

Why force PNG?

When we modify pixels mathematically, every number must be exact. If we save as .jpg, the compression algorithm will "smooth out" our noise, destroying the data needed for decryption. We force .png (lossless) to preserve data integrity.

Why _{clean_ext}?

We embed the original extension (e.g., jpg) into the filename so we know how to restore it later.

---

### 5. Decryption (Reverse Logic)
Decryption must mathematically reverse the encryption steps in the specific order.


# STEP 1: Reverse Math
r = (r - key) % 256
# ... (same for g and b)

# STEP 2: Swap Red and Blue back
r, b = b, r
Algorithmic Symmetry:

Since encryption did Swap -> Add, decryption must do Subtract -> Swap.

---

### 6. Smart Restoration
When the user decrypts, we restore the file to its original state.

```
if original_ext.lower() in ['jpg', 'jpeg']:
    img.save(restore_path, format="JPEG", quality=100, subsampling=0)
else:
    img.save(restore_path, format="PNG")
```

Format Detection: The script parses the filename (e.g., _encrypted_jpg) to find the original format.

Quality Control: If returning to JPEG, we use quality=100 and subsampling=0 to minimize data loss, making the restored image look as close to the original as possible.

---

### 7. Continuous Execution
The main function is wrapped in a loop for user convenience.

```
while True:
    # ... inputs ...
    if choice == 'Q':
        break
```

This allows the user to perform multiple operations (e.g., Encrypt one file, then immediately Decrypt another) without restarting the program.