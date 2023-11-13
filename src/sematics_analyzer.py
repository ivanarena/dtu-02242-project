import re
import time
import pprint
UPPER_BOUND = 30000
LOWER_BOUND = 0

class SemanticsAnalyzer:
    def __init__(self):
        self.runtime = 0
        self.ptr = 0

class SemanticsAnalyzer:
    def __init__(self):
        self.runtime = 0

    def _find_loop_end(self, code, start):
        counter = 1
        for i in range(start + 1, len(code)):
            if code[i] == '[':
                counter += 1
            elif code[i] == ']':
                counter -= 1
            if counter == 0:
                return i
        raise SyntaxError(f"No matching closing bracket for the opening bracket at index {start}")

    def _parse_loops(self, code, start=0, end=None, ptr=0, curr_var=0, variables={}):
        stack = []
        loops = []

        if end is None:
            end = len(code)

        i = start
        while i < end:
            ch = code[i]
            print(ch, ptr)
            if ch == '>':
                if ptr == UPPER_BOUND:  # upper bound err
                    raise SystemError('Pointer out of bounds')
                ptr += 1
                if ptr in variables.keys():
                    curr_var = variables[ptr]
                else:
                    curr_var = 0
            elif ch == '<':
                if ptr == LOWER_BOUND:  # lower bound err
                    raise SystemError('Pointer out of bounds')
                ptr -= 1
                if ptr in variables.keys():
                    curr_var = variables[ptr]
                else:
                    curr_var = 0
            elif ch == '+':
                curr_var += 1
                variables[ptr] = curr_var
            elif ch == '-':
                curr_var -= 1
                variables[ptr] = curr_var
            elif ch == '[':
                loop = {
                    "cell": ptr,
                    "value": curr_var,
                    "start": i,
                    "code": "",
                    "has_nested_loop": False,
                    "nested_loop": []
                }
                if stack:
                    stack[-1]["has_nested_loop"] = True
                stack.append(loop)
            elif ch == ']':
                if not stack:
                    raise SyntaxError('Loop end found without a corresponding loop start')
                loop = stack.pop()
                loop["end"] = i
                loop["code"] = code[loop["start"] + 1:i]
                if stack:
                    stack[-1]["nested_loop"].append(loop)
                else:
                    loops.append(loop)
            i += 1

        if stack:
            raise SyntaxError('Loop start found without a corresponding loop end')

        return loops, variables






    def analyze(self, code):
        """
        - keep a ptr to curr curr_var
        - create dict of ptr loc
        - every ptr loc has array of loop obj


        loop obj = {
                var: 3
                loop: [>>>++..]
                level: 0
            }
        """
        loops, variables = self._parse_loops(code)      
        print("CODE")
        pprint.pprint(code)
        print("LOOPS")
        pprint.pprint(loops)
        print("variables")
        pprint.pprint(variables)
        
        # TODO:
        # 1.    decide queue order
        # 2.    for every loop in order:
        #   2.1     read loop
        #   2.2     update variables dict
        #   2.3     decide if loop terminates 
        #       2.3.1a   if loop terminates continue
        #       2.3.1b   if loop doesn't terminate raise exception 
                            # loop for sure does not terminate if the variable I entered the loop with stays untouched
        """
        updated_variables = variables
        for key, elem in loops.items(): # iterate through the loops in the program
            initial_ptr = key
            current_ptr = initial_ptr

            #variables values are the ones post first iteration of loops
            if variables[initial_ptr] == 0: # just one iteration to make the entering variable reach zero
                print(f'loop {key} halts')
                continue # move on to outer loop

            for loop in elem:
                # here it holds that variables[initial_ptr] != 0
                print("LOOP", loop['code'])

                if not loop['code']: # empty loop
                    raise SystemError('Not halting: loop is empty')
                 
                if re.search(r'^[^+-]*$', loop['code']) : # no + - inside loop (e.g., [>>>>] wont halt) [not complete because >>>[>+>>] wont match]
                    raise SystemError('Not halting: loop has no writing operations')
                
                if loop['code'].count('+') > 0 and re.search(r'^[^-<>]*$', loop['code']): # (not considering input for now) if a loop has no - or moving operations
                    if (loop['code'].count('+') % 2 == 0 and variables[initial_ptr] % 2 == 0):
                        print('it halts')
                        variables[initial_ptr] = 0
                        continue
                    elif (loop['code'].count('+') % 2 == 0 and variables[initial_ptr] % 2 != 0):
                        raise SystemError('Not halting: odd inital value and even increment') # does this always hold?
                    elif (loop['code'].count('+') % 2 != 0 and variables[initial_ptr] % 2 == 0):
                        raise SystemError('Not halting: even inital value and odd increment') # does this always hold?
                    

                if loop['code'].count('-') > 0 and re.search(r'^[^+<>]*$', loop['code']): # (not considering input for now) if a loop has no + or moving operations
                    if (loop['code'].count('-') % 2 == 0 and variables[initial_ptr] % 2 == 0):
                        print('it halts')
                        variables[initial_ptr] = 0
                        continue
                    elif (loop['code'].count('+') % 2 == 0 and variables[initial_ptr] % 2 != 0):
                        raise SystemError('Not halting: odd inital value and even increment')                 


                for cmd in loop['code']: # to evaluate variables after another loop iteration (the 2nd one) 
                    print('currptr', current_ptr)
                    print('cmd', cmd)
                    if cmd == '+':
                        updated_variables[current_ptr] = (updated_variables[current_ptr] + 1) % 256
                    elif cmd == '-':
                        updated_variables[current_ptr] = (updated_variables[current_ptr] - 1) % 256
                    elif cmd == '>':
                        current_ptr += 1
                    elif cmd == '<':
                        current_ptr -= 1

                print("UPDATED variables", updated_variables)
                if updated_variables[initial_ptr] == 0:
                    print('it halts')
                # elif updated_variables[initial_ptr] < variables[initial_ptr] and ((variables[initial_ptr] - updated_variables[initial_ptr] % 2 != 0 and updated_variables[initial_ptr] % 2 != 0) or (variables[initial_ptr] - updated_variables[initial_ptr] % 2 == 0 and updated_variables[initial_ptr] % 2 == 0)):
                #     print('halts')
                else:
                    raise SystemError('not halts') # give up and say that it does not halt (?)
                    
            variables[initial_ptr] = 0 # update variables with the initial of this cycle (or with all the changed values?)
                                
            """


    def __call__(self, code):
        self.analyze(code)

s = SemanticsAnalyzer()
program = "+++[++[>>>[>>]]][>>++[+++]]"
program = "+++[++[>>>[>>]]][>>++[]]"
# program = "+[>++[<-]]" # a=1 b=2
s(program)