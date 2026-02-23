"""
Some snippets of code that didn't quite make it into 
production, but are too precious to be deleted.
"""

import matplotlib as mpl
import numpy as np


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
