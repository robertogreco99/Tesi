#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

from csvgraph.process import *


######################################################################################################
# Graph properties
class GPLOT:
    """
    Basic class that contains the properties of the graph (e.g., grid on/off, size in pixels etc.)

    """

    def __init__(self, grid=True, enhanced=False, w=800, h=600, option_str=""):
        """
        This is the constructor method. All parameters are optional, and can be assigned later.
        """
        self.grid_str = '' if grid else 'no'  # String: either "" or "no"  (used directly in gnuplot command string)
        self.enhanced_str = '' if enhanced else 'no'  # String: either "" or "no"  (used directly in gnuplot command string)
        self.w = w
        self.h = h
        self.option_str = option_str
        self.graph_data = None

        self.counter_n = 0

    def set_grid(self, grid):
        self.grid_str = '' if grid else 'no'

    def set_enhanced(self, enhanced):
        self.enhanced_str = '' if enhanced else 'no'

