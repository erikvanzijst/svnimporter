#!/usr/bin/env python

import subprocess
import re

p = subprocess.Popen(['svn', 'log', '-v', 'svn://svn.samba.org/subvertpy'],
                     shell=False,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT,
                     bufsize=1)

r = re.compile(r'^r[0-9]+\s\|\s(\w+)\s\|')

line = p.stdout.readline()
while line:
    match = r.match(line)
    if match:
        name = match.group(1)
        print name
    line = p.stdout.readline()

print p.wait()
