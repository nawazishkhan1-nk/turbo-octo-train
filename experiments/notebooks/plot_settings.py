import matplotlib
from matplotlib import pyplot as plt
from matplotlib import gridspec, cm
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

import palettable

# General size settings
TEXTWIDTH = 9.  # inches

FONTSIZE = 9.

# Colormap
CMAP = cm.plasma
CMAP_R = cm.plasma_r
# CMAP = palettable.scientific.sequential.Batlow_20.mpl_colormap
# CMAP = palettable.scientific.sequential.Tokyo_20.mpl_colormap
# CMAP = palettable.scientific.sequential.LaJolla_20_r.mpl_colormap

# Colors
COLORS = [CMAP(i/4.) for i in range(5)]
# COLORS = palettable.scientific.sequential.Batlow_6.mpl_colors
# COLORS = palettable.scientific.sequential.Tokyo_5.mpl_colors

COLOR_NEUTRAL1 = "black"
COLOR_NEUTRAL2 = "0.7"
COLOR_NEUTRAL3 = "0.4"
COLOR_NEUTRAL4 = "white"

COLOR_AF2D = COLOR_NEUTRAL2
COLOR_MADMINER = COLOR_NEUTRAL3
# COLOR_FLMS = COLORS[2]
# COLOR_FLMES = COLORS[2]
COLOR_AF = COLORS[3]
COLOR_PIE = COLORS[2]
COLOR_FLMA = COLORS[1]
COLOR_FLMEA = COLORS[0]


def setup():
    matplotlib.rcParams.update({'font.size': FONTSIZE})  # controls default text sizes
    matplotlib.rcParams.update({'axes.titlesize': FONTSIZE})  # fontsize of the axes title
    matplotlib.rcParams.update({'axes.labelsize': FONTSIZE})  # fontsize of the x and y labels
    matplotlib.rcParams.update({'xtick.labelsize': FONTSIZE})  # fontsize of the tick labels
    matplotlib.rcParams.update({'ytick.labelsize': FONTSIZE})  # fontsize of the tick labels
    matplotlib.rcParams.update({'legend.fontsize': FONTSIZE})  # legend fontsize
    matplotlib.rcParams.update({'figure.titlesize': FONTSIZE})  # fontsize of the figure title
    matplotlib.rcParams.update({'figure.dpi': 300})
    matplotlib.rcParams.update({'savefig.dpi': 300})


def figure(cbar=False, height=TEXTWIDTH*0.5, large_margin=0.14, small_margin=0.03, cbar_sep=0.02, cbar_width=0.04, make3d=False, l_space=True, r_space=False, b_space=True, t_space=False):
    """ Single plot, with or without colorbar, size specified by height """

    if cbar:
        top = large_margin if t_space else small_margin
        bottom = large_margin if b_space else small_margin
        left = large_margin if l_space else small_margin
        right = large_margin + cbar_width + cbar_sep
        
        width = height * (1. + cbar_sep + cbar_width + right + left - top - bottom)
        
        cleft = 1. - (large_margin + cbar_width) * height / width
        cbottom = bottom
        cwidth = cbar_width * height / width
        cheight = 1. - top - bottom

        fig = plt.figure(figsize=(width, height))
        if make3d:
            ax = Axes3D(fig)
        else:
            ax = plt.gca()
        plt.subplots_adjust(
            left=left * height / width,
            right=1. - right * height / width,
            bottom=bottom,
            top=1. - top,
            wspace=0.,
            hspace=0.,
        )
        cax = fig.add_axes([cleft, cbottom, cwidth, cheight])

        plt.sca(ax)

        return fig, (ax, cax)
    else:
        left = large_margin if l_space else small_margin
        right = large_margin if r_space else small_margin
        top = large_margin if t_space else small_margin
        bottom = large_margin if b_space else small_margin
        
        width = height * (1. + cbar_sep + cbar_width + right + left - top - bottom)

        fig = plt.figure(figsize=(width, height))
        if make3d:
            ax = Axes3D(fig)
        else:
            ax = plt.gca()
        plt.subplots_adjust(
            left=left,
            right=1. - right,
            bottom=bottom,
            top=1. - top,
            wspace=0.,
            hspace=0.,
        )

        return fig, ax


def figure_width(width=TEXTWIDTH*0.5, large_margin=0.14, small_margin=0.03, make3d=False, l_space=True, r_space=False, b_space=True, t_space=False):
    left = large_margin if l_space else small_margin
    right = large_margin if r_space else small_margin
    top = large_margin if t_space else small_margin
    bottom = large_margin if b_space else small_margin
    
    panel_size = (1. - top - bottom)
    
    height = width / (1. + right + left - top - bottom)
    
    return figure(False, height, large_margin, small_margin, 0.02, 0.04, make3d, l_space, r_space, b_space, t_space)


