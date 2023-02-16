#!/usr/bin/env python3

# ansibleguy.infra_pki
# script for certificate discovery - can be used by monitoring systems like Zabbix

from sys import argv as sys_argv
from pathlib import Path
from json import dumps as json_dumps

if len(sys_argv) < 2:
    raise ValueError('You need to provide the path to a directory that contains certificates (.crt)!')

CERT_DIR = sys_argv[1]

print(json_dumps({
    'data': [
        str(item) for item in Path(CERT_DIR).glob('**/*')
        if item.is_file() and str(item).endswith('.crt')
    ]
}))
