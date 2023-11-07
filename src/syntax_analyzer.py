import re
import time

class SyntaxAnalyzer:
    def __init__(self):
        self.runtime = 0

    def analyze(self, code):
        is_open_bracket = re.search('[', code)
        is_closed_bracket = re.search(']', code)

        start_time = time.time()

        if is_open_bracket is None and is_closed_bracket is None:
            end_time = time.time()
            self.runtime = (end_time - start_time) * 1000
            return True
        elif (is_open_bracket is None and is_closed_bracket is not None) or ( # fix this to do pattern matching 
            is_open_bracket is not None and is_closed_bracket is None):
            end_time = time.time()
            self.runtime = (end_time - start_time) * 1000
            raise SyntaxError()
        else: # if there is a loop assume that the program never halts
            end_time = time.time()
            self.runtime = (end_time - start_time) * 1000
            return False
        
    def __call__(self, code):
        self.analyze(code)