def grid(nx=4, ny=2, height=0.5*TEXTWIDTH, aspect_ratio=1.0, large_margin=0.14, small_margin=0.03, sep=0.02, l_space=True, r_space=False, b_space=True, t_space=False):
    """ Simple grid, no colorbars, size specified by height """

    # Geometry
    left = large_margin if l_space else small_margin
    right = large_margin if r_space else small_margin
    top = large_margin if t_space else small_margin
    bottom = large_margin if b_space else small_margin

    panel_size = (1. - top - bottom - (ny - 1)*sep)/ny
    width = height*aspect_ratio*(left + nx*panel_size + (nx-1)*sep + right)

    # wspace and hspace are complicated beasts
    avg_width_abs = (height*panel_size * nx * ny) / (nx * ny + ny)
    avg_height_abs = height*panel_size
    wspace = sep * height / avg_width_abs
    hspace = sep * height / avg_height_abs

    # Set up figure
    fig = plt.figure(figsize=(width, height))
    gs = gridspec.GridSpec(ny, nx, width_ratios=[1.]*nx, height_ratios=[1.] * ny)
    plt.subplots_adjust(
        left=left * height / width,
        right=1. - right * height / width,
        bottom=bottom,
        top=1. - top,
        wspace=wspace,
        hspace=hspace,
    )
    return fig, gs


def grid_width(nx=4, ny=2, width=TEXTWIDTH, aspect_ratio=1.0, large_margin=0.14, small_margin=0.03, sep=0.02, l_space=True, r_space=False, b_space=True, t_space=False):
    """ Simple grid, no colorbars, size specified by width """

    left = large_margin if l_space else small_margin
    right = large_margin if r_space else small_margin
    top = large_margin if t_space else small_margin
    bottom = large_margin if b_space else small_margin
    panel_size = (1. - top - bottom - (ny - 1)*sep)/ny
    height = width / (left + nx*panel_size + (nx - 1)*sep + right) / aspect_ratio
    return grid(nx, ny, height, aspect_ratio, large_margin, small_margin, sep, l_space=l_space, r_space=r_space, t_space=t_space, b_space=b_space)


def grid2(nx=4, ny=2, height=TEXTWIDTH*0.5, large_margin=0.14, small_margin=0.03, sep=0.02, cbar_width=0.04):
    """ Grid, colorbars on the right, size specified by height """

    # Geometry
    left = small_margin
    right = large_margin
    top = small_margin
    bottom = small_margin


    panel_size = (1. - top - bottom - (ny - 1)*sep)/ny
    width = height*(left + nx*panel_size + cbar_width + nx*sep + right)

    # wspace and hspace are complicated beasts
    avg_width_abs = (height*panel_size * nx * ny + ny * cbar_width * height) / (nx * ny + ny)
    avg_height_abs = height*panel_size
    wspace = sep * height / avg_width_abs
    hspace = sep * height / avg_height_abs

    # Set up figure
    fig = plt.figure(figsize=(width, height))
    gs = gridspec.GridSpec(ny, nx + 1, width_ratios=[1.]*nx + [cbar_width], height_ratios=[1.] * ny)
    plt.subplots_adjust(
        left=left * height / width,
        right=1. - right * height / width,
        bottom=bottom,
        top=1. - top,
        wspace=wspace,
        hspace=hspace,
    )
    return fig, gs


def grid2_width(nx=4, ny=2, width=TEXTWIDTH, large_margin=0.14, small_margin=0.03, sep=0.02, cbar_width=0.04):
    """ Grid, colorbars on the right, size specified by width """

    left = small_margin
    right = small_margin
    top = small_margin
    bottom = small_margin
    panel_size = (1. - top - bottom - (ny - 1)*sep)/ny
    height = width / (left + nx*panel_size + cbar_width + nx*sep + right)
    return grid2(nx, ny, height, large_margin, small_margin, sep, cbar_width)


def add_transparency(color, alpha):
    if isinstance(color, str):
        color2 = np.array(matplotlib.colors.to_rgba(color))
    else:
        color2 = np.copy(np.array(color))

    if len(color2.shape) == 1:
        if color2.shape[0] == 4:
            color2[3] = alpha
            return color2
        elif color2.shape[0] == 3:
            return np.hstack((color2, [alpha]))

    else:
        if color2.shape[1] == 4:
            color2[:, 3] = alpha
            return color2
        elif color2.shape[1] == 3:
            return np.hstack((color2, alpha * np.ones((color2.shape[0], 1))))
