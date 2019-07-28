#!/usr/bin/env python3

import argparse
import jinja2

parser = argparse.ArgumentParser('portchan.py')
parser.add_argument('-c', '--confname')
parser.add_argument('-p', '--prefix', required=True)
parser.add_argument('-f', '--first', type=int, default=1)
parser.add_argument('-o', '--offset', type=int, default=0)
parser.add_argument('-n', '--num', type=int, default=2)
parser.add_argument('-v', '--vlans', default='all')
parser.add_argument('-m', '--mode', default='active')
parser.add_argument('-s', '--switch', default=[], action='append')

args = parser.parse_args()

confname = args.confname
prefix = args.prefix
first = args.first
offset = args.offset
num = args.num
vlans = args.vlans
mode = args.mode
switchlist = args.switch

class Switch(object):
    def __init__(self, switch, vlans, ponum, mode, ifnum, num, prefix):
        self.switch = switch
        self.vlans = vlans
        self.ponum = ponum
        self.mode = mode

        self.slaves = []
        for i in range(num):
            slave = '{}/{}'.format(prefix, ifnum + i)
            self.slaves.append(slave)

ifnum = offset + 1
ponum = first
switches = []
for switch in switchlist:
    switches.append(Switch(switch, vlans, ponum, mode, ifnum, num, prefix))

    ifnum+=num
    ponum+=1

with open('templates/portchan.j2') as f:
    tmpl = jinja2.Template(f.read())

rendered = tmpl.render(switches=switches)

if confname:
    outfile = 'output/portchan-{}.txt'.format(confname)
    with open(outfile, 'w') as f:
        f.write(rendered)
    print('Configuration written into file {}'.format(outfile))

else:
    print(rendered)
