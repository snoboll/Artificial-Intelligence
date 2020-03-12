import datasets, random
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

def easynorm(x):
    x_max = max(x)
    norm = [xi / x_max for xi in x]
    return x_max, norm

def stoch_desc(x, y, rate, w):
    shuf = list(range(len(x)))
    for epoch in range(1000):
        random.shuffle(shuf)
        for i in shuf:
            w[0] = w[0] - rate*2*(w[0] + w[1]*x[i] - y[i])
            w[1] = w[1] - rate*2*x[i]*(w[0] + w[1]*x[i] - y[i])
    return w

def batch_desc(x, y, rate, w):
    for epoch in range(1000):
        w0dtot = 0
        w1dtot = 0
        for i in range(len(x)):
            w0d = rate*2*(w[0] + w[1]*x[i] - y[i])
            w1d = rate*2*x[i]*(w[0] + w[1]*x[i] - y[i])
            w0dtot += w0d
            w1dtot += w1d

        #updating w by using average wd
        w[0] = w[0] - w0dtot/len(x)
        w[1] = w[1] - w1dtot/len(x)
    return  w

if __name__ == '__main__':
    #loading and copying data
    Xe, ye = datasets.load_tsv(
        'https://raw.githubusercontent.com/pnugues/ilppp/master/programs/ch04/salammbo/salammbo_a_en.tsv')
    Xf, yf = datasets.load_tsv(
        'https://raw.githubusercontent.com/pnugues/ilppp/master/programs/ch04/salammbo/salammbo_a_fr.tsv')
    Xeye = [Xe[i] + [ye[i]] for i, x in enumerate(Xe)]#class 0
    Xfyf = [Xf[i] + [yf[i]] for i, x in enumerate(Xf)]#class 1
    x = [e[1] for e in Xe] + [e[1] for e in Xf]
    y = ye + yf

    x_copy = x.copy()
    y_copy = y.copy()

    #normalizing
    x_max, x_norm = easynorm(x_copy)
    y_max, y_norm = easynorm(y_copy)

    #performing the descent, choosing either batch or stoch
    rate = 0.1
    w = [0, 0]
    #w = batch_desc(x_norm, y_norm, rate, w)
    w = stoch_desc(x_norm, y_norm, rate, w)

    #adjusting normalized weights to original input
    w[1] = w[1] * y_max/x_max
    print(w)

    #plotting points in original input
    plt.plot([x[1] for x in Xe], ye, 'ro')
    plt.plot([x[1] for x in Xf], yf, 'bo')
    red_patch = mpatches.Patch(color='red', label='En')
    blue_patch = mpatches.Patch(color='blue', label='Fr')
    plt.legend(handles=[red_patch, blue_patch])

    #plotting the linear regression line
    x_fig = np.linspace(10000, 80000, 1000)
    y_fig = w[0] + w[1]*x_fig
    plt.plot(x_fig, y_fig)
    plt.xlabel("Letters in chapter")
    plt.ylabel("Number of a:s in chapter")
    plt.title("Linear regression: batch descent")

    #stoch final w: [0.0021761452941276367, 0.0664539945969992]
    #batch final w: [-0.00029542083736678514, 0.06642096202088386]

    plt.show()
