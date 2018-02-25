class InputError(Exception):
    def __init__(self):
        self.message = "Error in wave generator input."
    
class WaveGenerationError(Exception):
    def __init__(self):
        self.message = "Error in wave generation calculations"
    
class UserCancelled(Exception):
    def __init__(self):
        self.message = "User chose to cancel wave generation."
