import os
from dotenv import load_dotenv
from parsevb import parse_directory, generate_markdown


# Load variables from the .env file
load_dotenv()

# Get the directory path to the visual basic code
vb_code_path = os.getenv('VB_CODE_PATH')

if __name__ == '__main__':
    parsed_data = parse_directory(vb_code_path)
    markdown_content = generate_markdown(parsed_data)
    with open('documentacion_vb.md', 'w', encoding='utf-8') as md_file:
        md_file.write(markdown_content)