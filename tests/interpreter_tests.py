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

def test_h_1_sm(interpreter):
    try:
        interpreter.interpret(read(program_dict['h_1']), "", "semantic")
    except SystemError:
        assert False

def test_h_1_sy(interpreter):
    try:
        interpreter.interpret(read(program_dict['h_1']), "", "syntactic")
    except SystemError:
        assert False

def test_h_2_sm(interpreter):
    try:
        interpreter.interpret(read(program_dict['h_2']), "", "semantic")
    except SystemError:
        assert False

def test_h_2_sy(interpreter):
    try:
        interpreter.interpret(read(program_dict['h_2']), "", "syntactic")
    except SystemError:
        assert False

def test_h_3_sm(interpreter):
    try:
        interpreter.interpret(read(program_dict['h_3']), "", "semantic")
    except SystemError:
        assert False

def test_h_3_sy(interpreter):
    try:
        interpreter.interpret(read(program_dict['h_3']), "", "syntactic")
    except SystemError:
        assert False

def test_h_4_sm(interpreter):
    try:
        interpreter.interpret(read(program_dict['h_4']), "", "semantic")
    except SystemError:
        assert False

def test_h_4_sy(interpreter):
    try:
        interpreter.interpret(read(program_dict['h_4']), "", "syntactic")
    except SystemError:
        assert False

def test_h_5_sm(interpreter):
    try:
        interpreter.interpret(read(program_dict['h_5']), "", "semantic")
    except SystemError:
        assert False

def test_h_5_sy(interpreter):
    try:
        interpreter.interpret(read(program_dict['h_5']), "", "syntactic")
    except SystemError:
        assert False

def test_h_6_sm(interpreter):
    try:
        interpreter.interpret(read(program_dict['h_6']), "", "semantic")
    except SystemError:
        assert False

def test_h_6_sy(interpreter):
    try:
        interpreter.interpret(read(program_dict['h_6']), "", "syntactic")
    except SystemError:
        assert False

def test_h_7_sm(interpreter):
    try:
        interpreter.interpret(read(program_dict['h_7']), "", "semantic")
    except SystemError:
        assert False

def test_h_7_sy(interpreter):
    try:
        interpreter.interpret(read(program_dict['h_7']), "", "syntactic")
    except SystemError:
        assert False

def test_h_8_sm(interpreter):
    try:
        interpreter.interpret(read(program_dict['h_8']), "", "semantic")
    except SystemError:
        assert False

def test_h_8_sy(interpreter):
    try:
        interpreter.interpret(read(program_dict['h_8']), "", "syntactic")
    except SystemError:
        assert False

def test_h_9_sm(interpreter):
    try:
        interpreter.interpret(read(program_dict['h_9']), "", "semantic")
    except SystemError:
        assert False

def test_h_9_sy(interpreter):
    try:
        interpreter.interpret(read(program_dict['h_9']), "", "syntactic")
    except SystemError:
        assert False


def test_hello_sy(interpreter):
    expected_output = "Hello World!"
    interpreter.interpret(read(program_dict['h_11_hello']),"", "syntactic")
    assert interpreter.output == expected_output

def test_hello_sm(interpreter):
    expected_output = "Hello World!"
    interpreter.interpret(read(program_dict['h_11_hello']),"", "semantic")
    assert interpreter.output == expected_output

def test_addition_sy(interpreter):
    try:
        interpreter.interpret(read(program_dict['h_12_addition']), "", "syntactic")
    except SystemError:
        assert False

def test_addition_sm(interpreter):
    try:
        interpreter.interpret(read(program_dict['h_12_addition']), "", "semantic")
    except SystemError:
        assert False


def test_nh1_sy(interpreter):
    with pytest.raises(SystemError, match="The program never halts."):
        interpreter.interpret(read(program_dict['nh_1']), "", "syntactic")

def test_nh1_sm(interpreter):
    with pytest.raises(SystemError, match="The program never halts."):
        interpreter.interpret(read(program_dict['nh_1']), "", "semantic")

def test_nh2_sy(interpreter):
    with pytest.raises(SystemError, match="The program never halts."):
        interpreter.interpret(read(program_dict['nh_2']), "", "syntactic")

def test_nh2_sm(interpreter):
    with pytest.raises(SystemError, match="The program never halts."):
        interpreter.interpret(read(program_dict['nh_2']), "", "semantic")

def test_nh3_sy(interpreter):
    with pytest.raises(SystemError, match="The program never halts."):
        interpreter.interpret(read(program_dict['nh_3']), "", "syntactic")

def test_nh3_sm(interpreter):
    with pytest.raises(SystemError, match="The program never halts."):
        interpreter.interpret(read(program_dict['nh_3']), "", "semantic")

def test_nh4_sy(interpreter):
    with pytest.raises(SystemError, match="The program never halts."):
        interpreter.interpret(read(program_dict['nh_4']), "", "syntactic")

def test_nh4_sm(interpreter):
    with pytest.raises(SystemError, match="The program never halts."):
        interpreter.interpret(read(program_dict['nh_4']), "", "semantic")

def test_nh5_sy(interpreter):
    with pytest.raises(SystemError, match="The program never halts."):
        interpreter.interpret(read(program_dict['nh_5']), "", "syntactic")

def test_nh5_sm(interpreter):
    with pytest.raises(SystemError, match="The program never halts."):
        interpreter.interpret(read(program_dict['nh_5']), "", "semantic")

def test_nh6_sy(interpreter):
    with pytest.raises(SystemError, match="The program never halts."):
        interpreter.interpret(read(program_dict['nh_6']), "", "syntactic")

def test_nh6_sm(interpreter):
    with pytest.raises(SystemError, match="The program never halts."):
        interpreter.interpret(read(program_dict['nh_6']), "", "semantic")

def test_nh7_sy(interpreter):
    with pytest.raises(SystemError, match="The program never halts."):
        interpreter.interpret(read(program_dict['nh_7']), "", "syntactic")

def test_nh7_sm(interpreter):
    with pytest.raises(SystemError, match="The program never halts."):
        interpreter.interpret(read(program_dict['nh_7']), "", "semantic")

def test_nh8_sy(interpreter):
    with pytest.raises(SystemError, match="The program never halts."):
        interpreter.interpret(read(program_dict['nh_8']), "", "syntactic")

def test_nh8_sm(interpreter):
    with pytest.raises(SystemError, match="The program never halts."):
        interpreter.interpret(read(program_dict['nh_8']), "", "semantic")

def test_nh9_sy(interpreter):
    with pytest.raises(SystemError, match="The program never halts."):
        interpreter.interpret(read(program_dict['nh_9']), "", "syntactic")

def test_nh9_sm(interpreter):
    with pytest.raises(SystemError, match="The program never halts."):
        interpreter.interpret(read(program_dict['nh_9']), "", "semantic")

def test_nh10_sy(interpreter):
    with pytest.raises(SystemError, match="The program never halts."):
        interpreter.interpret(read(program_dict['nh_10']), "", "syntactic")

def test_nh10_sm(interpreter):
    with pytest.raises(SystemError, match="The program never halts."):
        interpreter.interpret(read(program_dict['nh_10']), "", "semantic")

        

