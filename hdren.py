#-------------------------------------------------------------------------------
# Name:        HdRen
# Purpose:     rename files adding their header hexdump, for a quick & easy
#              grouping by filetype
#
# Author:      Marco Pontello - http://mark0.net
#
# Created:     02/11/2013
# Copyright:   (c) 2015 Marco Pontello
# License:     The MIT License (MIT) - http://opensource.org/licenses/MIT
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import os
import argparse
import glob
import fnmatch

PROGRAM_VER = "1.00.100b"

PARAMS = {}

def header_intro():
  """Display the usual presentation, version, (C) notices, etc."""
  print
  print "HdRen - hexdump file renamer v%s - (C) 2015 By M.Pontello" % \
        (PROGRAM_VER)
  print

def get_cmdline():
    """
    Evaluate command line parameters, usage & help.
    """
    parser = argparse.ArgumentParser(
             description="Rename a number of files \
             adding their n bytes header hexdump.",
             prefix_chars='-/+',
             version = "DupDel v" + PROGRAM_VER)
    parser.add_argument("filenames", action="store", nargs="+",
                        help="Files to scan (can include path & wildcards)")
    parser.add_argument("-l", "--len", type=int, default=4,
                        help="header's lenght", metavar="n")
    parser.add_argument("-r", "--recurse", action="store_true",
                        help="recurse subdirs")
    res = parser.parse_args()

    PARAMS["files"] = res.filenames
    PARAMS["hdrlen"] = res.len
    PARAMS["recurse"] = res.recurse
    
def hexdump(filename, hdrlen):
    f = open(filename, "rb")
    buffer = f.read(hdrlen)
    f.close()
    buffer = buffer+chr(0x00)*hdrlen
    buffer = buffer[:hdrlen]
    text = ""
    for b in buffer:
        text += "%02x" % ord(b)
    return text.upper()
    
def renfiles(filenames, hdrlen):
    for filename in filenames:
        hextext = hexdump(filename, hdrlen)
        newfilename = os.path.join(os.path.dirname(filename),
                                   hextext + "=" + os.path.basename(filename))
        try:
          os.rename(filename, newfilename)
          print newfilename
        except:
          print "error: can't rename", filename


def main():
    header_intro()
    get_cmdline()

    filenames = []
    for filespec in PARAMS["files"]:
        filepath, filename = os.path.split(filespec)
        for wroot, wdirs, wfiles in os.walk(filepath):
            if not PARAMS["recurse"]:
                wdirs[:] = []
            for fn in fnmatch.filter(wfiles, filename):
              filenames.append(os.path.join(wroot, fn))
              
    filenames = sorted(set(filenames))
    filenames = [os.path.abspath(filename) for filename in filenames]
    hdrlen = PARAMS["hdrlen"]

    renfiles(filenames, hdrlen)
  

if __name__ == '__main__':
    main()
