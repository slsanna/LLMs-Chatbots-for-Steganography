from PIL import Image
import sys

def string_to_binary(message):
    """Converts a string into a binary string (e.g., 'hi' -> '0110100001101001')."""
    return ''.join(format(ord(char), '08b') for char in message)

def encode_lsb(input_image_path, message, output_image_path, delimiter="#####"):
    """Encodes a message into the LSBs of an image's pixels."""
    try:
        img = Image.open(input_image_path).convert('RGB') # Ensure image is in RGB
    except FileNotFoundError:
        print(f"Error: Input image file not found at {input_image_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error opening or processing input image: {e}")
        sys.exit(1)

    width, height = img.size
    max_bytes = (width * height * 3) // 8
    print(f"Image dimensions: {width}x{height} pixels.")
    print(f"Maximum theoretical capacity for LSB: {max_bytes} bytes.")

    # Convert message and delimiter to binary
    binary_message = string_to_binary(message + delimiter)
    message_length_bits = len(binary_message)
    required_pixels = (message_length_bits + 2) // 3 # +2 ensures we have enough pixels for rounding up

    print(f"Message length: {len(message)} characters + {len(delimiter)} delimiter characters.")
    print(f"Total bits to encode (message + delimiter): {message_length_bits} bits.")
    print(f"Required pixels: {required_pixels}.")

    # Check if the image has enough capacity
    if message_length_bits > width * height * 3:
        print(f"Error: Message is too long to be encoded in this image.")
        print(f"  Required bits: {message_length_bits}")
        print(f"  Available LSBs: {width * height * 3}")
        sys.exit(1)

    # Create a new image or load data to modify
    encoded_img = img.copy() # Work on a copy
    pixels = encoded_img.load() # Load pixel map for modification

    data_index = 0
    print("Encoding message...")
    for y in range(height):
        for x in range(width):
            if data_index < message_length_bits:
                try:
                    r, g, b = pixels[x, y]
                except IndexError:
                     print(f"Error accessing pixel ({x},{y}). Should not happen.")
                     continue # Should not happen based on width/height loop

                # Modify LSB of Red channel
                if data_index < message_length_bits:
                    r_binary = format(r, '08b')
                    new_r_binary = r_binary[:-1] + binary_message[data_index]
                    r = int(new_r_binary, 2)
                    data_index += 1
                else: # Optimization: Stop if message fully encoded
                    break

                # Modify LSB of Green channel
                if data_index < message_length_bits:
                    g_binary = format(g, '08b')
                    new_g_binary = g_binary[:-1] + binary_message[data_index]
                    g = int(new_g_binary, 2)
                    data_index += 1
                else: # Optimization: Stop if message fully encoded
                    pixels[x, y] = (r, g, b) # Save the potentially modified R value
                    break

                # Modify LSB of Blue channel
                if data_index < message_length_bits:
                    b_binary = format(b, '08b')
                    new_b_binary = b_binary[:-1] + binary_message[data_index]
                    b = int(new_b_binary, 2)
                    data_index += 1
                else: # Optimization: Stop if message fully encoded
                    pixels[x, y] = (r, g, b) # Save the potentially modified R, G values
                    break

                pixels[x, y] = (r, g, b) # Save modified pixel

            else: # Message finished, break outer loop
                break
        if data_index >= message_length_bits: # Break outer loop as well
            break

    # Save the modified image
    try:
        encoded_img.save(output_image_path, format='PNG') # Save as PNG (lossless) is recommended
        print(f"Message encoded successfully into '{output_image_path}'")
    except Exception as e:
        print(f"Error saving the encoded image: {e}")
        sys.exit(1)

# --- How to Use ---
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python encode_script.py <input_image_path> \"<your_message>\" <output_image_path>")
        print("Example: python encode_script.py beach.png \"Meet at noon\" encoded_beach.png")
        sys.exit(1)

    input_image = sys.argv[1]
    message_to_hide = sys.argv[2]
    output_image = sys.argv[3]

    # Using "#####" as the delimiter. The decoder needs to use the same one.
    encode_lsb(input_image, message_to_hide, output_image, delimiter="#####")