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

from distutils.cmd import Command
from distutils.core import setup, Extension
import os
import sys
from DOM_version import version as __version__

# Package name and version information
PACKAGE = "DOM"
VERSION = __version__

# Package list
package_list = ['', 'DST', 'SOM']

def pythonVersionCheck():
    # Minimum version of Python
    PYTHON_MAJOR = 2
    PYTHON_MINOR = 3
    
    if sys.version_info < (PYTHON_MAJOR, PYTHON_MINOR):
            print >> sys.stderr, 'You need at least Python %d.%d for %s %s' \
                  % (PYTHON_MAJOR, PYTHON_MINOR, PACKAGE, VERSION)
            sys.exit(3)

            
def parseOptions( argv, keywords ):
    """get values for input keywords

    inputs like:
    --keyword=value

    transformed to a dictionary of 
    {keyword: value}

    if nothing is given, value is set to default: True
    """
    res = {}
    for keyword in keywords:
        for i, item in enumerate(argv):
            if item.startswith(keyword):
                value = item[ len(keyword) + 1: ]
                if value == "": value = True
                res[keyword] = value
                del argv[i]
                pass
            continue
        continue
    return res

def parseCommandLine():
    argv = sys.argv

    keywords = ['--with-nexus']
    options = parseOptions(argv, keywords)

    file_locations = None
    if options.get('--with-nexus'):
        file_locations = options['--with-nexus'].split(',')

    return file_locations


def setupSnsNapiExt(locations):

    if locations is None:
        nexus_incdir = '/usr/local/include'
        nexus_libdir = '/usr/local/lib'
    else:
        if len(locations) == 1:
            nexus_incdir = locations[0]+'/include'
            nexus_libdir = locations[0]+'/lib'
        else:
            nexus_incdir = locations[0]
            nexus_libdir = locations[1]
                    
    incdir_list = [nexus_incdir]
    libdir_list = [nexus_libdir]
    
    nexus_lib = "NeXus"
    lib_list_all = [nexus_lib]
    
    if os.uname()[0] == 'Linux':
        lib_list_all.append('stdc++')
            
    return [Extension("sns_napi",
                      [os.path.join('nexus', 'sns_napi.cpp')],
                      include_dirs = incdir_list,
                      library_dirs = libdir_list,
                      libraries = lib_list_all)]

class build_doc(Command):
    """
    This class is responsible for creating the API documentation via the
    epydoc system.
    """
    description = "Build the Python API documentation"
    user_options = []
    
    def initialize_options(self):
        pass
    
    def finalize_options(self):
        pass
    
    def run(self):
        try:
            epydoc_conf = os.path.join('doc', 'config.epy')
            
            from epydoc import cli
            old_argv = sys.argv[1:]
            
            sys.argv[1:] = [
                "--config=%s" % epydoc_conf,
                "--verbose"
                ]
            cli.cli()
            
            sys.argv[1:] = old_argv

        except ImportError:
            print "Epydoc is needed to create API documentation. Skipping.."

        # Make SNS NAPI documentation via doxygen
        doxygen_conf = os.path.join('doc', 'config.dox')

        doxygen_cmd = "doxygen " + doxygen_conf

        fout = os.popen(doxygen_cmd)
        output = fout.readlines()
        status = fout.close()

        if status is not None:
            status = status >> 8
            if status == 127:
                print "Doxygen is needed to create SNAPI docmentation. "\
                      +"Skipping.."
            else:
                print "Doxygen execution failed with code %d" % status
        else:
            # Everything went fine with doxygen, show the output
            print "Running doxygen....."
            print "".join(output)
                                
if __name__ == "__main__":
    pythonVersionCheck()
    file_locations = parseCommandLine()
    sns_napi_ext = setupSnsNapiExt(file_locations)

    setup(name=PACKAGE,
          version=VERSION,
          extra_path=PACKAGE,
          packages=package_list,
          ext_modules=sns_napi_ext,
          cmdclass = {'build_doc': build_doc})

        

