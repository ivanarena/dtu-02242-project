def well_formatted_loop(code):
    stack = []
    loops = []
    

    for i, cmd in enumerate(code):
       
        if cmd == '[':
            stack.append(i+1)
        elif cmd == ']':
            if not stack:
                raise SyntaxError(f"Unbalanced brackets at index {i + 1}")
            start = stack.pop()
            
            loops.append((start, i + 1, code[start:i]))

    if stack:
        raise SyntaxError(f"Unbalanced brackets at index {stack[0]}")
    
    return loops
