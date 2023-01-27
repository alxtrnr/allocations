from mip import Model, INTEGER




# Create a new mixed-integer programming model
m = Model()

# Add input fixed variables

generals = m.add_var(var_type=INTEGER, name='generals')
one2one = m.add_var(var_type=INTEGER, name='1:1')
two2one = m.add_var(var_type=INTEGER, name='2:1')
sec = m.add_var(var_type=INTEGER, name='SEC')
lts = m.add_var(var_type=INTEGER, name='LTS')

m += generals == 12

# Solve the model
m.optimize()

# Print the solution
print(f"Generals = {generals.x}")
