#!/usr/bin/env python3
import argparse
from PIL import Image
import pillow_heif
import os
import sys


def convert_heic_to_png(input_path, output_path=None):
    """
    Convert HEIC image to PNG format.

    Args:
        input_path (str): Path to input HEIC file
        output_path (str, optional): Path for output PNG file. If not provided,
                                   will use the same name as input with .png extension
    """
    try:
        # Register HEIF opener
        pillow_heif.register_heif_opener()

        # Check if input file exists
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")

        # Generate output path if not provided
        if output_path is None:
            output_path = os.path.splitext(input_path)[0] + ".png"

        # Read and convert the image
        image = Image.open(input_path)

        # Save as PNG
        image.save(output_path, "PNG")
        print(f"Successfully converted {input_path} to {output_path}")

    except Exception as e:
        print(f"Error converting file: {str(e)}", file=sys.stderr)
        sys.exit(1)


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Convert HEIC images to PNG format")
    parser.add_argument("input", help="Input HEIC file path")
    parser.add_argument("-o", "--output", help="Output PNG file path (optional)")

    # Parse arguments
    args = parser.parse_args()

    # Convert the image
    convert_heic_to_png(args.input, args.output)


if __name__ == "__main__":
    main()
