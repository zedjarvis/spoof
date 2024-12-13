import argparse
import hashlib
import random

from PIL import Image


def adjust_image_to_hash(input_file, output_file, target_prefix, hash_func="sha512"):
    """
    Adjust the pixel values of an image to create a hash that matches a given prefix.

    Parameters:
        input_file (str): Path to the input image file.
        output_file (str): Path to save the output image with adjusted pixel values.
        target_prefix (str): Desired prefix for the hash (e.g., '0x24').
        hash_func (str): Hash function to use (default is 'sha512').

    Returns:
        bool: True if successful in finding a matching hash, False otherwise.

    Raises:
        ValueError: If the hash function is not supported by hashlib.
        FileNotFoundError: If the input file does not exist.
    """
    # Load image
    try:
        img = Image.open(input_file)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Input file not found: {input_file}") from e

    img = img.convert("RGB")  # Ensure it's in RGB format
    pixels = img.load()

    width, height = img.size

    # Check if hash function is valid
    if not hasattr(hashlib, hash_func):
        raise ValueError(f"Hash function '{hash_func}' is not supported.")

    hash_function = getattr(hashlib, hash_func)

    def compute_hash(data):
        return hash_function(data).hexdigest()

    # Normalize target prefix by removing leading '0x' if present
    if target_prefix.startswith("0x"):
        target_prefix = target_prefix[2:]

    # Start altering the image to achieve desired hash
    success = False
    for attempt in range(1000000):  # Limit the number of iterations
        # Modify a random pixel slightly
        x, y = random.randint(0, width - 1), random.randint(0, height - 1)
        r, g, b = pixels[x, y]

        # Modify least significant bits
        r = (r & ~1) | random.randint(0, 1)
        g = (g & ~1) | random.randint(0, 1)
        b = (b & ~1) | random.randint(0, 1)
        pixels[x, y] = (r, g, b)

        # Save modified image to bytes
        img_bytes = img.tobytes()
        img_hash = compute_hash(img_bytes)

        if img_hash.startswith(target_prefix):
            success = True
            print(f"Success after {attempt + 1} attempts: {img_hash}")
            img.save(output_file)
            break

    if not success:
        print("Failed to find a matching hash within the attempt limit.")
        return False

    return True


def main():
    """
    Entry point for the CLI tool. Parses arguments and invokes the image adjustment function.
    """
    parser = argparse.ArgumentParser(
        description="Spoof an image to produce a hash with a specific prefix."
    )
    parser.add_argument(
        "target_prefix", type=str, help="Desired prefix for the hash (e.g., '0x24')."
    )
    parser.add_argument("input_file", type=str, help="Path to the input image file.")
    parser.add_argument(
        "output_file", type=str, help="Path to save the adjusted image."
    )

    args = parser.parse_args()

    # Call the function with parsed arguments
    try:
        success = adjust_image_to_hash(
            args.input_file, args.output_file, args.target_prefix, "sha512"
        )
        if success:
            print(f"Output saved to {args.output_file}")
        else:
            print("Could not achieve the desired hash prefix within the attempt limit.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
