import copy
a = [1,2,3]
b = a
b[2] = 7
c = copy.copy(a)
c[1] = 5

print(a, b, c)

q = "a s d d fa df df fad "
print(",".join(q))
