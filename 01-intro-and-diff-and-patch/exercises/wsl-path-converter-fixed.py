import os
import re

dir_add = input("Enter directory path: ").strip("'\"")

# Convert //wsl.localhost/<distro>/... → /...
unc_match = re.match(r"^//wsl\.localhost/[^/]+(/.*)", dir_add, re.IGNORECASE)
if unc_match:
    dir_add = unc_match.group(1)
    print(f"Converted UNC to: {dir_add}")

# Convert Windows drive paths C:\... → /mnt/c/...
elif re.match(r"^[a-zA-Z]:[/\\]", dir_add):
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
