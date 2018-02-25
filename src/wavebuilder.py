import tkinter
from tkinter import messagebox

from config import *
from conversions import *
from dev import *
from sample import *
from util import *

# number of samples to generate (constant, regardless of wave duration)
NUM_SAMPLES = NUM_WAVE_SAMPLES

CLAMP_WARNING_TITLE = "Value Clamped"
CLAMP_WARNING_QUESTION = "\n\nDo you want to be notified of future clamped values?"

class WaveBuilder:
    """Takes a bunch of input and builds a wave out of it with some math and whatever."""
    
    def __init__(self):
        self.input = []
        self.duration = None
        self.wave = []
        self.amplitude = None
        self.showClampWarnings = True
        
    def clear(self):
        self.input = []
        self.duration = None
        self.wave = []
        self.amplitude = None
        self.showClampWarnings = True
        
    def appendSample(self, time, temp):
        self.input.append(Sample(time=time, temp=temp))
    
    def buildWave(self):
    
        debug("------------------------------------------------------")
        debug("WaveBuilder.buildWave()\n")
        
        if not self.input:
            error("no input specified")
            return
    
        debug("input:")
        for data in self.input:
            debug(data)
        debug("")
        
        # sort the data according to time
        self.input.sort(key=Sample.sortKey)
        
        # make sure we start and end at zero
        if self.input[0].time != 0:
            self.input.insert(0, Sample(0, 0))
        if self.input[-1].time != self.duration:
            self.input.append(Sample(self.duration, 0))
        
        debug("sorted input:")
        for data in self.input:
            debug(data)
        debug("")
        
        debug("self.wave:")
        
        # mise en place
        self.wave = []
        timeInterval = self.duration / (NUM_SAMPLES - 1)
        debug("timeInterval: " + str(timeInterval))
        prevInputIndex = 0
        nextInputIndex = 1
        currTime = 0.0
        maxVoltage = 0
        
        # generate samples by linearly interpolating between input points
        for sampleIndex in range(NUM_SAMPLES):
        
            # check if we've reached the next input point
            # second condition keeps us from running off the end of the input list
            # if floating point precision means the final sample is actually slightly higer than the specified duration
            if currTime > self.input[nextInputIndex].time and nextInputIndex <= len(self.input) - 2:
                prevInputIndex = nextInputIndex
                nextInputIndex = prevInputIndex + 1

            # do some fancy interpolating, calculate the corresponding voltage, and shove it in the self.wave
            prevInputTime = self.input[prevInputIndex].time
            prevInputTemp = self.input[prevInputIndex].temp
            nextInputTime = self.input[nextInputIndex].time
            nextInputTemp = self.input[nextInputIndex].temp
            interpolatedTemp = ((nextInputTemp - prevInputTemp) / (nextInputTime - prevInputTime)) * (currTime - prevInputTime) + prevInputTemp
            
            # make sure we never go below 0 because that won't happen in the lab and it'll break the voltage conversion
            clampedInterpolatedTemp = max(interpolatedTemp, MIN_TEMP)
            if interpolatedTemp != clampedInterpolatedTemp:
                debug("raised temp from " + str(interpolatedTemp) + " to minimum " + str(clampedInterpolatedTemp))
                if self.showClampWarnings:
                    self.showClampWarnings = messagebox.askyesno(CLAMP_WARNING_TITLE, "Interpolated temperature for sample " + str(sampleIndex+1) + " at " + formatTime(currTime) + " seconds was " + formatVoltage(interpolatedTemp) + " - clamped to " + formatVoltage(clampedInterpolatedTemp) + "." + CLAMP_WARNING_QUESTION)
                
            
            # calculate corresponding voltage and clamp to what the machine can actually do
            voltage = convertTempToVoltage(interpolatedTemp)
            clampedVoltage = max(MIN_VOLTAGE, min(MAX_VOLTAGE, voltage))
            if voltage != clampedVoltage:
                debug("clamped voltage from " + str(voltage) + " to " + str(clampedVoltage))
                if self.showClampWarnings:
                    self.showClampWarnings = messagebox.askyesno(CLAMP_WARNING_TITLE, "Calculated voltage for sample " + str(sampleIndex+1) + " at " + formatTime(currTime) + " seconds was " + formatVoltage(voltage) + " - clamped to " + formatVoltage(clampedVoltage) + "." + CLAMP_WARNING_QUESTION)
            
            self.wave.append(Sample(currTime, clampedInterpolatedTemp, clampedVoltage))
            
            maxVoltage = max(voltage, maxVoltage)
            
            debug("   " + str(sampleIndex + 1) + ": " + str(self.wave[-1]))
            currTime += timeInterval
            
        self.amplitude = 2 * maxVoltage
            
        debug("\namplitude: " + str(self.amplitude))
        debug("total samples: " + str(len(self.wave)))
        debug("------------------------------------------------------")
        
        if len(self.wave) != NUM_SAMPLES:
            messagebox.showerror("Error", "Wave generation error: should have generated " + str(NUM_SAMPLES) + " samples, but only generated " + str(len(self.wave)) + ".")
            error("problem with math - did not generate right number of samples. go yell at sheila.")

# test code (run via wavebuildertest.bat)
if __name__ == "__main__":

    # so we don't go crazy trying to verify our test self.wave
    #NUM_SAMPLES = 40

    waveBuilder = WaveBuilder()
    
    waveBuilder.appendSample(0, 0)
    waveBuilder.appendSample(10, 500)
    waveBuilder.duration = 20
    
    waveBuilder.buildWave()
   