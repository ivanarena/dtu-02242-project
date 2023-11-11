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
            loops = analyzer.well_formatted_loop(code) # check if loop is well formatted and get loops
            
            print("CODE", code)
            print("LOOPS", loops)

            for loop in loops:
                print(loop[2])
                if not loop[2]: # empty loop
                    raise SystemError('Not halting: loop is empty')
                
                if re.search(r'^[^+-]*$', loop[2]) : # no + - inside loop (e.g., [>>>>] wont halt) [not complete because >>>[>+>>] wont match]
                    raise SystemError('Not halting: loop has no writing operations')
                
                if re.search(r'^[^<>]*$', loop[2]): # no moving operations and same amount of + AND - (if I have [+] eventually I reach 0)
                    if loop[2].count('+') == loop[2].count('-'):
                        raise SystemError('Not halting: no moving operations and same amount of + and -')

            end_time = time.time()
            self.runtime = (end_time - start_time) * 1000

            return True #otherwise assume it halts 
        
    def __call__(self, code):
        self.analyze(code)