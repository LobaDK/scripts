webscrapped_variable = 'ace one           ace one'

var1 = webscrapped_variable.split()
print(" ".join(sorted(set(var1), key=var1.index)))