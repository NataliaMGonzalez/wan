instruction_pointer: int = 0

# When going into a function, save the current instruction to be executed
instructions_stack = []

# When entering into a function, this stack will keep the previous values
function_stack = []

# When calling an instance function, know which instance we are inside to
current_class = None
