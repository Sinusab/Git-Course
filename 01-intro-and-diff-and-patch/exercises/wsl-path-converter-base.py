import os
import re

dir_add = input("Enter directory path: ").strip("'\"")

# Convert Windows path to WSL path
if re.match(r"^[a-zA-Z]:[/\\]", dir_add):
    drive = dir_add[0].lower()
    rest = dir_add[2:].replace("\\", "/")
    dir_add = f"/mnt/{drive}{rest}"
    print(f"Converted to: {dir_add}")

try:
    contents = os.listdir(dir_add)
    print("\n".join(contents))
except FileNotFoundError:
    print(f"Directory not found: {dir_add}")
except PermissionError:
    print(f"Permission denied: {dir_add}")
