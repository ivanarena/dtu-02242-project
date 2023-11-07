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
                curr_var += 1
                variables[self.ptr] = curr_var 
            elif ch == '-':
                curr_var -= 1
                variables[self.ptr] = curr_var 
            elif ch == '[':
                ptr_stack.append(self.ptr)
                stack.append(i)
                depth += 1
            elif ch == ']':
                if not stack:
                    raise ValueError(f"Unbalanced brackets at index {i}")
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
            raise ValueError(f"Unbalanced brackets at index {stack[0]}")
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
        print(loops)
        print(variables)
        # TODO:
        # 1.    decide queue order
        # 2.    for every loop in order:
        #   2.1     read loop
        #   2.2     update variables dict
        #   2.3     decide if loop terminates
        #       2.3.1a   if loop terminates continue
        #       2.3.1b   if loop doesn't terminate raise exception

    def __call__(self, code):
        self.analyze(code)

s = SemanticsAnalyzer()
program = "+++[a=3>>+[b=1<<-][a=2]]"
s(program)