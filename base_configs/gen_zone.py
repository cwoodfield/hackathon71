#!/usr/bin/env python2

from __future__ import print_function

from collections import defaultdict, namedtuple
import os.path
import sys
import glob

from jinja2 import Environment, FileSystemLoader
import yaml
import netaddr


RRFields = namedtuple('RRFields', ['rtype', 'rdata'])


TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader('./'),
    trim_blocks=True
)


def render_template(template_filename, context):
  return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)


class ZoneSetBuilder(object):
    def __init__(self, defaults, mgmt_subdomain='mgmt'):
        self.defaults = defaults
        if not defaults['zone'].endswith('.'):
            raise ValueError('Zone name must be fully qualified')
        self.mgmt_subdomain = mgmt_subdomain
        self.fwd = defaultdict(list)
        self.rev4 = defaultdict(list)
        self.rev6 = defaultdict(list)

    def a_ptr(self, name, addr):
        self.fwd[name].append(RRFields('A', str(addr)))
        self.rev4[addr.reverse_dns].append(
                RRFields('PTR', name + '.' + self.defaults['zone'])
        )

    def aaaa_ptr(self, name, addr):
        self.fwd[name].append(RRFields('AAAA', str(addr)))
        self.rev6[addr.reverse_dns].append(
                RRFields('PTR', name + '.' + self.defaults['zone'])
        )

    def build(self, cfg):
        h = cfg['hostname']
        self.a_ptr(h, netaddr.IPNetwork(cfg['lo_ip4_addr']).ip)
        self.aaaa_ptr(h, netaddr.IPNetwork(cfg['lo_ip6_addr']).ip)

        h_mgmt = h + '.' + self.mgmt_subdomain
        if 'mgmt_addr' in cfg:
            self.a_ptr(h_mgmt, netaddr.IPAddress(cfg['mgmt_addr']))
        elif 'fxp0_addr' in cfg:
            self.a_ptr(h_mgmt, netaddr.IPNetwork(cfg['fxp0_addr']).ip)

        for i in cfg['interfaces']:
            addr4 = netaddr.IPNetwork(i['ip4_addr']).ip
            addr6 = netaddr.IPNetwork(i['ip6_addr']).ip
            if ':' in i['description']:
                # a P2P
                remote = i['description'].split(':')[-1]
                name = remote + '.' + h
            else:
                # a GW
                name = i['description'] + '.' + h
            self.a_ptr(name, addr4)
            self.aaaa_ptr(name, addr6)

    def forward(self):
        context = self.defaults.copy()
        context['records'] = self.fwd
        return context

    def reverse4(self):
        context = self.defaults.copy()
        context['zone'] = '.'
        context['records'] = self.rev4
        return context

    def reverse6(self):
        context = self.defaults.copy()
        context['zone'] = '.'
        context['records'] = self.rev6
        return context


def main(args):
    zone_defaults_fname = args[1]
    yaml_dir = args[2]
    zone_dir = args[3]

    # load zone defaults
    with open(zone_defaults_fname) as f:
        zone_defaults = yaml.load(f)

    # iterate over all node data to build zones
    zones = ZoneSetBuilder(zone_defaults)
    for tier in ['leaf', 'spine', 'vmx']:
        g =  os.path.join(yaml_dir, tier + '*.yaml')
        for fname in glob.glob(g):
            with open(fname) as f:
                d = yaml.load(f)
            zones.build(d)

    # render template per zone
    for z in ['forward', 'reverse4', 'reverse6']:
        zone_method = getattr(zones, z)
        zone_fname = os.path.join(zone_dir, z + '.zone')
        with open(zone_fname, 'wt') as f:
            f.write(render_template('TEMPLATES/zone_template.j2',
                                    zone_method()))
        
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
