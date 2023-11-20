from src.interpreter import Interpreter
import os
import pytest

PROGRAMS_DIRECTORY = 'programs/'
filenames = os.listdir(PROGRAMS_DIRECTORY)
program_dict = {}

# Iterate through the list of files and run the tests for each program
for filename in filenames:
    if filename.endswith('.bf'):
        file_path = os.path.join(PROGRAMS_DIRECTORY, filename)
        # Get the program name without the file extension
        program_name = os.path.splitext(filename)[0]
        # Store the program name and file path in the dictionary
        program_dict[program_name] = file_path


def read(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    return code


@pytest.fixture
def interpreter():
    return Interpreter()


@pytest.fixture
def interpreter_v1():
    return Interpreter(valid_characters=True)

def test_hello(interpreter):
    expected_output = "Hello World!"
    interpreter.interpret(read(program_dict['h_11_hello']),"", "syntactic")
    assert interpreter.output == expected_output

def test_nh1(interpreter):
    with pytest.raises(SystemError, match="The program never halts."):
        interpreter.interpret(read(program_dict['nh_1']),"", "syntactic")


        

