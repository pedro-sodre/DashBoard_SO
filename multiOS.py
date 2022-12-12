import platform
import subprocess
import re
import os


def get_slash():
    if platform.system() == "Windows":
        return "\\"
    elif platform.system() == "Linux":
        return "/"


def get_processor_name():
    if platform.system() == "Windows":
        return platform.processor()
    elif platform.system() == "Linux":
        command = "cat /proc/cpuinfo"
        all_info = subprocess.check_output(
            command, shell=True).decode().strip()
        for line in all_info.split("\n"):
            if "model name" in line:
                return re.sub(".*model name.*:", "", line, 1)
    return ""


def get_home_path():
    if platform.system() == "Windows":
        return os.path.expanduser("~")
    elif platform.system() == "Linux":
        return subprocess.check_output("echo ~", shell=True).decode().strip()
