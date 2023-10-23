from src.analyser import Analyser
import os
import time


class Interpreter:
    def __init__(
        self,
        valid_characters=True
    ):

        self.memory = [0] * 30000
        self.pointer = 0
        self.output = ''
        self.runtime = 0

        self.valid_characters = valid_characters

        self.analyser = Analyser()

    def interpret(self, code, input=None):

        if self.valid_characters:
            code = self.analyser.valid_characters(code)

        start_time = time.time()
        code_ptr = 0
        code_length = len(code)
        input_ptr = 0

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

        end_time = time.time()
        self.runtime = (end_time - start_time) * 1000
        if self.output:
            print(self.output)

    def reset(self):
        self.memory = [0] * 30000
        self.pointer = 0
        self.output = ''
        self.runtime = 0

    def __call__(self, file_path, input):
        self.reset()

        with open(file_path, 'r') as file:
            self.code = file.read()

        self.interpret(self.code, input=input)


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
                interpreter(file_path, input)
                print(
                    f"Interpreted {filename} in {round(interpreter.runtime,3)} ms.")
                print(f"="*50)
