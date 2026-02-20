"""
Everything related to creating figures.
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import calendar

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


def gridlines(ax):
    """
    Add gridlines with decent default options to cartopy plot.
    """
    ax.gridlines(linewidth=0.4, alpha=0.4, color='k', linestyle='--')


def bhx_box(ax, res=50):
    """
    Draw BHx bounding box (adding points to increase resolution).
    """
    ax.plot(
        np.append(np.linspace(140,230,res), [230, 140, 140]),
        np.append(np.repeat(73,res), [90, 90, 73]),
        marker=None, c='k', lw=1, alpha=0.9, transform=ccrs.PlateCarree()
    )


def months_as_letter(ax):
    """
    Translates integer month values to single-letter abbreviation.
    
    Parameters
    ----------
    ax : matplotlib.axes
    """
    formatter = mpl.ticker.FuncFormatter(
        # why +1 though?
        lambda x, pos: calendar.month_abbr[x+1][0]
    )
    ax.xaxis.set_major_formatter(formatter)


class MidpointNormalize(mpl.colors.Normalize):
    """
    Choose data range while preserving midpoint in divergent colorbars.
    Caution: Should be used together with ClippedAutoLocator or MidpointAutoLocator
             to avoid inconsistent colorbar tick labels!

    Creates a subclass of mpl.colors.Normalize based on:
    https://stackoverflow.com/a/50003503
    """
    def __init__(self, vmin=None, vmax=None, midpoint=0, clip=False):
        self.midpoint = midpoint
        super().__init__(vmin, vmax, clip)

    def __call__(self, value):
        nmin, nmid, nmax = self._normalized_bounds()
        x, y = [self.vmin, self.midpoint, self.vmax], [nmin, nmid, nmax]
        return np.ma.masked_array(np.interp(value, x, y))

    def _normalized_bounds(self):
        nmin = max(0, 1 / 2 * (1 - abs((self.midpoint - self.vmin) / (self.midpoint - self.vmax))))
        nmax = min(1, 1 / 2 * (1 + abs((self.vmax - self.midpoint) / (self.midpoint - self.vmin))))
        return nmin, 0.5, nmax


class ClippedAutoLocator(mpl.ticker.MaxNLocator):
    """
    Subclass of mpl.ticker.AutoLocator that strictly clips ticks to [vmin, vmax].
    """
    def __init__(self, nbins='auto', steps=[1, 2, 2.5, 5, 10]):
        super().__init__(nbins=nbins, steps=steps)

    def tick_values(self, vmin, vmax):
        ticks = super().tick_values(vmin, vmax)
        return ticks[(ticks >= vmin) & (ticks <= vmax)]


class MidpointAutoLocator(mpl.ticker.MaxNLocator):
    """
    Tick locator that forces ticks at vmin, midpoint, vmax.
    Other ticks (if any) follow AutoLocator's logic.
    """
    def __init__(self, midpoint=0, nbins='auto', steps=[1, 2, 2.5, 5, 10]):
        self.midpoint = midpoint
        super().__init__(nbins=nbins, steps=steps)

    def tick_values(self, vmin, vmax):
        # get default clipped ticks
        ticks = super().tick_values(vmin, vmax)
        ticks = ticks[(ticks >= vmin) & (ticks <= vmax)]

        # replace the edge ticks with exact vmin/vmax
        ticks[0] = vmin
        ticks[-1] = vmax

        # find the auto tick closest to midpoint
        idx = np.abs(ticks - self.midpoint).argmin()
        ticks[idx] = self.midpoint

        return ticks


class MidpointMixedFormatter(mpl.ticker.FuncFormatter):
    """
    Formatter for mixed decimal/integer ticks.
    NOTE: At some point just manually change ticks with FixedLocator!
    """
    def __init__(self, vmin, vmax, midpoint=0, decimals=2):
        self.vmin = vmin
        self.vmax = vmax
        self.midpoint = midpoint
        self.decimals = decimals
        super().__init__(self._format)

    def _format(self, x, pos):
        if (abs(x - self.vmin) < 1e-6) or (abs(x - self.vmax)) < 1e-6 or (abs(x - self.midpoint) < 1e-6):
            return f"{np.round(x, self.decimals)}"
        else:
            return f"{int(np.round(x))}"


class EdgeAutoLocator(mpl.ticker.MaxNLocator):
    """
    Subclass of mpl.ticker.AutoLocator that strictly places ticks at vmin & vmax.
    """
    def __init__(self, nbins='auto', steps=[1, 2, 2.5, 5, 10]):
        super().__init__(nbins=nbins, steps=steps)

    def tick_values(self, vmin, vmax):
        ticks = super().tick_values(vmin, vmax)
        ticks = ticks[(ticks >= vmin) & (ticks <= vmax)]

        # replace the edge ticks with exact vmin/vmax
        ticks[0] = vmin
        ticks[-1] = vmax

        return ticks


class EdgeMixedFormatter(mpl.ticker.FuncFormatter):
    """
    Formatter for mixed decimal/integer ticks.
    """
    def __init__(self, vmin, vmax, edge_decimals=2, other_decimals=0):
        self.vmin = vmin
        self.vmax = vmax
        self.edge_decimals = edge_decimals
        self.other_decimals = other_decimals
        super().__init__(self._format)

    def _format(self, x, pos):
        # handle vmin/vmax (compare values directly)
        if abs(x - self.vmin) < 1e-6 or abs(x - self.vmax) < 1e-6:
            return f"{x:.{self.edge_decimals}f}"
        return f"{x:.{self.other_decimals}f}"
