from config import *
from dev import *
from sample import *
from util import *

class FileWriter():
    """Dumps the wave to a file."""
    
    def __init__(self):
        self.filename = None
        
    def clear(self):
        self.filename = None
    
    def writeFile(self, wave, amplitude, frequency):
    
        # start writing to file
        with open(self.filename, 'w') as file:
        
            debug("------------------------------------------------------")
            debug("FileWriter.writeFile()")
            
            frequency = "{0:.9f}".format(frequency)
            amplitude = "{0:.9f}".format(amplitude)
            offset = "{0:.9f}".format(OFFSET)
            phase = "{0:.9f}".format(PHASE)
            header = OUTPUT_BOILERPLATE.format(datalength=NUM_WAVE_SAMPLES, frequency=frequency, amplitude=amplitude, offset=offset, phase=phase)
            debug(header, end="")
            
            file.write(header)
            
            # write each sample to the file
            for sample in wave:
                time = formatTime(sample.time)
                voltage = formatVoltage(sample.voltage)
                line = str(time) + OUTPUT_DELIMETER + str(voltage) + "\n"
                file.write(line)
                debug(line, end="")
                
            debug("------------------------------------------------------")
                
        file.closed

# test code (run via filewritertest.bat)
if __name__ == "__main__":
    testwave = []
    testwave.append(Sample(0, 5, 5))
    testwave.append(Sample(5, 10, 10))
    testwave.append(Sample(10, 15, 15))
    testwave.append(Sample(15, 10, 10))
    testwave.append(Sample(20, 5, 5))
    
    fileWriter = FileWriter()
    fileWriter.filename = "filewritertestoutput.csv"
    fileWriter.writeFile(testwave, 30, 1/20)