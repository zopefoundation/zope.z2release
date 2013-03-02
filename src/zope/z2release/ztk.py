import os
import sys
import urllib


def main():
    if len(sys.argv) != 3:
        print('Usage: ztk_kgs <tag-name> <destination-dirname>')
        print('Example: ztk_kgs tags/1.1.2 '
            '/var/www/download.zope.org/zopetoolkit/index/1.1.2/')
        sys.exit(1)

    tag = sys.argv[1]
    dirname = sys.argv[2]
    if not os.path.exists(dirname):
        print >>sys.stderr, 'Creating index directory: %s' % dirname
        os.makedirs(dirname)

    versions_url = 'http://svn.zope.org/*checkout*/zopetoolkit/' + \
                   '%s/ztk-versions.cfg' % tag
    print >>sys.stderr, 'Fetching %s' % versions_url
    data = urllib.urlopen(versions_url).read()
    version_file = os.path.join(dirname, 'ztk-versions.cfg')
    with open(version_file, 'w') as fd:
        fd.write(data)

    app_versions_url = 'http://svn.zope.org/*checkout*/zopetoolkit/' + \
                       '%s/zopeapp-versions.cfg' % tag
    print >>sys.stderr, 'Fetching %s' % app_versions_url
    data = urllib.urlopen(app_versions_url).read()
    app_version_file = os.path.join(dirname, 'zopeapp-versions.cfg')
    with open(app_version_file, 'w') as fd:
        fd.write(data)


if __name__ == '__main__':
    main()
