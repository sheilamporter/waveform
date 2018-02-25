import tkinter
from tkinter import messagebox
import os.path

from dev import *
from errors import *
from filewriter import *
from inputwindow import *
from wavebuilder import *

INPUT_ERROR_TITLE = "Input Error"

class App:
    def __init__(self):
        self.tkRoot = tkinter.Tk()
        self.inputWindow = InputWindow(self, self.tkRoot)
        self.waveBuilder = WaveBuilder()
        self.fileWriter = FileWriter()
        
    def start(self):
        self.tkRoot.mainloop()
        
    def generate(self):
        try:
            self.processInput()
            self.waveBuilder.buildWave()
            self.fileWriter.writeFile(self.waveBuilder.wave, self.waveBuilder.amplitude, 1 / self.waveBuilder.duration)
        except (InputError, WaveGenerationError, UserCancelled):
            pass
            
    def processInput(self):
    
        debug("------------------------------------------------------")
        debug("App.processInput()")
    
        # start with a clean slate
        self.waveBuilder.clear()
        self.fileWriter.clear()
    
        maxTime = 0
        for inputRow in self.inputWindow.inputRows:
            # grab text from entry widgets
            xText = inputRow.x.get()
            yText = inputRow.y.get()
            
            # if both entires are empty, just skip the row
            if not xText and not yText:
                debug("-empty row-")
                continue
            
            # if there is at least one entry filled out, make sure both are valid numbers and send to wavebuilder
            try:
                time = float(xText)
                temp = float(yText)
                maxTime = max(time, maxTime)
                self.waveBuilder.appendSample(time, temp)
                debug(self.waveBuilder.input[-1])
            except ValueError:
                messagebox.showerror(INPUT_ERROR_TITLE, "Invalid input in row " + str(int(inputRow.label["text"])) + ". Please only use numbers and provide values for both time and temperature.")
                error("Invalid input in row " + str(int(inputRow.label["text"])))
                raise InputError
                
        durationText = self.inputWindow.durationEntry.get()
        try:
            duration = float(durationText)
            self.waveBuilder.duration = duration
            debug("duration: " + str(duration))
        except ValueError:
            messagebox.showerror(INPUT_ERROR_TITLE, "Please specify a test length.")
            error("Invalid or missing duration.")
            raise InputError
            
        # make sure duration is at least as big as the highest timestamp
        if maxTime > self.waveBuilder.duration:
            messagebox.showerror(INPUT_ERROR_TITLE, "Please ensure that all time values are less than or equal to the test duration.")
            error("duration smaller than biggest timestamp")
            raise InputError
            
        # grab filename
        filename = self.inputWindow.outputFilenameEntry.get()
        if not filename:
            messagebox.showerror(INPUT_ERROR_TITLE, "Please specify an output filename.")
            error("Invalid output filename, please make sure you put something in there.")
            
        # stick a file extension on if it doesn't have one
        debug("filename: " + filename)
        filename = sanitizePath(filename)
        debug("sanitized filename: " + filename)
            
        if os.path.isfile(filename):
            debug("output file already exists")
            overwrite = messagebox.askyesno("Confirm File Overwrite", "The file " + filename + " already exists. Do you want to overwrite it?")
            if not overwrite:
                raise UserCancelled
        
        self.fileWriter.filename = filename
            
        debug("------------------------------------------------------")
        
if __name__ == "__main__":
    app = App()
    app.start()