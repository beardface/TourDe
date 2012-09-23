import matplotlib
matplotlib.use("Agg")
 
import matplotlib.backends.backend_agg as agg

import pylab
import pygame
from pygame.locals import *
import numpy as np

def adjust_borders(fig, targets):
    "Translate desired pixel sizes into percentages based on figure size."
    dpi = fig.get_dpi()
    width, height = [float(v * dpi) for v in fig.get_size_inches()]
    conversions = {
        'top': lambda v: 1.0 - (v / height),
        'bottom': lambda v: v / height,
        'right': lambda v: 1.0 - (v / width),
        'left': lambda v: v / width,
        'hspace': lambda v: v / height,
        'wspace': lambda v: v / width,
        }
    opts = dict((k, conversions[k](v)) for k, v in targets.items())
    fig.subplots_adjust(**opts)


def get_chart(data, step):
 
   fig = pylab.figure(figsize=[1.5, 1], # Inches
                   dpi=100,        # 100 dots per inch, so the resulting buffer is 400x400 pixels
                   )
   ax = fig.gca()
   pylab.setp(pylab.getp(pylab.gca(), 'xticklabels'), visible=False)  
   pylab.setp(pylab.getp(pylab.gca(), 'yticklabels'), visible=False)  
   pylab.setp(pylab.getp(pylab.gca(), 'xgridlines'), 'linestyle', ' ')
   pylab.setp(pylab.getp(pylab.gca(), 'ygridlines'), 'linestyle', ' ')
   ax.plot(data)
   ax.grid(True)

   targets = dict(left=2, right=2, top=2, bottom=2, hspace=0, wspace=0)
   fig.canvas.mpl_connect('resize_event', lambda e: adjust_borders(fig, targets))
   adjust_borders(fig, targets)
   
   ax.plot([step], [data[step]], 'ro')
   canvas = agg.FigureCanvasAgg(fig)
   
   canvas.draw()
   renderer = canvas.get_renderer()
   raw_data = renderer.tostring_rgb()
   return pygame.image.fromstring(raw_data, canvas.get_width_height(), "RGB")
 

