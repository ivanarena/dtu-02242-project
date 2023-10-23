class Analyser:
    def valid_characters(self, code):
        commands = ['>', '<', '+', '.', '[', ']', '-', ',', '']
        code = ''.join(char for char in code if char in commands)
        return code
