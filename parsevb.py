import os
import re

def parse_vb_file(file_path):
    """
    Parses a Visual Basic code file to extract the full definitions of functions and subroutines.

    This function reads a VB file and identifies the full lines of function and subroutine 
    declarations, preserving the order in which they appear in the code. It handles optional 
    access modifiers like 'Public', 'Private', and 'Friend' that may precede function and 
    subroutine declarations.

    Args:
        file_path (str): The path to the VB file to parse.

    Returns:
        list: A list containing the full definitions of functions and subroutines as they appear 
        in the VB6 file.
    """
    with open(file_path, 'r', encoding='latin-1') as file:
        code = file.readlines()

    definitions = []

    # Regular expressions updated to detect full function and subroutine definitions
    function_regex = re.compile(r'^(Public |Private |Friend )?Function .+', re.IGNORECASE)
    sub_regex = re.compile(r'^(Public |Private |Friend )?Sub .+', re.IGNORECASE)

    for line in code:
        line = line.strip()

        # Detect full function and subroutine definitions with optional modifiers
        if function_regex.match(line):
            # Add the full function definition to the list
            definitions.append(line)
        elif sub_regex.match(line):
            # Add the full subroutine definition to the list
            definitions.append(line)

    return definitions


def parse_directory(directory):
    """
    Parses all Visual Basic (VB) files within a specified directory to extract functions,
    subroutines, and calls.

    This function traverses a given directory recursively, looking for VB files with the 
    extensions '.frm', '.bas', and '.cls'. It uses the parse_vb_file function to extract 
    information from each file and collects this data into a dictionary.

    Args:
        directory (str): The path to the directory containing VB6 files to parse.

    Returns:
        dict: A dictionary where each key is a filename and each value is the parsed data from 
        that file.
    """
    parsed_data = {}

    # Traverse the directory and its subdirectories
    for root, _, files in os.walk(directory):
        for file in files:
            # Check if the file has a VB-related extension
            if file.endswith('.frm') or file.endswith('.bas') or file.endswith('.cls'):
                file_path = os.path.join(root, file)
                # Parse the VB file and store its parsed data
                parsed_data[file] = parse_vb_file(file_path)

    return parsed_data


def generate_markdown(parsed_data):
    """
    Generates a markdown representation from the parsed Visual Basic files data.

    This function takes the parsed data from VB files and generates markdown content 
    that includes the full definitions of functions and subroutines as they appear 
    in the original files.

    Args:
        parsed_data (dict): A dictionary where each key is a filename and each value is a list 
        of definitions (functions and subroutines) extracted from that file.

    Returns:
        str: A string containing the markdown content representing the parsed VB files data.
    """
    md_content = []

    for file, definitions in parsed_data.items():
        md_content.append(f"# {file}\n")
        md_content.append("## Definitions\n")

        for definition in definitions:
            md_content.append(f"- {definition}")
        
        md_content.append("\n")

    return "\n".join(md_content)


