#!/usr/bin/env python3

import os
import sys
import ipaddress
import yaml
import argparse
import jinja2

if not os.path.isdir('output'):
    os.mkdir('output')

parser = argparse.ArgumentParser('if.py')
parser.add_argument('-c', '--config', required=True)
parser.add_argument('-e', '--event')

args = parser.parse_args()

if args.event:
    event = args.event
else:
    event = args.config.rsplit('.')[0]


class Vlan(object):
    def __init__(self, vid, name, vconf, helpers=[], dhcpv6=[]):
        self.ipv4 = vconf.get('ipv4', None)
        self.ipv6 = vconf.get('ipv6', None)
        self.dhcp = vconf.get('dhcp', True)
        self.urpf = vconf.get('urpf', True)
        self.l2mtu = vconf.get('l2mtu', None)
        self.hsrp_invert = vconf.get('hsrp_invert', False)
        self.helpers = self.dhcp and helpers or []

        self.vid = vid
        self.name = name
        self.dhcpv6 = dhcpv6

        if self.hsrp_invert:
            self.hsrp_prio1 = 5
            self.hsrp_prio2 = 10
        else:
            self.hsrp_prio1 = 10
            self.hsrp_prio2 = 5


        if self.ipv4:
            self.net4 = ipaddress.IPv4Network(self.ipv4)
            self.hosts4 = self.net4.hosts()
            self.gw4 = next(self.hosts4)
            self.gw4_1 = next(self.hosts4)
            self.gw4_2 = next(self.hosts4)
            self.mask4 = self.net4.netmask

        if self.ipv6:
            self.net6 = ipaddress.IPv6Network(self.ipv6)
            self.hosts6 = self.net6.hosts()
            self.gw6 = next(self.hosts6)
            self.gw6_1 = next(self.hosts6)
            self.gw6_2 = next(self.hosts6)
            self.prefixlen6 = self.net6.prefixlen

with open(args.config, 'r') as f:
    config = yaml.load(f)

conf = config['conf']
helpers = conf['helpers']
dhcpv6 = conf['dhcpv6']

vlans = []
for name, vconf in config['vlans'].items():
    vid = vconf['vid']
    
    vlans.append(Vlan(vid, name, vconf, helpers, dhcpv6))
    vlans.sort(key=lambda x: x.vid)


outfiles = [
        ('templates/vlan.j2', 'output/{}-vlan.txt'),
        ('templates/gw.j2', 'output/{}-gw.txt'),
        ('templates/gw1.j2', 'output/{}-gw1.txt'),
        ('templates/gw2.j2', 'output/{}-gw2.txt')
        ]


for tmplfile, outfile in outfiles:
    with open(tmplfile, 'r') as f:
        tmpl = jinja2.Template(f.read())
    with open(outfile.format(event), 'w') as f:
        f.write(tmpl.render(vlans=vlans))
    print('Written {}'.format(outfile).format(event))

