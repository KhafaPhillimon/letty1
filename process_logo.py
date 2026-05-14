#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Process company logo to make background transparent
"""

from PIL import Image, ImageDraw
import os

def make_logo_transparent(input_path, output_path, white_threshold=240):
    """
    Remove white/light background from logo and make it transparent.

    Args:
        input_path: Path to original logo image
        output_path: Path to save transparent version
        white_threshold: RGB value threshold for white (0-255)
    """
    try:
        # Open image and convert to RGBA
        img = Image.open(input_path).convert("RGBA")

        # Get image dimensions
        width, height = img.size
        print(f"[OK] Loaded image: {width}x{height} pixels")

        # Process each pixel
        data = img.getdata()
        new_data = []

        for r, g, b, a in data:
            # If pixel is light (white/near-white), make it transparent
            if r > white_threshold and g > white_threshold and b > white_threshold:
                new_data.append((255, 255, 255, 0))  # Transparent
            else:
                new_data.append((r, g, b, a))  # Keep original

        # Apply new data
        img.putdata(new_data)

        # Save with transparency
        img.save(output_path, "PNG")
        print(f"[OK] Saved transparent logo: {output_path}")
        print(f"[OK] Size: {os.path.getsize(output_path) / 1024:.1f} KB")

        return True

    except FileNotFoundError:
        print(f"[ERROR] File not found: {input_path}")
        return False
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return False

def optimize_logo(input_path, output_path, size=(200, 200)):
    """
    Optimize logo: resize and ensure transparency.

    Args:
        input_path: Path to logo
        output_path: Path to save optimized version
        size: Target size (width, height)
    """
    try:
        img = Image.open(input_path).convert("RGBA")

        # Resize while maintaining aspect ratio
        img.thumbnail(size, Image.Resampling.LANCZOS)

        # Create new image with white background
        new_img = Image.new("RGBA", size, (255, 255, 255, 0))

        # Calculate position to center logo
        x = (size[0] - img.size[0]) // 2
        y = (size[1] - img.size[1]) // 2

        # Paste logo
        new_img.paste(img, (x, y), img)

        # Save
        new_img.save(output_path, "PNG")
        print(f"[OK] Optimized logo saved: {output_path}")
        return True

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return False

if __name__ == "__main__":
    import sys

    print("\n" + "="*60)
    print("  Logo Transparency Processor")
    print("="*60 + "\n")

    # Check for input file
    input_file = "logo.png"  # Expected input filename
    output_file = "logo_transparent.png"
    optimized_file = "logo_optimized.png"

    if not os.path.exists(input_file):
        print(f"[ERROR] Please save your logo as '{input_file}' in this directory")
        print(f"\nExpected location: {os.path.abspath(input_file)}")
        sys.exit(1)

    print(f"Processing: {input_file}\n")

    # Make background transparent
    if make_logo_transparent(input_file, output_file, white_threshold=240):
        print()

        # Create optimized version
        if optimize_logo(output_file, optimized_file, size=(150, 150)):
            print()
            print("="*60)
            print("  SUCCESS")
            print("="*60)
            print(f"  [OK] logo_transparent.png - Full size with transparency")
            print(f"  [OK] logo_optimized.png - 150x150 optimized version")
            print("\nUse these logos in your dashboard!")
            print("="*60 + "\n")
