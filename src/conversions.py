from config import *
from dev import *

def convertTempToVoltage(temp):
    #Converts temperature into corresponding thermocouple reference voltage.  Source: https://www.omega.com/techref/pdf/z198-201.pdf ; see Type B Thermoc qouples section.
    #Output of these polynomials are in microvolts.  Thermocouple reference tables are in milivolts.  Amp gain from thermocouple driver hardware is 1000x.  Therefore, multiplying polynomial output by 1000 provides V scale output from signal generator and a proper match to TC reference voltage.
    #Range 1: 0C to 630.615C
    if temp >= 0 and temp < 630.615:
        debug("[case 1] ", end="")
        return GAIN * (temp * -2.4650818346e-1 + temp**2 * 5.9040421171e-3 + temp**3 * -1.3257931636e-6 + temp**4 * 1.5668291901e-9 + temp**5 * -1.6944529240e-12 + temp**6 * 6.2290347094e-16)
    #Range 2: 630.615C to 1820C
    if temp >= 630.615 and temp <= 1820:
        debug("[case 2] ", end="")
        return GAIN * (-3.8938168621e3 + temp * 2.8571747470e1 + temp**2 * -8.4885104785e-2 + temp**3 * 1.5785280164e-4 + temp**4 * -1.6835344864e-7 + temp**5 * 1.1109794013e-10 + temp**6 * -4.4515431033e-14 + temp**7 * 9.8975640821e-18 + temp**8 * -9.3791330289e-22)
    error("temp " + str(temp) + " not within valid range - must be between 0 and 1820 degrees Celcius")
    return 0