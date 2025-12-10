# PRODIGY_CS_02
## Task-02: Pixel Manipulation for Image Encryption

This repository contains a simple image encryption tool developed in Python. It uses pixel manipulation techniques to secure images. Users can encrypt and decrypt images using a secret password, which performs mathematical operations and swaps pixel channels to obfuscate the image data.

### Usage
1. Run the script: `python pixel_manipulation.py`
2. Choose to (E)ncrypt or (D)ecrypt.
3. Enter the path to your image file.
4. Enter a secret password (this generates the encryption key).

### Watch the Demo Video
[Click to view the demo](pixel_manipulation_demo.mp4)

### Example

**Encryption:**
* **Input:** `my_photo.jpg` + Password: `CyberSec123`
* **Output:** A new file `my_photo_encrypted_jpg.png` containing visual noise/scrambled pixels. The original file is removed for security.

**Decryption:**
* **Input:** `my_photo_encrypted_jpg.png` + Password: `CyberSec123`
* **Output:** The original image `my_photo.jpg` is restored with correct colors and dimensions.