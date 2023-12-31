import re
import time
import pprint
UPPER_BOUND = 30000
LOWER_BOUND = 0


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

        return loops

    def __sanitize(self, code):
        pattern = re.compile(r'\[.*?\]')  # Match anything inside square brackets
        sanitized_code = re.sub(pattern, '', code)  # Remove text inside square brackets
        pattern = re.compile(r'\]')  # Match anything inside square brackets
        sanitized_code = re.sub(pattern, '', sanitized_code)  # Remove text inside square brackets
        return sanitized_code

    def _get_nth_loop(self, loop, nested_count):
        while nested_count > 0:
            loop = loop['nested_loop']
            nested_count -= 1
        return loop

    def _solve_loop(self, cell, value, code):

        code = self.__sanitize(code) # only keep relevant values

        # first analysis
        if '-' not in code:
            raise SystemError("The loop never halts.")

        ptr = cell
        
        to_update = {} # (key, value) pair is (variable, increment/decrement count)
        to_update[cell] = 0

        # analyse loop
        for ch in code:
            if ch == '<':
                ptr -= 1
            elif ch == '>':
                ptr += 1
            elif ch == '+':
                if ptr in to_update.keys():
                    to_update[ptr] += 1
                else:
                    to_update[ptr] = 1
            elif ch == '-':
                if ptr in to_update.keys():
                    to_update[ptr] -= 1
                else:
                    to_update[ptr] = -1
        
        # not decrementing enough
        if to_update[cell] > -1:
            raise SystemError("The loop never halts.")

        # ! assume that loops run at least once so decrement/increment once 
        return to_update
    
    def _get_init_variables(self, code):
        variables = {0: 0}

        ptr = 0
        for ch in code:
            if ch == '[':
                break
            if ch == '<':
                ptr -= 1
            elif ch == '>':
                ptr += 1
            elif ch == '+':
                variables[ptr] += 1
            elif ch == '-':
                variables[ptr] -= 1
            if ptr not in variables.keys():
                variables[ptr] = 0

        return variables

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
        loops = self._parse_loops(code)      
        variables = self._get_init_variables(code)

        for loop in loops:
            curr_loop = loop
            nested_count = 0
            
            curr_loop, nested_count = self._get_innermost_loop(curr_loop, nested_count)
            
            # ! nested_count == 0 solves the outermost loop
            while nested_count >= 0: # solve in order of depth

                if curr_loop["value"] > 0:

                    to_update = self._solve_loop(curr_loop["cell"], curr_loop["value"], curr_loop["code"])
                    

                    # update variables
                    for var in to_update.keys():
                        # if loop halts then entering cell value is 0 by definition
                        if var == curr_loop["cell"]:
                            variables[var] = 0
                        else:
                            if var in variables.keys():
                                variables[var] += to_update[var]

                            # first encounter of the variable
                            else:
                                if to_update[var] > 0:
                                    variables[var] = to_update[var]
                                else:
                                    variables[var] = 0
                            
                            # keep values beneath interpreter boundaries 
                            if not (var in variables.keys()) or variables[var] < 0:
                                variables[var] = 0                                 
                            elif variables[var] > 255:
                                variables[var] = 255                                       

                    
                    

                nested_count -= 1
                curr_loop = self._get_nth_loop(loop, nested_count) # get loop 1 level above
                curr_loop["value"] = variables[curr_loop['cell']] # update entering value from updated variables

        return True

    def _get_innermost_loop(self, curr_loop, nested_count):
        while curr_loop['has_nested_loop'] is True: # go to innermost loop 
            nested_count += 1
            curr_loop = curr_loop['nested_loop']
        return curr_loop, nested_count


    def __call__(self, code):
        self.analyze(code)
