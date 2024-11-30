import gradio as gr
import subprocess
import shlex
import os

def run_local_command(command):
    """
    Safely execute a local shell command with restricted permissions.
    
    Args:
        command (str): The command to be executed
    
    Returns:
        str: Command output or error message
    """
    # List of allowed commands (you can modify this list)
    allowed_commands = [
        'ls', 'pwd', 'whoami', 'date', 'cal', 
        'echo', 'cat', 'head', 'tail', 
        'grep', 'wc', 'find'
    ]
    
    # Extract the base command (first word)
    base_command = command.split()[0] if command else ''
    
    # Check if the command is allowed
    if base_command not in allowed_commands:
        return f"Command '{base_command}' is not in the list of allowed commands."
    
    try:
        # Use shlex.split to properly handle command arguments with spaces
        args = shlex.split(command)
        
        # Run the command and capture output
        result = subprocess.run(
            args, 
            capture_output=True, 
            text=True, 
            timeout=10,  # Prevent long-running commands
            cwd=os.path.expanduser('~')  # Run in user's home directory
        )
        
        # Combine stdout and stderr for full output
        if result.returncode == 0:
            return result.stdout or "Command executed successfully with no output."
        else:
            return f"Error (Exit Code {result.returncode}):\n{result.stderr}"
    
    except subprocess.TimeoutExpired:
        return "Command timed out. Execution took too long."
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Create Gradio interface
demo = gr.Interface(
    fn=run_local_command,
    inputs=gr.Textbox(
        label="Enter Command", 
        placeholder="Only allowed commands: ls, pwd, whoami, date, cal, echo, cat, head, tail, grep, wc, find"
    ),
    outputs=gr.Textbox(label="Command Output"),
    title="Local Command Runner",
    description="Run local shell commands with restricted permissions. Only specific safe commands are allowed."
)

# Launch the app locally
if __name__ == "__main__":
    demo.launch(
        server_name='127.0.0.1',  # Bind to localhost only
        server_port=80,  # Specify a port
        share=False  # Disable public sharing
    )
