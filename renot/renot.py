"""
This module is the main file for running renot.
"""
import sys
import os
import argparse
import logging
from pathlib import Path

from xrns import XrnsFile


__date__ = '2023-10-24'
__updated__ = '2023-10-24'
__author__ = 'micahanichols27@gmail.com'


def main(argv=None):
    # try parsing arguments
    try:
        parser = argparse.ArgumentParser(
            epilog='Convert Renoise project files into a Goise resource (a Godot plugin)',
            description='MIT License 2023 - Micah Nichols'
        )
        parser.add_argument('-f', '--filepath', dest='filepath', type=str, help='the directory of a .xrns project file')

        args = parser.parse_args(argv or sys.argv[1:])

    except Exception as e:
        name = os.path.basename(sys.argv[0])
        indent = len(name) * " "
        sys.stderr.write(name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

    # try to create a project file
    xrns = XrnsFile(args.filepath)

    # completion
    return 0


if __name__ == "__main__":
    sys.exit(main())
