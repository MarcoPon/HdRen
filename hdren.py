#-------------------------------------------------------------------------------
# Name:        HdRen
# Purpose:     rename files adding their header hexdump, for a quick & easy
#              grouping by filetype
#
# Author:      Mark
#
# Created:     02/11/2013
# Copyright:   (c) 2013 Marco Pontello
# License:     The MIT License (MIT) - http://opensource.org/licenses/MIT
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import os
import argparse
import glob


PROGRAM_VER = "1.00"

PARAMS = {}

def header_intro():
  """Display the usual presentation, version, (C) notices, etc."""
  print
  print "HdRen - hexdump file renamer v%s - (C) 2013 By M.Pontello" % \
        (PROGRAM_VER)
  print

def get_cmdline():
    """
    Evaluate command line parameters, usage & help.
    """
    parser = argparse.ArgumentParser(
             description="Rename a number of files \
             adding their 4 bytes header hexdump.",
             prefix_chars='-/+',
             version = "DupDel v" + PROGRAM_VER)
    parser.add_argument("filenames", action="store", nargs="+",
                        help = "Files to scan (can include path & wildcards)")
    res = parser.parse_args()

    PARAMS["files"] = res.filenames
    PARAMS["hdrlen"] = 4
    
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
    for filename in PARAMS["files"]:
        if os.path.isdir(filename):
            filename = os.path.join(filename, "*")
        filenames += glob.glob(unicode(filename))
    filenames = [filename for filename in filenames if not os.path.isdir(filename)]
    filenames = sorted(set(filenames))
    filenames = [os.path.abspath(filename) for filename in filenames]
    hdrlen = PARAMS["hdrlen"]

    renfiles(filenames, hdrlen)
    

if __name__ == '__main__':
    main()
