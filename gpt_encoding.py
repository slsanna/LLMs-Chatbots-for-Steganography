from PIL import Image
import numpy as np

def encode_message_in_image(input_image_path, output_image_path, message):
    # Load and convert image to RGB
    image = Image.open(input_image_path).convert('RGB')
    pixels = np.array(image)

    # Convert message to binary + null terminator
    binary_message = ''.join(f"{ord(c):08b}" for c in message) + '00000000'

    flat_pixels = pixels.reshape(-1, 3)
    bit_index = 0

    for i in range(len(flat_pixels)):
        for j in range(3):  # Loop over R, G, B channels
            if bit_index < len(binary_message):
                #flat_pixels[i, j] = (flat_pixels[i, j] & ~1) | int(binary_message[bit_index])
                flat_pixels[i, j] = (flat_pixels[i, j] & 0xFE) | int(binary_message[bit_index])
                bit_index += 1

    if bit_index < len(binary_message):
        raise ValueError("Message is too long to fit in the image.")

    # Reshape and save the modified image
    encoded_pixels = flat_pixels.reshape(pixels.shape)
    encoded_image = Image.fromarray(encoded_pixels.astype('uint8'), 'RGB')
    encoded_image.save(output_image_path)

    print(f"✅ Hidden message encoded into: {output_image_path}")

# Example usage
if __name__ == "__main__":
    input_img = "white.png"              # Replace with your image
    output_img = "gpt_script.png"    # Output image
    secret = "This is a secret message APWG." # Hidden message
    encode_message_in_image(input_img, output_img, secret)
