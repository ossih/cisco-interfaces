#!/usr/bin/env python3

import yaml
import argparse

## This is old and deprecated
## Use of if.py is recommended instead

parser = argparse.ArgumentParser('vlan.py')
parser.add_argument('-c', '--config', required=True)

args = parser.parse_args()


with open(args.config, 'r') as f:
    config = yaml.safe_load(f)

for name, vconf in config['vlans'].items():
    vid = vconf['vid']

    print('vlan %i' % vid)
    print(' name %s' % name)
    
