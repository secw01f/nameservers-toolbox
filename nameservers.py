import dns.resolver
import re
import requests
import argparse
import json
import os

def nsenum(target):
    dom = target
    try:
        dns.resolver.resolve(dom, 'SOA')
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers, dns.resolver.LifetimeTimeout):
        pass
    else:
        try:
            nameservers = dns.resolver.resolve(dom, 'NS')
            servers = []
            for server in nameservers:
                servers.append(str(server.target))
            return(servers)
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers, dns.resolver.LifetimeTimeout):
            pass

def details():
    details = {'name': str(os.path.basename(__file__)).splic('.')[0], 'category': 'recon', 'description': 'Enumerates DNS Nameservers for TLDs of provided target', 'path': os.path.abspath(__file__)}
    return(details)

def module(args):
    argparser = argparse.ArgumentParser(add_help=False)
    argparser.add_argument("-t", "--target", required=True)
    argparser.add_argument("-o", "--output", required=False)
    cmd = argparser.parse_args(args)
    
    results = {'results': [], 'total': 0}

    print(f'[ ! ] Retreiving DNS Name Servers for tlds tied to {cmd.target}\n')

    r = requests.get('https://data.iana.org/TLD/tlds-alpha-by-domain.txt')
    tlds = r.text.split('\n')
    tlds.remove(tlds[0])
    tlds.remove(tlds[(len(tlds) - 1)])

    for tld in tlds:
        domain = str(cmd.target + '.' + tld.lower())
        nservers = nsenum(domain)
        if nservers != None:
            data = {}
            data['domain'] = domain
            data['nameservers'] = nservers
            results['results'].append(data)
            results['total'] = results['total'] + 1
        else:
            pass
    if cmd.output != False:
        with open(str(cmd.target + '.json'), 'w') as file:
            json.dump(results, file)
            file.close()

    print(results)
    return(results)

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(add_help=False)
    argparser.add_argument("-t", "--target", required=True)
    argparser.add_argument("-o", "--output", required=False, action="store_true")
    args = argparser.parse_args()
    
    results = {'results': [], 'total': 0}

    print(f'[ ! ] Retreiving DNS Name Servers for tlds tied to {args.target}\n')

    r = requests.get('https://data.iana.org/TLD/tlds-alpha-by-domain.txt')
    tlds = r.text.split('\n')
    tlds.remove(tlds[0])
    tlds.remove(tlds[(len(tlds) - 1)])

    for tld in tlds:
        domain = str(args.target + '.' + tld.lower())
        nservers = nsenum(domain)
        if nservers != None:
            data = {}
            data['domain'] = domain
            data['nameservers'] = nservers
            results['results'].append(data)
            results['total'] = results['total'] + 1
        else:
            pass
    if args.output != False:
        with open(str(args.target + '.json'), 'w') as file:
            json.dump(results, file)
            file.close()
    
    print(results)