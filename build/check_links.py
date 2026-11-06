"""Checks every local link, image and anchor in both builds, plus the url() references in the stylesheet."""
import os
import re
import sys
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.ids.add(a['id'])
        for k in ('href', 'src', 'poster'):
            if a.get(k):
                self.refs.append((tag, k, a[k]))
        if a.get('srcset'):
            for part in a['srcset'].split(','):
                self.refs.append((tag, 'srcset', part.strip().split(' ')[0]))


IDS = {}


def ids_of(fp):
    if fp not in IDS:
        p = P()
        p.feed(open(fp, encoding='utf-8').read())
        IDS[fp] = p.ids
    return IDS[fp]


# Fragments handled by script rather than by an element id (blog topic filters)
SCRIPT_FRAGMENTS = {'installation', 'compliance', 'renewables', 'lighting'}


def check(root, mode):
    bad = []
    pages = 0
    refs = 0
    for dp, _, fs in os.walk(root):
        for f in fs:
            if not f.endswith('.html'):
                continue
            pages += 1
            path = os.path.join(dp, f)
            p = P()
            p.feed(open(path, encoding='utf-8').read())
            IDS[path] = p.ids
            for tag, k, v in p.refs:
                if v.startswith(('http://', 'https://', 'tel:', 'mailto:', 'data:')):
                    continue
                if v.startswith('#'):
                    if v[1:] and v[1:] not in p.ids:
                        bad.append((os.path.relpath(path, root), v, 'no such anchor on page'))
                    continue
                refs += 1
                u = urlsplit(v)
                target = unquote(u.path)
                if mode == 'site':
                    if not target.startswith('/'):
                        bad.append((path, v, 'not root relative'))
                        continue
                    fp = os.path.join(root, target.lstrip('/'))
                else:
                    if target.startswith('/'):
                        bad.append((path, v, 'root relative in preview'))
                        continue
                    fp = os.path.normpath(os.path.join(dp, target))
                if fp.endswith('/') or os.path.isdir(fp):
                    fp = os.path.join(fp, 'index.html')
                if not os.path.exists(fp):
                    bad.append((os.path.relpath(path, root), v, 'missing'))
                elif u.fragment and fp.endswith('.html') and u.fragment not in SCRIPT_FRAGMENTS \
                        and u.fragment not in ids_of(fp):
                    bad.append((os.path.relpath(path, root), v, 'no such anchor'))
    css = open(os.path.join(root, 'assets/site.css')).read()
    for u in [x for x in re.findall(r'url\("([^"]+)"\)', css) if not x.startswith('data:')]:
        if not os.path.exists(os.path.join(root, 'assets', u)):
            bad.append(('site.css', u, 'missing'))
    print(mode, 'pages', pages, 'local refs', refs, 'problems', len(bad))
    for b in bad[:30]:
        print('  ', b)
    return not bad


ok1 = check('dist/site', 'site')
ok2 = check('dist/preview', 'preview')
sys.exit(0 if ok1 and ok2 else 1)
