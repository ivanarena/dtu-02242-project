# dtu-02242-project
Repository for the project of the DTU course 02242 - Program Analysis

## Requirements

The project requires Python3.x and the `pytest` module. You can install `pytest` through either on of the following commands:

```bash
python -m pip install -r requirements.txt
```
or 
```bash
python -m pip install -r requirements.txt
```

# Setup

First, update the `PYTHONPATH`:

```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```
or
```bash
set PYTHONPATH=%PYTHONPATH%;%cd%
```

if you use Windows (cmd). Then you can run the tests, from root directory:

```bash
python src/tester.py
```

# Run

To only run the interpreter run this command from the root directory:

```bash
python src/intepreter.py
```

