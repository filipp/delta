#!/usr/bin/env python

import sys
import os.path
import difflib
import tempfile
import requests
from hashlib import sha1
from html2text import html2text


def main(url):
    old_hash = ''
    changed  = True

    html = requests.get(url).text
    text = html2text(html).encode('utf-8')
    new_hash = sha1(text).hexdigest()

    urlhash  = sha1(url).hexdigest()
    tmp_path = os.path.join(tempfile.gettempdir(), urlhash)

    if os.path.exists(tmp_path):
        tmp_file = open(tmp_path, 'r')
        old_hash = sha1(tmp_file.read()).hexdigest()
        changed  = new_hash != old_hash

    tmp_file = open(tmp_path, 'w')
    tmp_file.write(text)
    return changed


if __name__ == '__main__':
    changed = main(sys.argv[1])
    sys.exit(0 if changed else 1)
