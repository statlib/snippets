import base64
import sys
import zipfile
import os

def encode_file_to_base64_chunks_zip(input_file_path, output_file_base, max_size_mb=45):
    max_chunk_size = int((max_size_mb * 1024 * 1024) * 3 / 4)  # Calculating max bytes per chunk

    try:
        with open(input_file_path, 'rb') as input_file:
            binary_data = input_file.read()

        base64_encoded_data = base64.b64encode(binary_data)

        for i in range(0, len(base64_encoded_data), max_chunk_size):
            chunk = base64_encoded_data[i:i+max_chunk_size]
            part_num = i // max_chunk_size + 1
            zip_filename = f"{output_file_base}_{part_num}.zip"
            output_filename = f"{part_num}.txt"

            # Write the chunk to a zip file
            with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.writestr(output_filename, chunk)

            print(f"Chunk {part_num} written to {zip_filename}")

    except IOError as e:
        print(f"IOError: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py [input_file] [output_file_base]")
    else:
        input_file = sys.argv[1]
        output_file_base = sys.argv[2]
        encode_file_to_base64_chunks_zip(input_file, output_file_base)
