from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from PIL import Image
import numpy as np
import io

app = Flask(__name__)
CORS(app)

def encode_image(image_bytes, message):
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        pixels = np.array(img)
        print("Image opened and converted successfully.")
        print("Pixels array shape:", pixels.shape)
    except Exception as e:
        print("Error opening or converting image:", e)
        raise

    # Convert the message to binary and append an end marker
    binary_msg = ''.join(format(ord(c), '08b') for c in message) + "1111111111111110"
    print("Binary message length:", len(binary_msg))

    idx = 0
    try:
        for row in pixels:
            for pixel in row:
                for i in range(3):
                    if idx < len(binary_msg):
                        # Clear the least significant bit and set it to the message bit
                        pixel[i] = (int(pixel[i]) & 0xFE) | int(binary_msg[idx])
                        idx += 1
        print("Total bits written:", idx)
    except Exception as e:
        print("Error during encoding loop:", e)
        raise

    try:
        img_encoded = Image.fromarray(pixels)
        img_io = io.BytesIO()
        img_encoded.save(img_io, 'PNG')
        img_io.seek(0)
        print("Encoded image saved successfully.")
    except Exception as e:
        print("Error saving encoded image:", e)
        raise

    return img_io

def decode_image(image_bytes):
    try:
        img = Image.open(io.BytesIO(image_bytes))
        pixels = np.array(img)
        print("Image opened for decoding, shape:", pixels.shape)
    except Exception as e:
        print("Error opening image for decoding:", e)
        raise

    binary_msg = ""
    try:
        for row in pixels:
            for pixel in row:
                for i in range(3):
                    bit = str(pixel[i] & 1)
                    binary_msg += bit
                    
                    # Debug: Optionally print the running binary string length
                    if len(binary_msg) % 100 == 0:  # every 100 bits
                        print("Binary string length:", len(binary_msg))
                    
                    # Check if the end marker is reached
                    if binary_msg.endswith("1111111111111110"):
                        print("End marker found at length:", len(binary_msg))
                        binary_msg = binary_msg[:-16]  # Remove the end marker
                        
                        if len(binary_msg) % 8 != 0:
                            print("Warning: Binary message length is not a multiple of 8.")
                        
                        # Split the binary string into 8-bit chunks
                        chunks = [binary_msg[i:i+8] for i in range(0, len(binary_msg), 8)]
                        print("8-bit chunks:", chunks)
                        
                        try:
                            decoded_message = ''.join(chr(int(chunk, 2)) for chunk in chunks)
                        except Exception as conv_err:
                            print("Error converting binary to text:", conv_err)
                            raise
                        
                        print("Decoded message:", decoded_message)
                        return decoded_message
    except Exception as e:
        print("Error during decoding loop:", e)
        raise

    print("End marker not found; returning empty message.")
    return ""



@app.route('/encode', methods=['POST'])
def encode():
    try:
        image = request.files['image'].read()
        message = request.form['message']
        encoded_img_io = encode_image(image, message)
        return send_file(encoded_img_io, mimetype='image/png')
    except Exception as e:
        print("Error in /encode route:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/decode', methods=['POST'])
def decode():
    try:
        image = request.files['image'].read()
        message = decode_image(image)
        return jsonify({"message": message})
    except Exception as e:
        print("Error in /decode route:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
