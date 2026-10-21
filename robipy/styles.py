"""
Collection of matplotlib styles for different contexts.
"""

import seaborn as sns

# print(plt.rcParams["axes.linewidth"])

# ticks!
# "grid.linewidth" 1.0
# "axes.linewidth" 1.25
# "xtick.major.width" 1.25
# "xtick.minor.width" 1.0

# whitegrid
# "axes.linewidth" 1.25
# "grid.linewidth" 1.0

STYLES = {
    "explore": {
        "seaborn_style": "whitegrid",
        "rcParams": {
            "savefig.dpi": 300,
            "font.size": 12,  # size of axes labels, not tick labels (they're smaller)
            "font.family": ["Inter", "DejaVu Sans"],
            "mathtext.fontset": "stixsans",    # doesn't support arbitrary OpenType math fonts
        },
    },
    "thesis": {
        "seaborn_style": "ticks",
        "rcParams": {
            "savefig.dpi": 300,
            "font.size": 12,  # size of axes labels, not tick labels (they're smaller)
            "font.family": ["Inter", "DejaVu Sans"],
            "mathtext.fontset": "stixsans",    # doesn't support arbitrary OpenType math fonts
            "xtick.color": "0.8",
            "ytick.color": "0.8",
            "axes.edgecolor": "0.8",
            "text.color": "black",  # "black" finally worked, yay
            "axes.labelcolor": "black",
            "xtick.labelcolor": "black",
            "ytick.labelcolor": "black",
            "pgf.rcfonts": False,  # don't setup fonts from rc parameters
            "pgf.texsystem": "lualatex",
            "pgf.preamble": "\n".join([
                r"\usepackage{unicode-math}",  # unicode math setup
                r"\setmainfont{STIX Two Text}",
                r"\setmathfont{STIX Two Math}"
            ])
        },
    },
    "präsi": {
        "seaborn_style": "white",
        "rcParams": {
            "savefig.dpi": 300,
            "font.size": 12,  # size of axes labels, not tick labels (they're smaller)
            "font.family": ["Inter", "DejaVu Sans"],
            "mathtext.fontset": "stixsans",    # doesn't support arbitrary OpenType math fonts
            "text.color": "black",  # "black" finally worked, yay
            "axes.labelcolor": "black",
            "xtick.labelcolor": "black",
            "ytick.labelcolor": "black",
            "pgf.rcfonts": False,  # don't setup fonts from rc parameters
            "pgf.texsystem": "lualatex",
            "pgf.preamble": "\n".join([
                r"\usepackage{unicode-math}",  # unicode math setup
                r"\setmainfont{Fira Sans}",
                r"\setmathfont{Fira Math}"
            ])
        },
    },
}


def add_grid(ax):
    """
    Enable grid and remove now redundant ticks. For "thesis" style.
    """
    ax.grid(True)
    ax.tick_params(which='both', left=False, bottom=False)


def apply_style(style_name):
    """
    Apply a predefined matplotlib style.
    """
    style = STYLES[style_name]
    sns.set_theme(
        style=style["seaborn_style"],
        rc=style["rcParams"]
    )
