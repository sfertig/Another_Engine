import subprocess
import shutil
import sys
import os
from ..Net import Net


def get_python_command():
    # Check if 'python' or 'python3' is available in the system PATH
    for cmd in ["python", "python3", "py"]:
        if shutil.which(cmd):
            return cmd
    return None

def Runner(project_name):
    python_path = os.path.join(Net.save_dir, project_name)
    path = os.path.join(python_path, "build.py")
    
    python_cmd = get_python_command()
    
    if not python_cmd:
        print("[Runner Error] - Python is not installed or not found in system PATH!")
        # TODO: Trigger a UI popup or warning to the user here!
        return

    # Use the system Python interpreter found on the user's machine
    subprocess.Popen(
        [python_cmd, "-Xfrozen_modules=off", path],
        cwd=python_path,
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

    print("[Runner] - Project running: " + project_name)