import os.path

from config import *

def formatTime(time):
    # adapted from https://stackoverflow.com/questions/9910972/python-number-of-digits-in-exponent
    s = "{0:.6e}".format(time)
    mantissa, exp = s.split('e')
    return "{0}e+{1:03d}".format(mantissa, int(exp))
        
def formatVoltage(voltage):
    return "{0:.5f}".format(voltage)
    
def sanitizePath(filepath):
    sanitizedPath = os.path.abspath(filepath)
    if not sanitizedPath.endswith(OUTPUT_FILE_EXTENSION):
        sanitizedPath += OUTPUT_FILE_EXTENSION
    return sanitizedPath