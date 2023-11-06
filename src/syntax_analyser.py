import re


class SyntaxAnalyzer:
    def __init__(self):
        self.runtime = 0

    def analyze(self, code):
        is_open_bracket = re.search('[', code)
        is_closed_bracket = re.search(']', code)

        print(is_closed_bracket, is_open_bracket)

        if is_open_bracket is None and is_closed_bracket is None:
            return True
        elif (is_open_bracket is None and is_closed_bracket is not None) or (
            is_open_bracket is not None and is_closed_bracket is None):
            raise SyntaxError()
        else: # if there is a loop assume that the program never halts
            return False

        
    def __call__(self, code):
        self.analyze(code)