#!/usr/bin/env python3

import os
import signal
import sys
import math
import subprocess
import re
from argparse import ArgumentParser

def parseCommandline():
    parser = ArgumentParser(prog="leakage.py", description="nothing yet", add_help=True)
    parser.add_argument("--centre", help="foo", nargs=3, dest="centre", action="store", type=float, required=True)
    parser.add_argument("--edge-length", help=" ", dest="edge", action="store", type=float, required=True)
    argparse = parser.parse_args()
    return argparse

# def signal_handler(signal, frame):
#     print('You pressed Ctrl+C!')
#     sys.exit(0)

def write_input_file(centre, edge, offset):
    filename = 'gimic.inp'
    # print(centre, edge, offset)
    with open(filename, 'w') as f:
      f.write( 
        'calc=integral\n' +
        'title=""\n' +
        'basis="../MOL"\n' +
        'xdens="../XDENS"\n' +
        'debug=1\n' +
        'openshell = false\n' +
        'magnet = [0.0, 0.0, -1.0]\n' +
        '\n' +
        'Grid(bond) {\n' +
        '     type=gauss\n' +
        '     spacing=[0.01, 0.01, 0.01]\n' +
        '     distance = {:f}\n'.format(edge/2.0) +
        '     coord1 = [{:f}, {:f}, {:f}]\n'.format(centre[0], centre[1], centre[2]) +
        '     coord2 = [{:f}, {:f}, {:f}]\n'.format(centre[0]+offset[0], centre[1]+offset[1], centre[2]+offset[2]) +
        '     width = [-0.1000000, 0.1000000]\n' +
        '     height = [-0.1000000, 0.1000000]\n' +
        '     fixcoord = [{:f}, {:f}, {:f}]\n'.format(centre[0]+0.01, centre[1]+0.01, centre[2]+0.01) +
        '}\n' +
        '\n' +
        ' Advanced {\n' +
        '     lip_order=9\n' +
        '     spherical=off\n' +
        '     diamag=on\n' +
        '     paramag=on\n' +
        '     GIAO=on\n' +
        '     screening=on\n' +
        '     screening_thrs=1.d-8\n' +
        '}'\
      )

def run_gimic():
      p = subprocess.Popen(['/usr/bin/env', 'gimic'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      # print (p)
      out, err = p.communicate()
      out_string = out.decode('utf-8')
      err_string = err.decode('utf-8')
      rx = re.compile('-*\d+.\d+')
      # print(out)
      for line in out_string.splitlines():
        # print(type(line))
        if "Induced current (nA/T)" in line:
          # print(line)
          m = rx.findall(line)
          # print(m[0])
          return float(m[0])


def main():
    # signal.signal(signal.SIGINT, signal_handler)
    args = parseCommandline()
    print(args)
    for x in range(-21, 21):
      for y in range(-21, 21):
        print(x/10.0, y/10.0)
        args.centre = [x/10.0, y/10.0, 0.0]
        
        offsets = [[-args.edge, 0, 0],
                   [args.edge, 0, 0],
                   [0, -args.edge, 0],
                   [0, args.edge, 0],
                   [0, 0, -args.edge],
                   [0, 0, args.edge]]
        # print(offsets)
        contribs = []
        for offset in offsets:
          # print(offset[0])
          write_input_file(args.centre, args.edge, offset)
          # p = subprocess.run(['/usr/bin/env', 'gimic'], capture_output=True)
          c = run_gimic() 
          contribs.append(c)
#        print(contribs)
        print(sum(contribs))

if __name__ == "__main__":
    main()

