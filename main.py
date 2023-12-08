import subprocess
import os
import sys

# Specify the full path to the Python executable and the script
python_executable = sys.executable  # replace with the actual path
script_path = fr'{os.path.dirname(os.path.abspath(__file__))}\music_player.py'  # replace with the actual path

invisible_script_command = [python_executable, script_path]

subprocess.Popen(invisible_script_command, creationflags=subprocess.CREATE_NO_WINDOW)
