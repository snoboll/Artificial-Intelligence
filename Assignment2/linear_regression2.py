#linear regression
import matplotlib.pyplot as plt
import datasets
import numpy as np
import gradient_descent as gd

def normalize(X, y):
    X_max = [max(x[i] for x in X) for i in range(len(X[0]))]
    X_norm = [[x[i]/X_max[i] for i in range(len(X[0]))] for x in X]

    y_max = max(y)
    y_norm = [yi / y_max for yi in y]

    return X_norm, y_norm, X_max, y_max

def my_descent(X, y, rate, w):



    return
    
if __name__ == '__main__':
    #loading and copying data
    Xe, ye = datasets.load_tsv(
        'https://raw.githubusercontent.com/pnugues/ilppp/master/programs/ch04/salammbo/salammbo_a_en.tsv')
    Xf, yf = datasets.load_tsv(
        'https://raw.githubusercontent.com/pnugues/ilppp/master/programs/ch04/salammbo/salammbo_a_fr.tsv')
    Xeye = [Xe[i] + [ye[i]] for i, x in enumerate(Xe)]#class 0
    Xfyf = [Xf[i] + [yf[i]] for i, x in enumerate(Xf)]#class 1
    X = Xe + Xf
    y = ye + yf

    X_copy = X.copy()
    y_copy = y.copy()

    #normalizing
    X_norm, y_norm, X_max, y_max = normalize(X_copy, y_copy)
    Xy_max = X_max + [y_max]
    rate = 1

    #performing the descent
    w = [0] * (len(X_copy))
    w = gd.batch_descent(X_norm, y_norm, rate, w)

    #adjusting normalized weights to original input
    w = [w[i] * Xy_max[-1] / Xy_max[i] for i in range(len(w))]

    #setting up values in X and y for plotting
    x_fig = [x[1] for x in X_copy]
    y_fig = y_copy

    plt.plot([x[1] for x in Xe], ye, 'ro')
    plt.plot([x[1] for x in Xf], yf, 'bo')
    plt.plot([min(x_fig), max(x_fig)],
         [np.dot([1, min(x_fig)], w),
          np.dot([1, max(x_fig)], w)])
    plt.show()
