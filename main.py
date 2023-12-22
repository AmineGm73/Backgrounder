import subprocess
import os

import shutil
from json_m import Operation, json_file

# Specify the full path to the Python executable and the script
python_executable = shutil.which("python")  # replace with the actual path
music_player_path = fr'{os.path.dirname(os.path.abspath(__file__))}\music_player.py'
config_script_path = fr'{os.path.dirname(os.path.abspath(__file__))}\config.py'

app = {
    "app_path": os.path.dirname(os.path.abspath(__file__)),
    "music_player_script_path": music_player_path,
    "config_script_path": config_script_path,
    "python": python_executable
}

json_file("config.json",Operation.CHANGE, "app", app)

invisible_script_command = [python_executable, music_player_path]

subprocess.Popen(invisible_script_command, creationflags=subprocess.CREATE_NO_WINDOW)
