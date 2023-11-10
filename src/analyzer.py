def well_formatted_loop(code):
    stack = []
    loops = []
    
    filtered_code = ''.join(c for c in code if c in "+-<>[],.") # exclude comments

    for i, cmd in enumerate(filtered_code):
       
        if cmd == '[':
            stack.append(i+1)
        elif cmd == ']':
            if not stack:
                raise SyntaxError(f"Unbalanced brackets at index {i + 1}")
            start = stack.pop()
            
            loops.append((start + 1, i + 1, filtered_code[start+1:i]))

    if stack:
        raise SyntaxError(f"Unbalanced brackets at index {stack[0]}")
    
    return loops
