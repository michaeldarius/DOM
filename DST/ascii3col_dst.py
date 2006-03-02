###############################################################################
#
# This class creates a 3 column ASCII file with a metadata header. The
# formatting is based on spec
# (http://www.certif.com/spec_manual/user_1_4_1.html) file format.
#
# $Id$
#
###############################################################################

import dst_base
import math
import sys

class Ascii3ColDST(dst_base.DST_BASE):
    MIME_TYPE="text/Spec"
    EMPTY=""
    COLUMNS=3
    
    ########## DST_BASE functions

    def __init__(self, resource, *args, **kwargs):
        self.__file = resource


    def release_resource(self):
        self.__file.close()


    def writeSO(self,so):
        self.writeData(so)


    def writeSOM(self,som):
        self.writeHeader(som)
        self.__counter = 1
        for so in som:
            self.writeData(so)

    ########## Special functions

    def writeHeader(self,som):
        print >> self.__file, "#F",som.attr_list["filename"]
        print >> self.__file, "#E",som.attr_list["epoch"]
        print >> self.__file, "#D",som.attr_list["timestamp"]
        if som.attr_list.has_key("run_number"):
            print >> self.__file, "#C Run Number:",som.attr_list["run_number"]
        print >> self.__file, "#C Title:",som.attr_list["title"]
        if som.attr_list.has_key("username"):
            print >> self.__file, "#C User:",som.attr_list["username"]
        if som.attr_list.has_key("operations"):
            for op in som.attr_list["operations"]:
                print >> self.__file, "#C Operation",op
        if som.attr_list.has_key("parents"):
            print >> self.__file, "#C Parent Files"
            pdict = som.attr_list["parents"]
            for key in pdict:
                print >> self.__file, "#C %s: %s" % (key, pdict[key]) 

        self.__axes_and_units = "#L %s(%s) %s(%s) Sigma(%s)" \
        % (som.attr_list["x_label"], som.attr_list["x_units"],
           som.attr_list["y_label"], som.attr_list["y_units"],
           som.attr_list["y_units"])

    def writeData(self,so):
        print >> self.__file, self.EMPTY
        print >> self.__file, "#S",self.__counter,"Spectrum ID",so.id
        print >> self.__file, "#N", self.COLUMNS
        print >> self.__file, self.__axes_and_units
        for i in range(len(so)+1):
            print >> self.__file, so.x[i]," ",
            if i < len(so.y):
                print >> self.__file, so.y[i]," ",
                print >> self.__file, math.sqrt(so.var_y[i])
            else:
                print >> self.__file, self.EMPTY

        self.__counter += 1
