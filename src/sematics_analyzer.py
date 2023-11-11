import re
import time

class SemanticsAnalyzer:
    def __init__(self):
        self.runtime = 0
        self.ptr = 0

    def _parse_loops(self, code):
        """
        Returns loops and variables abstractions dicts
        
        Inputs:
            - code: Brainfuck program
        
        Outputs:
            - loops: dict: key: memory cell index, value: array of loop objects 
                                (e.g.) {
                                            'start': loop start index,
                                            'end': loop end index,
                                            'code': loop code,
                                            'depth': loop depth,
                                        }
            - variables: dict: key: memory cell index, value: memory cell value 
        """
        stack = []
        ptr_stack = []
        loops = {}
        variables = {}
        depth = -1
        
        curr_var = 0
        for i, ch in enumerate(code):
            # TODO: implement and abstract input command
            if ch == '>':
                self.ptr += 1
                if self.ptr in variables.keys():
                    curr_var = variables[self.ptr]
                else:
                    curr_var = 0
            elif ch == '<':
                self.ptr -= 1
                if self.ptr in variables.keys():
                    curr_var = variables[self.ptr]
                else:
                    curr_var = 0
            elif ch == '+':
                if (self.ptr < 0):
                    raise SystemError('Pointer out of bounds') #TODO add upper bound to memory tape
                curr_var += 1
                variables[self.ptr] = curr_var 
            elif ch == '-':
                if (self.ptr < 0):
                    raise SystemError('Pointer out of bounds')
                curr_var -= 1
                variables[self.ptr] = curr_var 
            elif ch == '[':
                ptr_stack.append(self.ptr)
                stack.append(i)
                depth += 1
            elif ch == ']':
                if not stack:
                    raise SyntaxError(f"Unbalanced brackets at index {i}")
                start = stack.pop()
                if ptr_stack[-1] not in loops.keys():
                    loops[ptr_stack[-1]] = []
                loops[ptr_stack[-1]].append({
                    "start": start,
                    "end": i,
                    "code": code[start+1:i],
                    "depth": depth
                })
                ptr_stack.pop()
                depth -= 1
        if stack:
            raise SyntaxError(f"Unbalanced brackets at index {stack[0]}")
        

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
        loops, vars = self._parse_loops(code)      
        print("CODE", code)
        print("LOOPS", loops)
        print("VARS", vars)
        
        updated_vars = vars
        for key, elem in loops.items(): # iterate through the loops in the program
            initial_ptr = key
            current_ptr = initial_ptr
            #vars values are the ones post first iteration of loops
            if vars[initial_ptr] == 0: # just one iteration to make the entering variable reach zero
                print(f'loop {key} halts')
                continue # move on to outer loop

            for loop in elem:
                # here it holds that vars[initial_ptr] != 0
                print("LOOP", loop['code'])

                if not loop['code']: # empty loop
                    raise SystemError('Not halting: loop is empty')
                 
                if re.search(r'^[^+-]*$', loop['code']) : # no + - inside loop (e.g., [>>>>] wont halt) [not complete because >>>[>+>>] wont match]
                    raise SystemError('Not halting: loop has no writing operations')
                
                if loop['code'].count('+') > 0 and re.search(r'^[^-<>]*$', loop['code']): # (not considering input for now) if a loop has no - or moving operations
                    if (loop['code'].count('+') % 2 == 0 and vars[initial_ptr] % 2 == 0):
                        print('it halts')
                        vars[initial_ptr] = 0
                        continue
                    elif (loop['code'].count('+') % 2 == 0 and vars[initial_ptr] % 2 != 0):
                        raise SystemError('Not halting: odd inital value and even increment') # does this always hold?
                    elif (loop['code'].count('+') % 2 != 0 and vars[initial_ptr] % 2 == 0):
                        raise SystemError('Not halting: even inital value and odd increment') # does this always hold?
                    

                if loop['code'].count('-') > 0 and re.search(r'^[^+<>]*$', loop['code']): # (not considering input for now) if a loop has no + or moving operations
                    if (loop['code'].count('-') % 2 == 0 and vars[initial_ptr] % 2 == 0):
                        print('it halts')
                        vars[initial_ptr] = 0
                        continue
                    elif (loop['code'].count('+') % 2 == 0 and vars[initial_ptr] % 2 != 0):
                        raise SystemError('Not halting: odd inital value and even increment')                 


                for cmd in loop['code']: # to evaluate vars after another loop iteration (the 2nd one) 
                    print('currptr', current_ptr)
                    print('cmd', cmd)
                    if cmd == '+':
                        updated_vars[current_ptr] = (updated_vars[current_ptr] + 1) % 256
                    elif cmd == '-':
                        updated_vars[current_ptr] = (updated_vars[current_ptr] - 1) % 256
                    elif cmd == '>':
                        current_ptr += 1
                    elif cmd == '<':
                        current_ptr -= 1

                print("UPDATED VARS", updated_vars)
                if updated_vars[initial_ptr] == 0:
                    print('it halts')
                # elif updated_vars[initial_ptr] < vars[initial_ptr] and ((vars[initial_ptr] - updated_vars[initial_ptr] % 2 != 0 and updated_vars[initial_ptr] % 2 != 0) or (vars[initial_ptr] - updated_vars[initial_ptr] % 2 == 0 and updated_vars[initial_ptr] % 2 == 0)):
                #     print('halts')
                else:
                    raise SystemError('not halts') # give up and say that it does not halt (?)
                    
            vars[initial_ptr] = 0 # update vars with the initial of this cycle (or with all the changed values?)
                                

        # TODO:
        # 1.    decide queue order
        # 2.    for every loop in order:
        #   2.1     read loop
        #   2.2     update variables dict
        #   2.3     decide if loop terminates 
        #       2.3.1a   if loop terminates continue
        #       2.3.1b   if loop doesn't terminate raise exception 
                            # loop for sure does not terminate if the variable I entered the loop with stays untouched

    def __call__(self, code):
        self.analyze(code)

# s = SemanticsAnalyzer()
# #program = "+++[a=3>>+[b=1<<-][a=2]]"
# program = "+[>++[<-]]" # a=1 b=2
# s(program)