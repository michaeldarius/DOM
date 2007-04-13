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

def make_ISO8601(now=None):
    """
    This function takes an optional argument of a UNIX time and converts that
    time to an ISO-8601 standard time string. If no UNIX time is given, the
    default is to use the current time.

    Parameters:
    ----------
    -> now (OPTIONAL) is a UNIX time (number of seconds after Jan 1, 1970)

    Returns:
    -------
    <- a time string in ISO-8601 standard format
    """
    
    import datetime
    import ltz
    Local = ltz.LocalTimezone()

    if now != None:
        return datetime.datetime(2006,1,1).fromtimestamp(now,Local).isoformat()
    else:
        return datetime.datetime(2006,1,1).now(Local).isoformat()


def make_magic_key():
    """
    This function creates a unique key for SNS created files.

    Returns:
    -------
    <- a unique key
    """

    import random
    import time

    key = str(time.time())
    key = key.split('.')[0]+key.split('.')[1]

    adders = random.randint(1,10)

    for i in range(adders):
        len_s = len(key)
        ins = random.randint(0,len_s)
        val = random.randint(0,9)
        key = key[0:ins]+str(val)+key[ins:]
    
    return key

def write_spec_header(ofile, epoch, som):
    """
    This function writes a header based on the Spec file format.
    http://www.certif.com/spec_manual/user_1_4_1.html

    Parameters:
    ----------
    -> ofile is the handle to the output file
    -> epoch is the UNIX time at creation
    -> som is the associated data
    """

    file_keys = [key for key in som.attr_list.keys() \
                 if key.find("-filename") != -1]
    if len(file_keys):
        for file_key in file_keys:
            tag = file_key.split('-')[0]
            try:
                som.attr_list[file_key].reverse()
                som.attr_list[file_key].reverse()
                for file in som.attr_list[file_key]:
                    print >> ofile, "#F %s: %s" % (tag, file)
            except AttributeError:
                print >> ofile, "#F %s: %s" % (tag, som.attr_list[file_key])
    else:
        print >> ofile, "#F", som.attr_list["filename"]

    print >> ofile, "#E", epoch
    print >> ofile, "#D", make_ISO8601(epoch)
        
    if som.attr_list.has_key("run_number"):
        print >> ofile, "#C Run Number:",som.attr_list["run_number"]
    else:
        pass
        
    print >> ofile, "#C Title:",som.getTitle()
    if som.attr_list.has_key("notes"):
        print >> ofile, "#C Notes:", som.attr_list["notes"]
    else:
        pass
    
    if som.attr_list.has_key("username"):
        print >> ofile, "#C User:",som.attr_list["username"]
    else:
        pass
    
    if som.attr_list.has_key("detector_angle"):
        print >> ofile, "#C Detector Angle:",\
              som.attr_list["detector_angle"]
    else:
        pass
    
    if som.attr_list.has_key("operations"):
        for op in som.attr_list["operations"]:
            print >> ofile, "#C Operation",op
    else:
        pass
    
    if som.attr_list.has_key("parents"):
        print >> ofile, "#C Parent Files"
        pdict = som.attr_list["parents"]
        for key in pdict:
            print >> ofile, "#C %s: %s" % (key, pdict[key]) 
    else:
        pass

    if som.attr_list.has_key("proton_charge"):
        print >> ofile, "#C Proton Charge:",\
              str(som.attr_list["proton_charge"])
    else:
        pass

