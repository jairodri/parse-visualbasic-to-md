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
    markdown_content = generate_markdown(parsed_data)

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Create the full path for the output Markdown file
    output_file_path = os.path.join(output_dir, 'documentacion_vb.md')

    # Write the Markdown content to the file in the specified output directory
    with open(output_file_path, 'w', encoding='utf-8') as md_file:
        md_file.write(markdown_content)