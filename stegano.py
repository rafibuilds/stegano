from PIL import Image
import sys

# SECRET KEY SHOULD ALWAYS BE 6
# encrypt the text
def encrypt(text, key):
    encypted_data = []
    for char in text:
        encypted_data.append(chr(ord(char) + key))
    return ''.join(encypted_data)

# SECRET KEY SHOULD ALWAYS BE 6
# decrypt the text
def decrypt(text, key):
    decrypted_data = []
    for char in text:
        decrypted_data.append(chr(ord(char) - key))
    return ''.join(decrypted_data)

# encode the data
def encode(image_path, secret_msg, output_path):
    try:
        image = Image.open(image_path)
    except FileNotFoundError:
        sys.exit("File not found")

    image_pixs = image.load()
    output_image = Image.new(image.mode, image.size, (255, 255, 255, 255))
    output_pixs = output_image.load()

    msg_len = len(secret_msg)
    msg_index = 0

    for y in range(image.size[1]):
        for x in range(image.size[0]):
            if len(image_pixs[x, y]) == 3:
                r, g, b = image_pixs[x, y]
                if x == 0 and y == 0: # encode the size of the text in the first pixel of the image in R value
                    output_pixs[x, y] = (msg_len, g, b)
                elif msg_index <= msg_len: # encode the ascii value of each char in the R value of each pixel
                    output_pixs[x, y] = (ord(secret_msg[msg_index - 1]), g, b)
                else: # The rest of the RGB values be the same
                    output_pixs[x, y] = (r, g, b)

            elif len(image_pixs[x, y]) == 4:
                r, g, b, a = image_pixs[x, y]
                if x == 0 and y == 0: # encode the size of the text in the first pixel of the image in R value
                    output_pixs[x, y] = (msg_len, g, b, a)
                elif msg_index <= msg_len: # encode the ascii value of each char in the R value of each pixel
                    output_pixs[x, y] = (ord(secret_msg[msg_index - 1]), g, b, a)
                else: # The rest of the RGB values be the same
                    output_pixs[x, y] = (r, g, b, a)

            msg_index += 1

    image.close()
    output_image.save(output_path)  

# decode the data
def decode(image_path):
    try:
        image = Image.open(image_path)
    except FileNotFoundError:
        sys.exit("File not found")
    
    #Find the length of the secret message
    image_pixs = image.load()
    msg_len = image_pixs[0, 0][0] # The length of the text is in the first pixel's R value
    pixel_index = 0
    msg = ''

    for y in range(image.size[1]):
        for x in range(image.size[0]):
            if (pixel_index <= msg_len) and (pixel_index > 0):
                msg += chr(image_pixs[x, y][0])
            pixel_index += 1

    image.close()
    return msg

def main():
    print("""\nWelcome to Stegano. Steganography is art and science of hiding data.

(This program works best for PNG files)
          
The whole process is in two steps:
1. First encrypt the text to a form that cannot be read without a specific key.
2. The encrypted text is then formatted to binary.
3. The binary is then encoded in a picture""")

    print("""\nThere are two modes:
1. Encode (type on the keyboard: 1)
2. Decode (type on the keyboard: 2)""")

    print("\nMode:")
    mode = None

    while mode not in [1, 2]:
        try:
            mode = int(input("> "))
        except ValueError:
            pass
    
    if mode == 1:
        text = input("Text: ")
        key = int(input("Key for encryption (0-20): "))
        encrypted_text = encrypt(text, key)
        input_image = input("Input image path (with extension): ")
        output_image = input("Output image path (with extension): ")
        encode(input_image, encrypted_text, output_image)
        
    elif mode == 2:
        image = input("Image path (with extension): ")
        key = int(input("Key for decryption (0-20): "))
        decoded_text = decode(image)
        decrypted_text = decrypt(decoded_text, key)
        print("Message: " + decrypted_text)

if __name__ == "__main__":
    main()