import matplotlib.pyplot as plt
import datasets, random
import numpy as np
import matplotlib.patches as mpatches

Xe, ye = datasets.load_tsv(
    'https://raw.githubusercontent.com/pnugues/ilppp/master/programs/ch04/salammbo/salammbo_a_en.tsv')
Xf, yf = datasets.load_tsv(
    'https://raw.githubusercontent.com/pnugues/ilppp/master/programs/ch04/salammbo/salammbo_a_fr.tsv')

rate = 1
w = [1, 1, 1]

Xeye = [Xe[i] + [ye[i]] for i, x in enumerate(Xe)]#class 0
Xfyf = [Xf[i] + [yf[i]] for i, x in enumerate(Xf)]#class 1
allpoints = Xeye + Xfyf
score = 0

errcount = -1
for j in range(30):
    allpoints_copy = allpoints.copy()
    randint = random.randint(0,29)
    p = allpoints_copy.pop(randint)
    goldlist = [0]*15 + [1]*15
    p_gold = goldlist.pop(randint)
    #eng = 0, fra = 1
    for _ in range(1000):
        for i, x in enumerate(allpoints_copy):
            pred = 1 if np.dot(x, w) > 0 else 0
            gold = goldlist[i]
            d = gold-pred
            w[0] = w[0] + x[0]*d*rate
            w[1] = w[1] + x[1]*d*rate
            w[2] = w[2] + x[2]*d*rate

            if not d == 0:
                errcount += 1
        if errcount == 0:
            break
        print(w)
    errcount = 0
    pred = 1 if np.dot(p, w) > 0 else 0
    if (p_gold == pred):
        score += 1

print(score)

x = np.linspace(10000, 80000, 1000)
#final weights w: [-5, -2600.0, 39579.0]

y = -(w[0] + w[1]*x)/w[2]
plt.plot(x, y)

plt.plot([x[1] for x in Xe], ye, 'ro')
plt.plot([x[1] for x in Xf], yf, 'bo')
red_patch = mpatches.Patch(color='red', label='En')
blue_patch = mpatches.Patch(color='blue', label='Fr')
plt.legend(handles=[red_patch, blue_patch])
plt.xlabel("Letters in chapter")
plt.ylabel("Number of a:s in chapter")
plt.title("Perceptron")

plt.show()
