# Image Hash Spoofer CLI

## Overview
This CLI tool adjusts the pixel values of an image file to produce a hash that starts with a specified prefix.
It maintains the visual appearance of the image while modifying its internal structure to achieve the desired hash prefix.
The tool supports the SHA-512 hash function.

## Features
- Adjusts images to produce hashes with specified prefixes.
- Retains the visual integrity of the image.
- Uses the `sha512` hashing algorithm.
- Easy-to-use command-line interface.

## Requirements
- Python 3.7+
- Required Python libraries:
  - `Pillow`

Install the dependencies using pip:
```bash
pip install pillow
```

## Usage
Run the following command to spoof an image hash:
```bash
python spoof.py <target_prefix> <input_file> <output_file>
```

### Parameters
- `target_prefix`: The desired prefix for the hash (e.g., `0x24`).
- `input_file`: Path to the input image file.
- `output_file`: Path to save the adjusted image.

### Example
To spoof the hash of an image `bed.jpg` so it starts with `0x24`, and save the modified image as `altered.jpg`:
```bash
python spoof.py 0x24 bed.jpg altered.jpg
```
Verify the hash of the resulting file on Linux:
```bash
sha512sum altered.jpg
```

## How It Works
1. The tool loads the input image and converts it to RGB format.
2. It randomly modifies the least significant bits of the image pixels.
3. After each modification, the hash of the image is computed.
4. The process continues until the hash matches the specified prefix or the iteration limit is reached.

## Limitations
- The tool limits attempts to 1,000,000 iterations to prevent excessive runtime.
- Only SHA-512 is supported as the hash function.

## Error Handling
- If the input file does not exist, a `FileNotFoundError` is raised.
- If an unsupported hash function is specified, a `ValueError` is raised.
- Errors during processing are displayed in the console.

## License
This project is open-source and available under the MIT License.