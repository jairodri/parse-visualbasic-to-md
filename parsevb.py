import re
import os

def parse_vb_file(file_path):
    """
    Parses a Visual Basic code file to extract the full definitions of functions, subroutines, 
    variables, and calls.

    This function reads a VB file and identifies the full lines of function and subroutine 
    declarations, as well as variable declarations using 'Dim' and calls using 'Call'. 
    It distinguishes between variables declared at the module level (global to the file) and 
    those declared inside functions or subroutines (local).

    Args:
        file_path (str): The path to the VB file to parse.

    Returns:
        dict: A dictionary containing:
            - 'module_level_vars': A list of variable declarations at the module level.
            - 'definitions': A list of dictionaries, each containing:
                - 'type': The type of definition ('Function' or 'Sub').
                - 'definition': The full definition line of the function or subroutine.
                - 'local_vars': A list of variable declarations inside the function or subroutine.
                - 'calls': A list of calls inside the function or subroutine.
    """
    with open(file_path, 'r', encoding='latin-1') as file:
        code = file.readlines()

    module_level_vars = []
    definitions = []
    current_definition = None

    # Regular expressions to detect full function and subroutine definitions, variable declarations, and calls
    function_regex = re.compile(r'^(Public |Private )?Function .+', re.IGNORECASE)
    sub_regex = re.compile(r'^(Public |Private )?Sub .+', re.IGNORECASE)
    dim_regex = re.compile(r'^\s*Dim\s+\w+', re.IGNORECASE)
    call_regex = re.compile(r'^\s*Call\s+\w+', re.IGNORECASE)

    for line in code:
        line = line.strip()

        # Check for variable declarations
        if dim_regex.match(line):
            if current_definition:
                # We are inside a function or subroutine, so add to local variables
                current_definition['local_vars'].append(line)
            else:
                # We are at the module level
                module_level_vars.append(line)

        # Check for calls
        elif call_regex.match(line):
            if current_definition:
                # We are inside a function or subroutine, so add to calls
                current_definition['calls'].append(line)
        
        # Detect full function and subroutine definitions with optional modifiers
        elif function_regex.match(line) or sub_regex.match(line):
            if current_definition:
                # If we are already inside a definition, save the current one
                definitions.append(current_definition)
            
            # Start a new function or subroutine definition
            current_definition = {
                'type': 'Function' if function_regex.match(line) else 'Sub',
                'definition': line,
                'local_vars': [],
                'calls': []  # Initialize calls list for the current definition
            }
    
    # If we end with a definition still open, add it to the list
    if current_definition:
        definitions.append(current_definition)

    return {
        'module_level_vars': module_level_vars,
        'definitions': definitions
    }


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
    that includes the module-level variable declarations, function and subroutine 
    definitions, local variable declarations inside those functions and subroutines, 
    and calls made within those functions and subroutines.

    Args:
        parsed_data (dict): A dictionary where each key is a filename and each value is a 
        dictionary containing:
            - 'module_level_vars': A list of variable declarations at the module level.
            - 'definitions': A list of dictionaries, each containing:
                - 'type': The type of definition ('Function' or 'Sub').
                - 'definition': The full definition line of the function or subroutine.
                - 'local_vars': A list of variable declarations inside the function or subroutine.
                - 'calls': A list of calls inside the function or subroutine.

    Returns:
        str: A string containing the markdown content representing the parsed VB files data.
    """
    md_content = []

    for file, data in parsed_data.items():
        md_content.append(f"# {file}\n")
        
        # Add module-level variables
        if data['module_level_vars']:
            md_content.append("## Module Level Variables\n")
            for var in data['module_level_vars']:
                md_content.append(f"- {var}")
            md_content.append("\n")

        # Add function and subroutine definitions
        md_content.append("## Definitions\n")
        for definition in data['definitions']:
            md_content.append(f"- **{definition['type']}**: {definition['definition']}")
            
            # Add local variables with increased indentation
            if definition['local_vars']:
                md_content.append("  - **Local Variables**:")
                for local_var in definition['local_vars']:
                    md_content.append(f"    - {local_var}")
            
            # Add calls with increased indentation
            if definition['calls']:
                md_content.append("  - **Calls**:")
                for call in definition['calls']:
                    md_content.append(f"    - {call}")
            
            md_content.append("\n")
    
    return "\n".join(md_content)

