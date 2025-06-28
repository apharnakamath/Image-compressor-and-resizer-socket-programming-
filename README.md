# Image Compressor and Resizer

A lightweight TCP-based client-server application for resizing and compressing images remotely. The server processes images sent by clients, resizes them to specified dimensions, and applies JPEG compression before sending them back.

## Features

- **Remote Processing**: Client-server architecture allows for distributed image processing
- **Image Resizing**: Resize images to custom width and height dimensions
- **JPEG Compression**: Configurable quality compression (default: 85%)
- **Performance Metrics**: Real-time processing time and compression ratio statistics
- **Multiple Format Support**: Input images in various formats (PNG, JPEG, BMP, etc.)
- **Binary Protocol**: Efficient binary data transmission over TCP

## Architecture

The application consists of two main components:

- **Server** (`server.py`): Receives images, processes them, and sends results back
- **Client** (`client.py`): Sends images to server and receives processed results

## Requirements

```
Python 3.6+
Pillow (PIL)
```

Install dependencies:
```bash
pip install Pillow
```

## Usage

### Starting the Server

```bash
python server.py
```

The server will start on `127.0.0.1:65432` by default and listen for incoming connections.

### Using the Client

Basic usage:
```bash
python client.py path/to/your/image.jpg
```

With custom dimensions:
```bash
python client.py path/to/your/image.jpg --width 1024 --height 768
```

### Command Line Arguments

- `image_path`: Path to the input image file (required)
- `--width`: Target width in pixels (default: 800)
- `--height`: Target height in pixels (default: 600)

## Configuration

### Server Configuration

Edit the following variables in `server.py`:

```python
HOST = '127.0.0.1'      # Server IP address
PORT = 65432            # Server port
BUFFER_SIZE = 4096      # Network buffer size
```

### Client Configuration

Edit the following variables in `client.py`:

```python
HOST = '172.16.5.108'   # Server IP address
PORT = 65432            # Server port
BUFFER_SIZE = 4096      # Network buffer size
```

### Image Quality

Modify the compression quality in the `resize_image` function:

```python
def resize_image(image_data, width, height, quality=85):
    # quality: 1-100 (higher = better quality, larger file)
```

## Protocol Specification

The application uses a simple binary protocol:

1. **Client → Server**: Header (12 bytes)
   - Image size (4 bytes, unsigned int)
   - Target width (4 bytes, unsigned int)
   - Target height (4 bytes, unsigned int)

2. **Client → Server**: Image data (variable length)

3. **Server → Client**: Processed image size (4 bytes, unsigned int)

4. **Server → Client**: Processed image data (variable length)

## Output

The client saves processed images with the prefix `processed_` in the same directory.

Example output:
```
Original image size: 2048576 bytes
Connecting to 172.16.5.108:65432...
Connected to server
Sent 2048576 bytes of image data
Expecting processed image of 156789 bytes
Received 156789 bytes of processed image data
Total time: 0.45 seconds
Compression ratio: 13.06x
Saved processed image as processed_image.jpg
Original image dimensions: (3000, 2000)
Processed image dimensions: (800, 600)
```

## Performance Features

- **Processing Time**: Measures server-side image processing time
- **Compression Ratio**: Calculates size reduction after processing
- **Transfer Statistics**: Shows bytes sent/received and total operation time

## Limitations

- Single-threaded server (processes one client at a time)
- No authentication or security features
- Images are processed in memory (large images may cause memory issues)
- No error recovery for network interruptions

## Future Enhancements

- Multi-threaded or async server support
- Authentication and encryption
- Batch processing capabilities
- Additional image formats and processing options
- Configuration file support
- Logging and monitoring features

## License

This project is provided as-is for educational and development purposes.

## Troubleshooting

**Connection Refused**: Ensure the server is running and the client is connecting to the correct IP/port.

**Memory Issues**: For very large images, consider implementing streaming or chunked processing.

**Network Timeouts**: Increase buffer size or implement connection retry logic for unstable networks.
