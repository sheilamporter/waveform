import os.path
from tkinter import *
from tkinter import filedialog

import app
from config import *
from dev import *
from util import *

PADDING = 5

class InputRow:
    def __init__(self, label, xEntry, yEntry):
        self.label = label
        self.x = xEntry
        self.y = yEntry

class InputWindow:
    def __init__(self, app, tkMaster):
        self.app = app
        self.tkMaster = tkMaster
        self.initialdir = OUTPUT_DEFAULT_DIRECTORY
        
        tkMaster.winfo_toplevel().title("Waveform Generator")
        
        self.inputRows = []
        
        self.inputFrame = Frame(height=20, borderwidth=3, relief=RAISED)
        
        self.inputLabel = Label(self.inputFrame, text="Input Table")
        self.xColumnLabel = Label(self.inputFrame, text="Time (Seconds)")
        self.yColumnLabel = Label(self.inputFrame, text="Temperature (°C)")
        
        for row in range(STARTING_NUM_INPUT_ROWS):
            self.buildNewRow()
            
        self.inputRows[0].x.focus_set()
            
        self.addRowButton = Button(self.inputFrame, text="+", takefocus=0, command=self.addRow)
        self.removeRowButton = Button(self.inputFrame, text="-", takefocus=0, command=self.removeRow)
        
        self.outputFrame = Frame(height=20, borderwidth=3, relief=FLAT)
        
        self.durationLabel = Label(self.outputFrame, text="Test Length (Seconds):")
        self.durationEntry = Entry(self.outputFrame)
        
        self.outputFilenameLabel = Label(self.outputFrame, text="Output Filename:")
        
        self.outputFilenameEntry = Entry(self.outputFrame)
        
        self.browseButton = Button(self.outputFrame, text="...", command=self.browse)
        
        self.generateButton = Button(self.outputFrame, text="Generate Waveform", command=self.generate)
        
        self.progressText = StringVar()
        self.progressLabel = Label(self.outputFrame, textvariable=self.progressText)
        self.progressText.set("")
        
        self.layout()
        
    def buildNewRow(self):
        row = len(self.inputRows) + 1
        prefix = ""
        if row < 10:
            prefix = "  "
        rowText = prefix + str(row)
        label = Label(self.inputFrame, text=rowText)
        xEntry = Entry(self.inputFrame)
        yEntry = Entry(self.inputFrame)
        self.inputRows.append(InputRow(label, xEntry, yEntry))
        
    def layout(self):
        row = 0
        self.inputLabel.grid(row=row, columnspan=4, pady=PADDING, sticky=W+E)
        row += 1
        self.xColumnLabel.grid(row=row, column=1)
        self.yColumnLabel.grid(row=row, column=2)
        self.addRowButton.grid(row=row, column=3, padx=(PADDING,0))
        self.removeRowButton.grid(row=row, column=4, padx=(0,PADDING))
        
        for index in range(len(self.inputRows)):
            inputRow = self.inputRows[index]
            bottomPad = 0
            if index == len(self.inputRows) - 1:
                bottomPad = PADDING
            row += 1
            inputRow.label.grid(row=row, column=0, padx=PADDING, pady=(0, bottomPad), sticky=E)
            inputRow.x.grid(row=row, column=1, pady=(0, bottomPad))
            inputRow.y.grid(row=row, column=2, pady=(0, bottomPad))
            
        self.inputFrame.grid(row=0, column=0, padx=PADDING, pady=PADDING, sticky=N+W+E+S)
        
        row = 0
        
        self.durationLabel.grid(row=row, column=0, padx=PADDING, pady=PADDING, sticky=E)
        self.durationEntry.grid(row=row, column=1, columnspan=2, padx=PADDING, pady=PADDING, sticky=W+E)
        row += 1
        
        self.outputFilenameLabel.grid(row=row, column=0, padx=PADDING, pady=PADDING, sticky=E)
        self.outputFilenameEntry.grid(row=row, column=1, padx=(PADDING, 0), pady=PADDING, sticky=W+E)
        self.browseButton.grid(row=row, column=2, padx=(0, PADDING), pady=PADDING, sticky=W+E)
        row += 1
        
        self.generateButton.grid(row=row, column=0, columnspan=3, padx=PADDING, pady=PADDING, sticky=W+E)
        row += 1
        
        self.progressLabel.grid(row=row, column=0, columnspan=3, padx=PADDING, pady=PADDING, sticky=W+E)
        
        self.outputFrame.grid(row=0, column=1, padx=PADDING, pady=PADDING, sticky=N+W+E+S)
        
    def addRow(self):
        self.buildNewRow()
        self.layout()
        
    def removeRow(self):
        if not self.inputRows or len(self.inputRows) <= 1:
            return
        row = self.inputRows.pop()
        row.label.destroy()
        row.x.destroy()
        row.y.destroy()
        self.layout()
        
    def generate(self):
        if not self.app:
            error("no app defined; cannot generate")
            return
        self.app.generate()
        self.progressText.set("Done.")
        
    def browse(self):
        # pull up file dialog
        filepath = filedialog.asksaveasfilename(initialdir=self.initialdir, title="Output File", filetypes=(("CSV files", "*.csv"), ("All Files", "*")))
        # if user hits "cancel" button, an empty string is returned - do nothing
        if filepath == "":
            debug("cancelled")
            return
        # sanitize returned path and put it in the text entry
        filepath = sanitizePath(filepath)
        debug(filepath)
        self.outputFilenameEntry.delete(0, END)
        self.outputFilenameEntry.insert(0, filepath)
        # cache the chosen directory for next time
        self.initialdir = os.path.dirname(filepath)

# test code (run via inputwindowtest.bat)        
if __name__ == "__main__":
    root = Tk()
    inputWindow = InputWindow(None, root)
    root.mainloop()