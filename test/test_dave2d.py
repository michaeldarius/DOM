#!/usr/bin/env python

#                        Data Object Model
#           A part of the SNS Analysis Software Suite.
#
#                  Spallation Neutron Source
#          Oak Ridge National Laboratory, Oak Ridge TN.
#
#
#                             NOTICE
#
# For this software and its associated documentation, permission is granted
# to reproduce, prepare derivative works, and distribute copies to the public
# for any purpose and without fee.
#
# This material was prepared as an account of work sponsored by an agency of
# the United States Government.  Neither the United States Government nor the
# United States Department of Energy, nor any of their employees, makes any
# warranty, express or implied, or assumes any legal liability or
# responsibility for the accuracy, completeness, or usefulness of any
# information, apparatus, product, or process disclosed, or represents that
# its use would not infringe privately owned rights.
#

# $Id$

import DST
from SOM import SOM
from SOM import SO
from time import localtime, strftime, time

filename_SOM1 = "stuff1.dat"

SOM1 = SOM()
SOM1.attr_list["filename"] = filename_SOM1
SOM1.attr_list["epoch"] = time()
SOM1.attr_list["timestamp"] = DST.make_ISO8601(SOM1.attr_list["epoch"])
SOM1.attr_list["username"] = "Michael Reuter and the Gang"
SOM1.setAllAxisLabels(["Q", "E"])
SOM1.setAllAxisUnits(["A-1", "meV"])
SOM1.setYLabel("Intensity")
SOM1.setYUnits("Counts/(meV A-1))")

SO1 = SO(2)
SO1.id = 0
SO1.axis[0].val.extend(range(5))
SO1.axis[1].val.extend(range(10))

y_len = (len(SO1.axis[0].val)-1) * (len(SO1.axis[1].val)-1)
y = range(y_len)
SO1.y.extend(y)
SO1.var_y.extend(y)

SOM1.append(SO1)

file = open(filename_SOM1, "w")

d2d = DST.Dave2dDST(file)
d2d.writeSOM(SOM1)
d2d.release_resource()
