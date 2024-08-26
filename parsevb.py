import os
import re

def parse_vb_file(file_path):
    with open(file_path, 'r', encoding='latin-1') as file:
        code = file.readlines()

    functions = []
    subs = []
    calls = []

    # Expresión regular actualizada para detectar funciones y subrutinas con modificadores de acceso opcionales
    function_regex = re.compile(r'^(Public |Private |Friend )?Function (\w+)', re.IGNORECASE)
    sub_regex = re.compile(r'^(Public |Private |Friend )?Sub (\w+)', re.IGNORECASE)
    call_regex = re.compile(r'^\s*Call (\w+)', re.IGNORECASE)

    for line in code:
        line = line.strip()

        # Detectar funciones y subrutinas con modificadores opcionales
        func_match = function_regex.match(line)
        sub_match = sub_regex.match(line)
        call_match = call_regex.match(line)

        if func_match:
            # Captura el nombre de la función, que es el segundo grupo en la expresión regular
            functions.append(func_match.group(2))
        elif sub_match:
            # Captura el nombre de la subrutina, que es el segundo grupo en la expresión regular
            subs.append(sub_match.group(2))
        elif call_match:
            # Captura el nombre de la función o subrutina llamada
            calls.append(call_match.group(1))

    return {
        'functions': functions,
        'subs': subs,
        'calls': calls
    }

def parse_directory(directory):
    parsed_data = {}

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.frm') or file.endswith('.bas') or file.endswith('.cls'):
                file_path = os.path.join(root, file)
                parsed_data[file] = parse_vb_file(file_path)

    return parsed_data


