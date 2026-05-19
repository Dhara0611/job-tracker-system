
class ValidationError(Exception):
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

"""
The built-in Exception class expects an error message string so it knows how to print the error in logs or terminals. 
By passing self.message into super().__init__(), you are giving Python's native system the text it needs.
"""