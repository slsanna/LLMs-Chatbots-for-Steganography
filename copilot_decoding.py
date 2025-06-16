from PIL import Image

# Function to decode a secret message from an image
def decode_image(image_path):
    # Load the image
    image = Image.open(image_path)
    
    width, height = image.size
    binary_secret_message = ''
    
    # Decode the message from the image
    for row in range(height):
        for col in range(width):
            pixel = list(image.getpixel((col, row)))
            for n in range(3):  # Iterate over RGB channels
                binary_secret_message += str(pixel[n] & 1)
    
    # Split by 8 bits and convert to characters
    secret_message = ''
    for i in range(0, len(binary_secret_message), 8):
        byte = binary_secret_message[i:i+8]
        if byte == '11111111':  # Delimiter found
            break
        secret_message += chr(int(byte, 2))
    
    return secret_message

# Example usage:
# Decode the secret message from the encoded teaching image
decoded_message = decode_image('icon_seq_lsb.png')
print(f"Decoded message: {decoded_message}")