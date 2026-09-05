import os

from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str :
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        # Will be True or False
        valid_target_dir = (os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs)

        if not valid_target_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_dir):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_dir, 'r') as file_dir:
            file_content = file_dir.read(MAX_CHARS)
            if file_dir.read(1):
                file_content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return file_content



    except:
        return f"Error: Failed to fetch file information"



schema_get_file_content = {
    "type": "function",
        "function": {
            "name": "get_file_content",
            "description": "Read file contents",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the file to read, relative to the working directory.",
                    },
                },
                "required": ["file_path"],
            },
        },
}