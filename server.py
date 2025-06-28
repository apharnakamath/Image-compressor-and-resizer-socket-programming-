import socket
import struct
import io
from PIL import Image
import zlib
import os
import time

# Server configuration
HOST = '127.0.0.1'
PORT = 65432
BUFFER_SIZE = 4096

def resize_image(image_data, width, height, quality=85):
    """Resize image and compress it with the specified quality."""
    # Open image from binary data
    img = Image.open(io.BytesIO(image_data))
    
    # Resize the image
    resized_img = img.resize((width, height), Image.LANCZOS)
    
    # Save the resized image to a bytes buffer with compression
    output_buffer = io.BytesIO()
    resized_img.save(output_buffer, format='JPEG', quality=quality)
    compressed_data = output_buffer.getvalue()
    
    # Return the compressed image data
    return compressed_data

def handle_client(client_socket):
    """Handle a client connection."""
    try:
        # First receive the header (contains sizes)
        header = client_socket.recv(12)
        if not header or len(header) < 12:
            print("Error: Incomplete header received")
            return
        
        # Unpack the header
        image_size, target_width, target_height = struct.unpack('!III', header)
        print(f"Receiving image of size {image_size} bytes")
        print(f"Target dimensions: {target_width}x{target_height}")
        
        # Receive the image data
        image_data = b''
        remaining = image_size
        
        while remaining > 0:
            chunk_size = min(BUFFER_SIZE, remaining)
            chunk = client_socket.recv(chunk_size)
            if not chunk:
                break
            image_data += chunk
            remaining -= len(chunk)
        
        print(f"Received {len(image_data)} bytes of image data")
        
        # Start timing the processing
        start_time = time.time()
        
        # Process the image (resize and compress)
        processed_image = resize_image(image_data, target_width, target_height)
        
        # End timing
        processing_time = time.time() - start_time
        
        # Calculate compression ratio
        compression_ratio = len(image_data) / len(processed_image)
        
        print(f"Processing completed in {processing_time:.2f} seconds")
        print(f"Original size: {len(image_data)} bytes")
        print(f"Processed size: {len(processed_image)} bytes")
        print(f"Compression ratio: {compression_ratio:.2f}x")
        
        # Send the size of the processed image first
        client_socket.sendall(struct.pack('!I', len(processed_image)))
        
        # Send the processed image
        client_socket.sendall(processed_image)
        
        print("Image sent back to client")
        
    except Exception as e:
        print(f"Error processing client request: {e}")
    finally:
        client_socket.close()

def main():
    """Main server function."""
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Set socket option to reuse address
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind the socket to the port
    server_socket.bind((HOST, PORT))
    
    # Listen for incoming connections
    server_socket.listen(5)
    print(f"Server started on {HOST}:{PORT}")
    
    try:
        while True:
            # Wait for a connection
            client_socket, client_address = server_socket.accept()
            print(f"Connected to client at {client_address}")
            
            # Handle the client in the same thread
            # In a production environment, you'd want to use threading or async
            handle_client(client_socket)
            
    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
