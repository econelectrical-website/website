"""House style check on the built site: no hyphens or dashes in visible text, and no "free quote" wording."""
import os
import re
import sys
from html.parser import HTMLParser

SKIP = {'script', 'style', 'svg', 'code', 'pre'}


class T(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.text = []
        self.attrs_text = []

    def handle_starttag(self, tag, attrs):
        if tag not in ('br', 'img', 'input', 'meta', 'link', 'source', 'hr'):
            self.stack.append(tag)
        for k, v in attrs:
            if k in ('alt', 'title', 'aria-label', 'placeholder') and v:
                self.attrs_text.append(v)
            if k == 'content' and v and dict(attrs).get('name') == 'description':
                self.attrs_text.append(v)

    def handle_endtag(self, tag):
        while self.stack:
            if self.stack.pop() == tag:
                break

    def handle_data(self, data):
        if not any(t in SKIP for t in self.stack):
            self.text.append(data)


DASH = re.compile(r'(?<=\w)-(?=\w)|[‐-―−]|\s-\s')
QUOTE = re.compile(r'free,? (no obligation )?quot|get a quote|request a quote', re.I)

problems = []
for dp, _, fs in os.walk('dist/site'):
    for f in fs:
        if not f.endswith('.html'):
            continue
        path = os.path.join(dp, f)
        t = T()
        t.feed(open(path, encoding='utf-8').read())
        for chunk in t.text + t.attrs_text:
            for m in DASH.finditer(chunk):
                ctx = chunk[max(0, m.start() - 30):m.end() + 30].replace('\n', ' ')
                if re.search(r'https?://|@|\.co\.uk', ctx):
                    continue
                problems.append((os.path.relpath(path, 'dist/site'), 'dash', ctx))
            for m in QUOTE.finditer(chunk):
                problems.append((os.path.relpath(path, 'dist/site'), 'quote wording', chunk[max(0, m.start() - 30):m.end() + 30]))

print('text problems', len(problems))
for p in problems[:60]:
    print('  ', p)
sys.exit(1 if problems else 0)
