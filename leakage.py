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
    parser.add_argument("--origin", help="foo", nargs=3, dest="origin", action="store", type=float, required=False, default=[0.0 ,0.0 ,0.0])
    parser.add_argument("--steps", help="number of steps in +x, -x, +y, -y, +z, -z", nargs=6, dest="steps", action="store", type=int, required=False, default=[1, 1, 1, 1, 0, 0])
    parser.add_argument("--step-length", help=" ", nargs=1, dest="edge", action="store", type=float, required=False, default=0.1 )
    argparse = parser.parse_args()
    return argparse

def check_input(args):
    ones = 0
    for d in {0, 1, 2}:
      if args.steps[2*d] + args.steps[2*d+1] == 0:
        ones += 1
      if args.steps[2*d] + args.steps[2*d+1] < 0:
        return False
      # print("ones ", ones)
    if ones != 1:
      print("invalid step counts")
      return False
    return True


# def signal_handler(signal, frame):
#     print('You pressed Ctrl+C!')
#     sys.exit(0)

def write_input_file(voxel_centre, edge, offset):
    filename = 'gimic.inp'
    # print("voxel_centre, edge, off", voxel_centre, edge, offset)
      
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
        '     distance = {:f}\n'.format(edge/2.0) + # plane in the middle
        '     coord1 = [{:f}, {:f}, {:f}]\n'.format(voxel_centre[0], voxel_centre[1], voxel_centre[2]) +
        '     coord2 = [{:f}, {:f}, {:f}]\n'.format(voxel_centre[0]+offset[0], voxel_centre[1]+offset[1], voxel_centre[2]+offset[2]) +
        '     width = [{:f}, {:f}]\n'.format(-edge, edge) +
        '     height = [{:f}, {:f}]\n'.format(-edge, edge) +
        '     fixcoord = [{:f}, {:f}, {:f}]\n'.format(voxel_centre[0]+0.01, voxel_centre[1]+0.01, voxel_centre[2]+0.01) +
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
    check_input(args)
    print(args)

    print("xrange: ", args.origin[0] - args.steps[0] * args.edge, args.origin[0] + args.steps[1] * args.edge)
    print("yrange: ", args.origin[1] - args.steps[2] * args.edge, args.origin[1] + args.steps[3] * args.edge)
    print("zrange: ", args.origin[2] - args.steps[4] * args.edge, args.origin[2] + args.steps[4] * args.edge)
    for x in range(-args.steps[0], args.steps[1] + 1):
      for y in range(-args.steps[2], args.steps[3] + 1):
        for z in range(-args.steps[4], args.steps[5] + 1):
          print("x, y, z: ", x, y, z)
          # args.origin = [x/10.0, y/10.0, 0.0]
          voxel_centre = [args.origin[0] + x*args.edge, args.origin[1] + y*args.edge, args.origin[2] + z*args.edge]
          
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
            write_input_file(voxel_centre, args.edge, offset)
            # p = subprocess.run(['/usr/bin/env', 'gimic'], capture_output=True)
            c = run_gimic() 
            contribs.append(c)
#          print(contribs)
          print(sum(contribs))

if __name__ == "__main__":
    main()

