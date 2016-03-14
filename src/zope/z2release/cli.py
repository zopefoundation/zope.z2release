"""
Generate an index file based on the version.cfg file of Zope 2
in order to provide a version specific index page generated to be used
in combination with easy_install -i <some_url>
"""

import os
import sys
import urllib

from zope.z2release.utils import CasePreservingConfigParser
from zope.z2release.utils import write_index


def fetch_cfg(url, version_file):
    print('Fetching %s' % url)
    response = urllib.urlopen(url)
    if response.code == 200:
        data = response.read()
        with open(version_file, 'w') as fd:
            fd.write(data)
    else:
        raise ValueError('Failed to fetch %s' % url)


def write_versions(version_file, dirname):
    CP = CasePreservingConfigParser()
    CP.read(version_file)
    for package in CP.options('versions'):
        version = CP.get('versions', package)
        if '#' in version:
            version = version.split('#')[0].strip()
        write_index(package, version, dirname)
    return CP


def build_version_file(name, dirname, url):
    version_file = os.path.join(dirname, name)
    fetch_cfg(url, version_file)
    return write_versions(version_file, dirname)


GITHUB_RAW = 'https://raw.githubusercontent.com/zopefoundation/Zope' 

def main():
    if len(sys.argv) != 3:
        print('Usage: z2_kgs <tag-name> <destination-dirname>')
        print('Example: z2_kgs 2.13.15 '
            '/var/www/download.zope.org/Zope2/index/2.13.15/')
        sys.exit(1)

    tag = sys.argv[1]
    dirname = sys.argv[2]
    if not os.path.exists(dirname):
        print('Creating index directory: %s' % dirname)
        os.makedirs(dirname)

    if tuple(tag.split('.')) >= (2, 13, 23):
        url = '%s/%s/buildout.cfg' % (GITHUB_RAW, tag)
    else:
        url = '%s/%s/versions.cfg' % (GITHUB_RAW, tag)
    CP = build_version_file('versions.cfg', dirname, url)

    buildout = CP.options('buildout')
    if 'extends' in buildout:
        extends = CP.get('buildout', 'extends').split('\n')
        name = 'ztk-versions.cfg'
        for extend in extends:
            if name in extend:
                url = '%s/%s/ztk-versions.cfg' % (GITHUB_RAW, tag)
                build_version_file(name, dirname, url)


if __name__ == '__main__':
    main()
