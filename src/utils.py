import os
import re
import tkinter as tk
from tkinter import filedialog

def get_job_dir(output_dir, desc=None):
    """
    Finds the next job directory index under output_dir.
    Job folders are expected to follow the pattern 'job_<index>'.

    Args:
        output_dir (str): The base directory containing job folders.

    Returns:
        str: Absolute path to the next job directory.
    """
    job_pattern = re.compile(r'^job_(\d+)(_[\w]+)?$')
    max_index = -1

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for entry in os.listdir(output_dir):
        full_path = os.path.join(output_dir, entry)
        if os.path.isdir(full_path):
            match = job_pattern.match(entry)
            if match:
                idx = int(match.group(1))
                max_index = max(max_index, idx)

    next_index = max_index + 1
    next_job_name = f"job_{next_index:03d}"
    if desc is not None:
        next_job_name += f"_{desc}"
    return os.path.abspath(os.path.join(output_dir, next_job_name))

def select_file():
    """
    Opens a tk inter file dialog

    Returns:
        str[]: Array of selected absolute file paths
    """
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.iconify()
    file_path = filedialog.askopenfilenames(
        title="Select a file",
        filetypes=[("All Files", "*.*")]  # You can customize filters
    )
    root.destroy()
    return file_path

