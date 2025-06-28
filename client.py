import socket
import struct
import os
import io
from PIL import Image
import time
import argparse

# Client configuration
HOST = '172.16.5.108'
PORT = 65432
BUFFER_SIZE = 4096

def send_image_for_processing(image_path, target_width, target_height):
    """Send an image to the server for processing."""
    # Open and read the image file
    with open(image_path, 'rb') as f:
        image_data = f.read()
    
    image_size = len(image_data)
    print(f"Original image size: {image_size} bytes")
    
    # Create a socket and connect to the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        print(f"Connecting to {HOST}:{PORT}...")
        client_socket.connect((HOST, PORT))
        print("Connected to server")
        
        # Send the header with image size and target dimensions
        header = struct.pack('!III', image_size, target_width, target_height)
        client_socket.sendall(header)
        
        # Send the image data
        client_socket.sendall(image_data)
        print(f"Sent {image_size} bytes of image data")
        
        # Start timing the server processing
        start_time = time.time()
        
        # Receive the size of the processed image
        size_data = client_socket.recv(4)
        processed_size = struct.unpack('!I', size_data)[0]
        print(f"Expecting processed image of {processed_size} bytes")
        
        # Receive the processed image
        processed_image = b''
        remaining = processed_size
        
        while remaining > 0:
            chunk_size = min(BUFFER_SIZE, remaining)
            chunk = client_socket.recv(chunk_size)
            if not chunk:
                break
            processed_image += chunk
            remaining -= len(chunk)
        
        # End timing
        total_time = time.time() - start_time
        
        print(f"Received {len(processed_image)} bytes of processed image data")
        print(f"Total time: {total_time:.2f} seconds")
        
        # Calculate compression ratio
        compression_ratio = image_size / len(processed_image)
        print(f"Compression ratio: {compression_ratio:.2f}x")
        
        # Save the processed image
        output_filename = f"processed_{os.path.basename(image_path)}"
        with open(output_filename, 'wb') as f:
            f.write(processed_image)
        
        print(f"Saved processed image as	` {output_filename}")
        
        # Display image information
        try:
            original_img = Image.open(image_path)
            processed_img = Image.open(io.BytesIO(processed_image))
            
            print(f"Original image dimensions: {original_img.size}")
            print(f"Processed image dimensions: {processed_img.size}")
        except Exception as e:
            print(f"Error getting image information: {e}")

def main():
    """Parse arguments and send image for processing."""
    parser = argparse.ArgumentParser(description='Client for image resizing and compression')
    parser.add_argument('image_path', help='Path to the image file')
    parser.add_argument('--width', type=int, default=800, help='Target width for resizing')
    parser.add_argument('--height', type=int, default=600, help='Target height for resizing')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.image_path):
        print(f"Error: Image file '{args.image_path}' not found")
        return
    
    send_image_for_processing(args.image_path, args.width, args.height)

if __name__ == "__main__":
    main()
