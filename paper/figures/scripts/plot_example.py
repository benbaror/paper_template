from replot import Axes
import numpy as np


if __name__ == '__main__':
    ax = Axes('example.rplt')
    x = np.linspace(0,1)
    ax.plot(x, x**2)
