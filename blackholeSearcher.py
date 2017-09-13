#Number of black holes per halos

import pynbody
import matplotlib as plt
import numpy as np

snap     = 'h148.cosmo50PLK.3072g3HbwK1BH.000139'   #  use the real filename here!
s        = pynbody.load(snap)
BHfilter = pynbody.filt.BandPass('tform','-15 Gyr','0 Gyr')
BH       = s.star[BHfilter]