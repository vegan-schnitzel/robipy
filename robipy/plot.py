import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

def circular_stereo(ax):
    """
    Compute a circle in axes coordinates, which we can use as a boundary
    for the map. We can pan/zoom as much as we like - the boundary will be
    permanently circular.
    Based on: https://scitools.org.uk/cartopy/docs/v0.15/examples/always_circular_stereo.html
    """
    theta = np.linspace(0, 2*np.pi, 100)
    center, radius = [0.5, 0.5], 0.5
    verts = np.vstack([np.sin(theta), np.cos(theta)]).T
    circle = mpl.path.Path(verts * radius + center)

    ax.set_boundary(circle, transform=ax.transAxes)


def coastlines(ax):
    """
    Add coastlines with decent default options to cartopy plot.
    """
    ax.coastlines('110m', lw=0.75, alpha=0.5)


class MidpointNormalize(mpl.colors.Normalize):
    """
    Choose data range while preserving midpoint in divergent colorbars.

    Create a subclass of Normalize based on:
    https://stackoverflow.com/a/50003503
    """
    def __init__(self, vmin, vmax, midpoint=0, clip=False):
        self.midpoint = midpoint
        mpl.colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        normalized_min = max(0, 1 / 2 * (1 - abs((self.midpoint - self.vmin) / (self.midpoint - self.vmax))))
        normalized_max = min(1, 1 / 2 * (1 + abs((self.vmax - self.midpoint) / (self.midpoint - self.vmin))))
        normalized_mid = 0.5
        x, y = [self.vmin, self.midpoint, self.vmax], [normalized_min, normalized_mid, normalized_max]
        return np.ma.masked_array(np.interp(value, x, y))
