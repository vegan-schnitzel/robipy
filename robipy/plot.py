import matplotlib.path as mpath
import numpy as np

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
    circle = mpath.Path(verts * radius + center)

    ax.set_boundary(circle, transform=ax.transAxes)


def coastlines(ax):
    ax.coastlines('110m', lw=0.75, alpha=0.5)