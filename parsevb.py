import os
import re

def parse_vb_file(file_path):
    """
    Parses a Visual Basic code file to extract functions, subroutines, 
    and calls.

    This function reads a VB file, identifies and extracts the names of 
    functions, subroutines, and calls (procedures) defined in the code. It 
    handles optional access modifiers like 'Public', 'Private', and 'Friend' 
    that may precede function and subroutine declarations.

    Args:
        file_path (str): The path to the VB file to parse.

    Returns:
        dict: A dictionary containing three lists:
            - 'functions': A list of function names defined in the VB6 file.
            - 'subs': A list of subroutine names defined in the VB6 file.
            - 'calls': A list of function or subroutine calls found in the VB6 file.
    """
    with open(file_path, 'r', encoding='latin-1') as file:
        code = file.readlines()

    functions = []
    subs = []
    calls = []

    # Regular expression updated to detect functions and subroutines with optional access modifiers
    function_regex = re.compile(r'^(Public |Private |Friend )?Function (\w+)', re.IGNORECASE)
    sub_regex = re.compile(r'^(Public |Private |Friend )?Sub (\w+)', re.IGNORECASE)
    call_regex = re.compile(r'^\s*Call (\w+)', re.IGNORECASE)

    for line in code:
        line = line.strip()

        # Detect functions and subroutines with optional modifiers
        func_match = function_regex.match(line)
        sub_match = sub_regex.match(line)
        call_match = call_regex.match(line)

        if func_match:
            # Capture the function name, which is the second group in the regular expression
            functions.append(func_match.group(2))
        elif sub_match:
            # Capture the subroutine name, which is the second group in the regular expression
            subs.append(sub_match.group(2))
        elif call_match:
            # Capture the name of the function or subroutine being called
            calls.append(call_match.group(1))

    return {
        'functions': functions,
        'subs': subs,
        'calls': calls
    }


def parse_directory(directory):
    """
    Parses all Visual Basic (VB) files within a specified directory to extract functions,
    subroutines, and calls.

    This function traverses a given directory recursively, looking for VB files with the 
    extensions '.frm', '.bas', and '.cls'. It uses the parse_vb6_file function to extract 
    information from each file and collects this data into a dictionary.

    Args:
        directory (str): The path to the directory containing VB6 files to parse.

    Returns:
        dict: A dictionary where each key is a filename and each value is the parsed data from 
        that file, including lists of functions, subroutines, and calls.
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

