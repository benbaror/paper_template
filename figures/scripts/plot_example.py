from replot import Axes
import numpy as np
import matplotlib.pyplot as plt
import click


@click.command()
@click.option('-s', '--save', default='')
@click.option('--show', is_flag=True)
def main(save, show):

    name = save.split('.')[0].replace('_',' ').capitalize()

    if save.endswith('rplt'):
        ax = Axes(save)
        save = False
    else:
        ax = plt.gca()

    x = np.linspace(0,1)
    ax.plot(x, x**2)
    ax.set_title(name)

    if save:
        plt.savefig(save)

    if show:
        plt.show()


if __name__ == '__main__':
    main()
