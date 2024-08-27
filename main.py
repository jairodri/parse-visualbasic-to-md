import os
from dotenv import load_dotenv
from parsevb import parse_directory, generate_markdown


# Load variables from the .env file
load_dotenv()

# Get the directory path to the visual basic code and the output directory
vb_code_path = os.getenv('VB_CODE_PATH')
output_dir = os.getenv('OUTPUT_DIR')

if __name__ == '__main__':
    parsed_data = parse_directory(vb_code_path)
    generate_markdown(parsed_data, output_dir)  