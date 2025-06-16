from PIL import Image, ImageDraw

# Create a blank white image for teaching purposes
width, height = 300, 300
image = Image.new('RGB', (width, height), color='white')

# Draw some text on the image
draw = ImageDraw.Draw(image)
draw.text((10, 10), "Teaching Image", fill='black')

# Save the image
image.save('teaching_image.png')

# Function to encode a secret message into an image
def encode_image(image_path, secret_message, output_path):
    # Load the image
    image = Image.open(image_path)
    encoded_image = image.copy()
    
    width, height = image.size
    index = 0
    
    # Convert the secret message to binary
    binary_secret_message = ''.join(format(ord(char), '08b') for char in secret_message)
    
    # Add a delimiter to the end of the binary message
    binary_secret_message += '1111111111111110'
    
    # Encode the message into the image
    for row in range(height):
        for col in range(width):
            if index < len(binary_secret_message):
                pixel = list(image.getpixel((col, row)))
                for n in range(3):  # Iterate over RGB channels
                    if index < len(binary_secret_message):
                        pixel[n] = pixel[n] & ~1 | int(binary_secret_message[index])
                        index += 1
                encoded_image.putpixel((col, row), tuple(pixel))
    
    # Save the encoded image
    encoded_image.save(output_path)

# Encode a secret message into the teaching image
encode_image('white.png', 'This is a secret message APWG.', 'copilot_script.png')