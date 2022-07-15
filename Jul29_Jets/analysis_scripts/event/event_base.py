#!/usr/bin/env python3

"""
  Event class
  
  Author: James Mulligan (james.mulligan@berkeley.edu)
  """

from __future__ import print_function

# Base class
from base import common_base

################################################################
class EventBase(common_base.CommonBase):

    # ---------------------------------------------------------------
    # Constructor
    # ---------------------------------------------------------------
    def __init__(self, **kwargs):
        super(EventBase, self).__init__(**kwargs)
