#linear regression
import matplotlib.pyplot as plt
import datasets, random
import vector
import numpy as np
import gradient_descent as gd

if __name__ == '__main__':
    Xe, ye = datasets.load_tsv(
        'https://raw.githubusercontent.com/pnugues/ilppp/master/programs/ch04/salammbo/salammbo_a_en.tsv')
    Xf, yf = datasets.load_tsv(
        'https://raw.githubusercontent.com/pnugues/ilppp/master/programs/ch04/salammbo/salammbo_a_fr.tsv')
    Xeye = [Xe[i] + [ye[i]] for i, x in enumerate(Xe)]#class 0
    Xfyf = [Xf[i] + [yf[i]] for i, x in enumerate(Xf)]#class 1

    X = Xe + Xf
    y = ye + yf

    plt.plot([x[1] for x in Xe], ye, 'ro')
    plt.plot([x[1] for x in Xf], yf, 'bo')

    for i in range(30):
        X_copy = X.copy()
        y_copy = y.copy()
        goldlist = [0]*15 + [1]*15

        randint = random.randint(0,29)
        px = X_copy.pop(randint)
        py = y_copy.pop(randint)
        p_gold = goldlist.pop(randint)

        X_copy, maxima_X = gd.normalize(X_copy)
        maxima_y = max(y_copy)
        y_copy = [yi / maxima_y for yi in y_copy]
        maxima = maxima_X + [maxima_y]
        alpha = 1

        w = [0.0] * (len(X_copy))
        w = gd.batch_descent(X_copy, y_copy, alpha, w)

        #restoring
        w = [w[i] * maxima[-1] / maxima[i] for i in range(len(w))]
        x_fig = [X_copy[i][1] * maxima_X[1] for i in range(len(X_copy))]
        y_fig = [yi * maxima_y for yi in y_copy]
        plt.plot([min(x_fig), max(x_fig)],
             [vector.dot([1, min(x_fig)], w),
              vector.dot([1, max(x_fig)], w)])
    plt.show()
