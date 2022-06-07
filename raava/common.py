"""The variables to be used and shared by the virtual machine.

These variables only have one instance of each, and their content may be updated
by any of the files within the virtual machine.
"""

# Current instruction that is executed by the virtual machine
instruction_pointer: int = 0

# When calling an instance function, know which instance we are inside to
current_class = None
