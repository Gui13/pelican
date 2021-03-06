#! /usr/bin/env python

from BeautifulSoup import BeautifulStoneSoup
from codecs import open
import os
import argparse

def wp2html(xml):
    xmlfile = open(xml, encoding='utf-8').read()
    soup = BeautifulStoneSoup(xmlfile)
    items = soup.rss.channel.findAll('item')

    for item in items:
        if item.fetch('wp:status')[0].contents[0] == "publish":
            title = item.title.contents[0]
            content = item.fetch('content:encoded')[0].contents[0]
            filename = item.fetch('wp:post_name')[0].contents[0]
            yield (title, content, filename)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""Transform a wordpress xml export into rst files """)

    parser.add_argument(dest='xml', help='The xml filepath')
    parser.add_argument('-o', '--output', dest='output', default='output', help='Output path')
    args = parser.parse_args() 

    for title, content, filename in wp2html(args.xml): 
        html_filename = os.path.join(args.output, filename+'.html')
        rst_filename = os.path.join(args.output, filename+'.rst')

        with open(html_filename, 'w', encoding='utf-8') as fp:
            fp.write(content)
        os.system('pandoc --from=html --to=rst -o %s %s' % (rst_filename,
            html_filename))
