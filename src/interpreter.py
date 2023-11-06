from syntax_analyser import SyntaxAnalyzer
from sematics_analyzer import SemanticsAnalyzer
import os
import time


class Interpreter:
    def __init__(
        self,
    ):
        self.memory = [0] * 30000
        self.pointer = 0
        self.output = ''
        self.runtime = 0
        self.steps = 0

        self.syntax_analyzer = SyntaxAnalyzer()
        self.semantics_analyzer = SemanticsAnalyzer()

    def interpret(self, code, input=None, analysis='syntactic'):
        """
        Interprets a Brainfuck program

        Inputs:
            - code: Brainfuck code
            - input: if not None, the input string for the program  
            - analysis: ['syntactic' | 'semantic'] 
        """

        start_time = time.time()
        code_ptr = 0
        code_length = len(code)
        input_ptr = 0

        if analysis == 'syntactic':
            analyzer = self.syntax_analyzer
            try:
                halts = analyzer(code)
            except:
                raise SystemError('The program never halts.')
        else:
            analyzer = self.semantics_analyzer

        while code_ptr < code_length:
            command = code[code_ptr]

            if command == '>':
                self.pointer += 1
            elif command == '<':
                self.pointer -= 1
            elif command == '+':
                self.memory[self.pointer] = (
                    self.memory[self.pointer] + 1) % 256
            elif command == '-':
                self.memory[self.pointer] = (
                    self.memory[self.pointer] - 1) % 256
            elif command == '.':
                self.output += chr(self.memory[self.pointer])
            elif command == ',':
                if input and input_ptr < len(input):
                    self.memory[self.pointer] = ord(input[input_ptr])
                input_ptr += 1
            elif command == '[':
                if self.memory[self.pointer] == 0:
                    loop_depth = 1
                    while loop_depth > 0:
                        code_ptr += 1
                        self.steps += 1
                        if code[code_ptr] == '[':
                            loop_depth += 1
                        elif code[code_ptr] == ']':
                            loop_depth -= 1
            elif command == ']':
                if self.memory[self.pointer] != 0:
                    loop_depth = 1
                    while loop_depth > 0:
                        code_ptr -= 1
                        if code[code_ptr] == ']':
                            loop_depth += 1
                        elif code[code_ptr] == '[':
                            loop_depth -= 1
            code_ptr += 1
            self.steps += 1
            if (self.steps > 10000):
                raise RuntimeError() 

        end_time = time.time()
        self.runtime = (end_time - start_time) * 1000
        if self.output:
            print(self.output)

    def reset(self):
        self.memory = [0] * 30000
        self.pointer = 0
        self.output = ''
        self.runtime = 0
        self.steps = 0

    def __call__(self, file_path, input, analysis):
        self.reset()

        with open(file_path, 'r') as file:
            self.code = file.read()

        self.interpret(self.code, input=input, analysis=analysis)


# temporary to run each files
if __name__ == '__main__':
    PROGRAMS_DIRECTORY = 'programs/'

    filenames = os.listdir(PROGRAMS_DIRECTORY)

    interpreter = Interpreter()
    for filename in filenames:
        if filename.endswith('.bf'):
            file_path = os.path.join(PROGRAMS_DIRECTORY, filename)
            with open(file_path, 'r') as file:
                print(f"Interpreting {filename}...")
                input = '2331'
                analysis = 'syntactic'
                try:
                    interpreter(file_path, input=input, analysis=analysis)
                    print(
                        f"Interpreted {filename} in {interpreter.steps} steps.")
                except:
                    print('SystemError: The program never halts.')    
                print(f"="*50)
