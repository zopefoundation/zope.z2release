import json
import os
import urlparse
import urllib2

from ConfigParser import RawConfigParser as ConfigParser


def _pypi_release_dists(project, version):
    pypi = 'https://pypi.python.org/pypi/%s/%s/json' % (project, version)
    try:
        response = urllib2.urlopen(pypi)
    except urllib2.HTTPError:
        if '-' in project:
            project = project.replace('-', '_')
            pypi = 'https://pypi.python.org/pypi/%s/%s/json' % (project,
                                                                version)
            response = urllib2.urlopen(pypi)
        else:
            raise

    info = json.load(response)
    for dist in info['urls']:
        yield dist['filename'], dist['url']


class CasePreservingConfigParser(ConfigParser):

    def optionxform(self, option):
        return option  # don't flatten case!


def write_index(package, version, dirname):

    print('Package %s==%s' % (package, version))
    dest_dir = os.path.join(dirname, package)
    if os.path.exists(dest_dir):
        print("Don't override package %s==%s" % (package, version))
        return

    os.makedirs(dest_dir)
    index_html = os.path.join(dest_dir, 'index.html')

    with open(index_html, 'w') as fp:
        fp.write('<html><body>')
        for filename, url in _pypi_release_dists(package, version):
            link = '<a href="%s">%s</a>' % (url, filename)
            fp.write(link + '<br/>')

        fp.write('</body></html>')
