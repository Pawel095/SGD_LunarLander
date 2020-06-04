import subprocess
import os
import shutil
import sys

path = os.getcwd() + "\\assets"
if sys.platform.startswith("win32"):
    path = os.getcwd() + "\\assets"
elif sys.platform.startswith("linux"):
    path = os.getcwd() + "/assets"
files = []
for r, d, f in os.walk(path):
    for file in f:
        files.append(os.path.join(r, file))

args = ["pyinstaller", "-F", "-w"]
args.append("main.py")
print(args)
subprocess.call(args)
try:
    if sys.platform.startswith("win32"):
        os.mkdir("dist\\assets\\")
    elif sys.platform.startswith("linux"):
        os.mkdir("dist/assets/")
except FileExistsError:
    pass

for f in files:
    if sys.platform.startswith("win32"):
        shutil.copy(f, "dist\\assets\\")
    elif sys.platform.startswith("linux"):
        shutil.copy(f, "dist/assets/")
