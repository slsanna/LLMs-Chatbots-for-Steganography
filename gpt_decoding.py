from PIL import Image
import numpy as np

def decode_image(image_path):
    image = Image.open(image_path).convert("RGB")
    pixels = np.array(image).reshape(-1, 3)

    bits = []
    for pixel in pixels:
        for color in pixel:
            bits.append(str(color & 1))
    
    # Join bits and convert every 8 bits to a character
    chars = []
    for i in range(0, len(bits), 8):
        byte = ''.join(bits[i:i+8])
        if byte == '00000000':  # Null terminator
            break
        chars.append(chr(int(byte, 2)))

    return ''.join(chars)

# Usage
hidden_message = decode_image("icon_seq_lsb.png")
print("Hidden message:", hidden_message)
