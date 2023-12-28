import base64
import sys
import zipfile
import os

def reconstruct_from_chunks_zip(output_file_base, reconstructed_filename):
    # Assuming the parts are numbered sequentially and exist in the current directory
    part_num = 1
    base64_encoded_data = b''

    while True:
        zip_filename = f"{output_file_base}_{part_num}.zip"
        if not os.path.exists(zip_filename):
            break  # Exit loop if the part doesn't exist

        # Extract and concatenate base64 encoded data
        with zipfile.ZipFile(zip_filename, 'r') as zipf:
            # Assuming there's only one file per zip and it's named consistently
            for fileinfo in zipf.infolist():
                print(fileinfo)
                with zipf.open(fileinfo) as chunk_file:
                    base64_encoded_data += chunk_file.read()

        part_num += 1

    # Decode the concatenated base64 data back into binary
    binary_data = base64.b64decode(base64_encoded_data)

    # Write the binary data to the reconstructed file
    with open(reconstructed_filename, 'wb') as reconstructed_file:
        reconstructed_file.write(binary_data)

    print(f"Reconstructed file written to {reconstructed_filename}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py [output_file_base] [reconstructed_filename]")
    else:
        output_file_base = sys.argv[1]
        reconstructed_filename = sys.argv[2]
        reconstruct_from_chunks_zip(output_file_base, reconstructed_filename)
