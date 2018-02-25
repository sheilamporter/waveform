PRINT_DEBUG = True
PRINT_ERROR = True

STARTING_NUM_INPUT_ROWS = 5

GAIN = .001

NUM_WAVE_SAMPLES = 16384

MIN_TEMP = 0
MIN_VOLTAGE = -10
MAX_VOLTAGE = 10
OFFSET = 0
PHASE = 0

OUTPUT_DEFAULT_DIRECTORY = "."
OUTPUT_FILE_EXTENSION = ".csv"
OUTPUT_DELIMETER = ","
OUTPUT_BOILERPLATE = """data length,{datalength}
frequency,{frequency}
amp,{amplitude}
offset,{offset}
phase,{phase}







xpos,value
"""