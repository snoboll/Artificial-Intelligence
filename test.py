import operator
a = {1:5, 2:6, 3:9}
b = [(111, 22), (33333, 44), (55, 666)]

c, d= max(b, key=operator.itemgetter(1))
print(c)
print (d)
