#perceptron
import matplotlib.pyplot as plt
import datasets
import vector
import numpy as np

Xe, ye = datasets.load_tsv(
    'https://raw.githubusercontent.com/pnugues/ilppp/master/programs/ch04/salammbo/salammbo_a_en.tsv')
Xf, yf = datasets.load_tsv(
    'https://raw.githubusercontent.com/pnugues/ilppp/master/programs/ch04/salammbo/salammbo_a_fr.tsv')

plt.plot([x[1] for x in Xe], ye, 'ro')
plt.plot([x[1] for x in Xf], yf, 'bo')

rate = 1
w = [1, 1, 1]

Xeye = [Xe[i] + [ye[i]] for i, x in enumerate(Xe)]#class 0
Xfyf = [Xf[i] + [yf[i]] for i, x in enumerate(Xf)]#class 1
allpoints = Xeye + Xfyf
#eng = 0, fra = 1
for _ in range(1000):
    for i, x in enumerate(allpoints):
        gold = 0 if i < 15 else 1
        pred = 1 if np.dot(x, w) > 0 else 0

        d = gold-pred
        w[0] = w[0] + x[0]*d*rate
        w[1] = w[1] + x[1]*d*rate
        w[2] = w[2] + x[2]*d*rate

x = np.linspace(10000, 80000, 1000)
y = -(w[0] + w[1]*x)/w[2]
plt.plot(x, y)
plt.show()
