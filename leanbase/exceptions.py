class LeanbaseException(Exception):
    pass

class BadConfigurationException(LeanbaseException):
    def __init__(self, message):
        self.message = message

class ReconfigurationException(LeanbaseException):
    pass