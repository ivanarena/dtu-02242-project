import analyzer

class SyntaxAnalyzer:
    def __init__(self):
        self.runtime = 0

    def analyze(self, code):
        is_open_bracket = code.find('[')
        is_closed_bracket = code.find(']')

        if is_open_bracket is None and is_closed_bracket is None:
            return True
        else: # if there are brackets check if loops are well-formatted, if they are assume that program never halts
            analyzer.not_well_formatted_loop(code)
            return False

        
    def __call__(self, code):
        self.analyze(code)