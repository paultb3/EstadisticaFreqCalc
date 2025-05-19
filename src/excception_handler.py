"""
    ===================================================================================
    Codigo extraido de StatPhi.
    ===================================================================================
"""

class WarningException(Exception):
    def __init__(self, message):
        super().__init__(message)