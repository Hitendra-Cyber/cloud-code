import os


def get_files_info(working_directory: str, directory: str = ".") -> str | None:
    try:
        new_list = []
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        # Will be True or False
        valid_target_dir = (os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs)
    
        if valid_target_dir == False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
        if not os.path.isdir(target_dir):
            return f'Error: "{target_dir}" is not a directory'
    
        if os.path.isdir(target_dir):
            # return f'Success: "{directory}" is within the working directory'
            for item in os.listdir(target_dir):
                item_path = os.path.join(target_dir, item)
        
                new_list.append(f"- {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}")

            return str(new_list)
        

    except:
        raise Exception("Error: Failed to fetch file information")
        return




schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
