import re
import time
import analyzer

class SyntaxAnalyzer:
    def __init__(self):
        self.runtime = 0

    def analyze(self, code):
        is_open_bracket = re.search(r'\[', code)
        is_closed_bracket = re.search(r'\]', code)

        start_time = time.time()

        if is_open_bracket is None and is_closed_bracket is None: # no loop, hence it halts
            end_time = time.time()
            self.runtime = (end_time - start_time) * 1000
            return True
        else: # if there is a loop assume that the program never halts
            print(analyzer.well_formatted_loop(code)) # check if loop is well formatted

            end_time = time.time()
            self.runtime = (end_time - start_time) * 1000
            return False
        
    def __call__(self, code):
        self.analyze(code)