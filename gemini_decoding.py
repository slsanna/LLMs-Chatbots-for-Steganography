from PIL import Image
import sys

def decode_lsb(image_path, delimiter="#####"):
    """
    Decodes a message hidden in the LSBs of an image's pixels.
    Stops when the delimiter sequence is found.
    """
    try:
        img = Image.open(image_path).convert('RGB') # Ensure image is in RGB
    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error opening or processing image: {e}")
        sys.exit(1)

    width, height = img.size
    binary_message = ""
    delimiter_binary = ''.join(format(ord(char), '08b') for char in delimiter)
    delimiter_len = len(delimiter_binary)
    extracted_bits = ""

    pixel_index = 0
    for y in range(height):
        for x in range(width):
            try:
                r, g, b = img.getpixel((x, y))
            except IndexError:
                print("Warning: Reached end of image data unexpectedly.")
                break # Should not happen with width/height loop, but safe check

            # Extract LSB from each color channel
            binary_message += bin(r)[-1]
            extracted_bits += bin(r)[-1]
            if len(extracted_bits) >= delimiter_len and extracted_bits.endswith(delimiter_binary):
                print("Delimiter found. Decoding complete.")
                binary_message = binary_message[:-delimiter_len] # Remove delimiter
                return binary_to_string(binary_message)

            binary_message += bin(g)[-1]
            extracted_bits += bin(g)[-1]
            if len(extracted_bits) >= delimiter_len and extracted_bits.endswith(delimiter_binary):
                print("Delimiter found. Decoding complete.")
                binary_message = binary_message[:-delimiter_len] # Remove delimiter
                return binary_to_string(binary_message)

            binary_message += bin(b)[-1]
            extracted_bits += bin(b)[-1]
            if len(extracted_bits) >= delimiter_len and extracted_bits.endswith(delimiter_binary):
                print("Delimiter found. Decoding complete.")
                binary_message = binary_message[:-delimiter_len] # Remove delimiter
                return binary_to_string(binary_message)

            pixel_index += 1

    print("Warning: Reached end of image without finding the specified delimiter.")
    # Optionally, try decoding what was found anyway
    return binary_to_string(binary_message)

def binary_to_string(binary_data):
    """Converts a binary string (e.g., '0110100001101001') to a string."""
    # Ensure the binary string length is a multiple of 8
    remainder = len(binary_data) % 8
    if remainder != 0:
        print(f"Warning: Binary data length ({len(binary_data)}) is not a multiple of 8. Trimming last {remainder} bits.")
        binary_data = binary_data[:-remainder]

    if not binary_data:
        return ""

    message = ""
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i+8]
        try:
            decimal_value = int(byte, 2)
            message += chr(decimal_value)
        except ValueError:
            print(f"Warning: Could not convert byte '{byte}' at position {i//8}. Skipping.")
        except Exception as e:
            print(f"An error occurred converting byte '{byte}': {e}. Skipping.")

    return message

# --- How to Use ---
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python decode_script.py <path_to_your_image>")
        sys.exit(1)

    image_file = sys.argv[1]
    # You might need to know the delimiter used during encoding.
    # If you don't know it, you might guess common ones or analyze the LSBs.
    # Using "#####" as an example delimiter.
    secret_delimiter = "#####"

    print(f"Attempting to decode message from '{image_file}' using LSB...")
    hidden_message = decode_lsb(image_file, delimiter=secret_delimiter)

    if hidden_message:
        print("\nDecoded Message:")
        print(hidden_message)
    else:
        print("\nNo message found or decoded (or delimiter not found).")