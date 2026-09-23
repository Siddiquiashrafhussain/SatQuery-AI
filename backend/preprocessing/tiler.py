import sys
import os
from worker import build_pyramid

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tiler.py <input.tif>")
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_file = input_file.replace(".tif", "_tiled.tif")
    
    print(f"Building pyramid for {input_file}...")
    build_pyramid(input_file, output_file)
    print(f"Done! Output: {output_file}")
