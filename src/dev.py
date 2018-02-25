from config import *

def debug(text, end="\n"):
    if PRINT_DEBUG:
        print(text, end=end)

def error(text, end="\n"):
    if PRINT_ERROR:
        print("[ERROR] " + text, end=end)