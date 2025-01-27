#!/usr/bin/env python3

import os
from bgpdumpy import BGPDump, TableDumpV2

def parse(dir, all_asn=False):
    for file in os.listdir(dir):
        with BGPDump(f'{dir}/{file}') as bgp:
                print(f"Processing {file}...")
                to_dump = ""
                for entry in bgp:
                    if not isinstance(entry.body, TableDumpV2):
                        continue

                    prefix = '%s/%d' % (entry.body.prefix, entry.body.prefixLength)
                    if not all_asn:
                        list_ASN = set([
                            route.attr.asPath.split()[-1]
                            for route
                            in entry.body.routeEntries])

                        for item in list(list_ASN):
                            to_dump += f'{prefix} AS{item}\n'
                    else:
                        list_ASN = set([
                            route.attr.asPath
                            for route
                            in entry.body.routeEntries])
                        
                        for item in list(list_ASN):
                            to_dump += f'{prefix}|{item}\n'

                if not os.path.exists(f"paths-{dir}"):
                    os.mkdir(f"paths-{dir}")
                with open(f'paths-{dir}/{file}', 'w') as w_file:
                    w_file.write(to_dump)