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
            # print(ch, ptr)
            if ch == '>':
                if ptr > UPPER_BOUND:  # upper bound err
                    raise SystemError('Pointer out of bounds')
                ptr += 1
                if ptr in variables.keys():
                    curr_var = variables[ptr]
                else:
                    curr_var = 0
            elif ch == '<':
                if ptr < LOWER_BOUND:  # lower bound err
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
                    "nested_loop": None
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
                    stack[-1]["nested_loop"] = loop
                else:
                    loops.append(loop)
            i += 1

        if stack:
            raise SyntaxError('Loop start found without a corresponding loop end')

        return loops, variables

    def __sanitize(self, code):
        pattern = re.compile(r'\[.*?\]')  # Match anything inside square brackets
        sanitized_code = re.sub(pattern, '', code)  # Remove text inside square brackets
        pattern = re.compile(r'\]')  # Match anything inside square brackets
        sanitized_code = re.sub(pattern, '', sanitized_code)  # Remove text inside square brackets
        return sanitized_code

    def _solve_loop(self, cell, value, code):

        code = self.__sanitize(code) # only keep relevant values

        # remember to update variables

        return cell

    def _get_nth_loop(self, loop, nested_count):
        while nested_count > 0:
            loop = loop['nested_loop']
            nested_count -= 1
        return loop
    

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
        # print("CODE")
        # pprint.pprint(code)
        # print("LOOPS")
        # pprint.pprint(loops)
        # print("variables")
        # pprint.pprint(variables)
        
        # TODO:
        # 1.    decide queue order
        # 2.    for every loop in order:
        #   2.1     read loop
        #   2.2     update variables dict
        #   2.3     decide if loop terminates 
        #       2.3.1a   if loop terminates continue
        #       2.3.1b   if loop doesn't terminate raise exception 
                            # loop for sure does not terminate if the variable I entered the loop with stays untouched
        for loop in loops:
            curr_loop = loop
            nested_count = 0
            
            curr_loop, nested_count = self._get_innermost_loop(curr_loop, nested_count)
            
            while nested_count >= 0: # solve in order of depth
                updated_variables = self._solve_loop(curr_loop["cell"], curr_loop["value"], curr_loop["code"])
                
                nested_count -= 1
                curr_loop = self._get_nth_loop(loop, nested_count) # get loop 1 level above
                
            
        
        
        
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

    def _get_innermost_loop(self, curr_loop, nested_count):
        while curr_loop['has_nested_loop'] is True: # go to innermost loop 
            nested_count += 1
            curr_loop = curr_loop['nested_loop']
        return curr_loop, nested_count


    def __call__(self, code):
        self.analyze(code)

s = SemanticsAnalyzer()
program = "+++[++[>>>[>>]]][>>++[+++]]"
# program = "+++[++[>>>[>>]]][>>++[]]"
program = "+++[1[1.1[1.1.1]]]asda[2[2.1]]"
# program = "+[>++[<-]]" # a=1 b=2
s(program)