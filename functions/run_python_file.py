import os
import subprocess

def run_python_file(working_directory: str, file_path: str , args: list[str] | None = None) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        # Will be True or False
        valid_target_dir = (os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs)
    
        if valid_target_dir == False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'
    
        if not target_dir.lower().endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
    
        command = ["python", target_dir]
        
        if args:
            command.extend(args)
    
        results = subprocess.run(command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30)

        output = []
        if results.returncode != 0:
            output.append(f"Process exited with code {results.returncode}")
        if not results.stdout and not results.stderr:
            output.append("No output produced")
        
        if results.stdout:
            output.append(f"STDOUT:\n{results.stdout}")
        if results.stderr:
            output.append(f"STDERR:\n{results.stderr}")
          
        return "\n".join(output)  
        
        

    except Exception as e:
        return f"Error: executing Python file: {e}"



schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a specified Python file or test suite relative to the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file or test file to run.",
                },
                "args": {
                    "type": "array",
                    "description": "Optional list of command-line arguments to pass to the script.",
                    "items": {
                        "type": "string",
                    },
                },
            },
            "required": ["file_path"],
        },
    },
}