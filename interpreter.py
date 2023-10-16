class Interpreter:
    def __init__(self):
        self.memory = [0] * 30000
        self.pointer = 0
        self.output = ''

    def interpret(self, code):
        code_ptr = 0
        code_length = len(code)

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
                user_input = input('Enter a character: ')
                if len(user_input) > 0:
                    self.memory[self.pointer] = ord(user_input[0])
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

    def get_output(self):
        return self.output


if __name__ == '__main__':
    with open('programs/hello.bf', 'r') as file:
        hello_bf_code = file.read()

    interpreter = Interpreter()
    interpreter.interpret(hello_bf_code)

    print(interpreter.get_output())
