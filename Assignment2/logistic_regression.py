#logistic regression
import matplotlib.pyplot as plt
import datasets, random
import vector
import numpy as np
import gradient_descent as gd

def sigmoid(z):
    return 1.0 / (1 + np.exp(-z))

def predict(xy, w):
    #[1, 38674, 7364] dot []
    print(xy)
    print(w)
    z = np.dot(xy, w)
    return sigmoid(z)

def home_descent(X, y, alpha, w, px, py, pgold):
    alpha /= len(X)
    for epoch in range(1, 1000):
        pred = 1 if predict((px+[py]), w) >= 0.5 else 0
        if pred == pgold:
            break
        loss = vector.sub(y, vector.mul_mat_vec(X, w))
        gradient = vector.mul_mat_vec(vector.transpose(X), loss)
        w_old = w
        w = vector.add(w, vector.mul(alpha, gradient))
        if vector.norm(vector.sub(w, w_old)) / vector.norm(w) < 1.0e-5:
            break
    return w

Xe, ye = datasets.load_tsv(
    'https://raw.githubusercontent.com/pnugues/ilppp/master/programs/ch04/salammbo/salammbo_a_en.tsv')
Xf, yf = datasets.load_tsv(
    'https://raw.githubusercontent.com/pnugues/ilppp/master/programs/ch04/salammbo/salammbo_a_fr.tsv')

plt.plot([x[1] for x in Xe], ye, 'ro')
plt.plot([x[1] for x in Xf], yf, 'bo')

rate = 1

Xeye = [Xe[i] + [ye[i]] for i, x in enumerate(Xe)]#class 0
Xfyf = [Xf[i] + [yf[i]] for i, x in enumerate(Xf)]#class 1
X = Xe+Xf
y = ye+yf
score = 0

for j in range(30):
    X_copy = X.copy()
    y_copy = y.copy()
    w = [0.0]*3

    goldlist = [0]*15 + [1]*15

    randint = random.randint(0,29)
    px = X_copy.pop(randint)
    py = y_copy.pop(randint)
    pgold = goldlist.pop(randint)

    X_copy, maxima_X = gd.normalize(X_copy)
    maxima_y = max(y_copy)
    y_copy = [yi / maxima_y for yi in y_copy]
    maxima = maxima_X + [maxima_y]

    w = home_descent(X_copy, y_copy, rate, w, px, py, pgold)

    w = [w[i] * maxima[-1] / maxima[i] for i in range(len(w))]
    x_fig = [X_copy[i][1] * maxima_X[1] for i in range(len(X_copy))]
    y_fig = [yi * maxima_y for yi in y_copy]
    plt.plot([min(x_fig), max(x_fig)],
         [vector.dot([1, min(x_fig)], w),
          vector.dot([1, max(x_fig)], w)])
print(score)

plt.show()
