def not_well_formatted_loop(program):
    stack = []
    
    for cmd in program:
        if cmd == '[':
            stack.append('[')
        elif cmd == ']':
            if not stack:
                raise SyntaxError()
            stack.pop()


    if len(stack) != 0:
        raise SyntaxError()
