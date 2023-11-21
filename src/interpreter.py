from src.syntax_analyzer import SyntaxAnalyzer
from src.semantics_analyzer import SemanticsAnalyzer
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
        self.analysis_runtime = 0

        self.syntax_analyzer = SyntaxAnalyzer()
        self.semantics_analyzer = SemanticsAnalyzer()

    def interpret(self, code, input=None, analysis='syntactic', omit_output=True):
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
        else:
            analyzer = self.semantics_analyzer

        try:
            start_time = time.time()
            analyzer(code)
            end_time = time.time()
            self.analysis_runtime = (end_time - start_time) * 1000
        except SyntaxError:
            raise SyntaxError('The program is not well-formatted.')
        except SystemError:
            end_time = time.time()
            self.analysis_runtime = (end_time - start_time) * 1000
            raise SystemError('The program never halts.')

        while code_ptr < code_length:
            command = code[code_ptr]

            if command == '>':
                self.pointer += 1
            elif command == '<':
                self.pointer -= 1
            elif command == '+':
                if self.memory[self.pointer] < 255: 
                    self.memory[self.pointer] = self.memory[self.pointer] + 1
            elif command == '-':
                if self.memory[self.pointer] > 0: 
                    self.memory[self.pointer] = self.memory[self.pointer] - 1
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
                raise SystemError() 

        end_time = time.time()
        self.runtime = (end_time - start_time) * 1000
        if self.output and not omit_output:
            print(self.output)

    def reset(self):
        self.memory = [0] * 30000
        self.pointer = 0
        self.output = ''
        self.runtime = 0
        self.steps = 0
        self.analysis_runtime = 0

    def __call__(self, file_path, input, analysis):
        self.reset()

        with open(file_path, 'r') as file:
            content = file.read()

        self.code = ''.join(c for c in content if c in "+-<>[],.")

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
                input = 'hello'
                analysis = 'syntactic'
                try:
                    interpreter(file_path, input=input, analysis=analysis)
                    print(
                        f"Interpreted {filename} in {interpreter.steps} steps.")
                except SyntaxError:
                    print('SyntaxError: The program is not well-formatted.')   
                except SystemError:
                    print('SystemError: The program never halts.')     
                
                print(f"="*50)
