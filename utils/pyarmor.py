import os
from pathlib import Path
import platform 
import sys
def load_pyarmor_runtime():
 
    operating_system = platform.system().lower()
    root = Path(__file__).resolve().parent.parent
    py_armor_folder = os.path.join(root, 'runtimes', f"{operating_system}")
    sys.path.insert(0, py_armor_folder)

# Use runtime
load_pyarmor_runtime()
