instruction_pointer: int = 0

# When going into a function, save the current instruction to be executed
return_to_instruction: int = None

# When entering into a function, this stack will keep the previous values
function_stack = []
