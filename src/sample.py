class Sample:
    """Data object that represents a single data element."""

    def __init__(self, time=None, temp=None, voltage=None):
        self.time = time
        self.temp = temp
        self.voltage = voltage
    def __repr__(self):
        repr = "[time: "
        
        if self.time != None:
            repr += "{0:.2f}".format(self.time)
        else:
            repr += "---"
            
        repr += " temp: "
        if self.temp != None:
            repr += "{0:.2f}".format(self.temp)
        else:
            repr += "---"
            
        repr += " volt: "
        if self.voltage != None:
            repr += "{0:.2f}".format(self.voltage)
        else:
            repr += "---"  
            
        return repr + "]"
    def __str__(self):
        return self.__repr__()
    def sortKey(self):
        return self.time