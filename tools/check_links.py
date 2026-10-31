#!/usr/bin/env python3
"""Check repository file links; optionally check external HTTP availability.

SPDX-License-Identifier: MIT
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path
import re
import urllib.error
import urllib.parse
import urllib.request


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in {'href', 'src'} and value:
                self.links.append(value)


def extract(path):
    text = path.read_text(encoding='utf-8')
    if path.suffix == '.md':
        text = re.sub(r'```.*?```', '', text, flags=re.S)
        inline = re.findall(r'\]\(([^\s)]+)(?:\s+"[^"]*")?\)', text)
        refs = re.findall(r'^\[[^\]]+\]:\s*(\S+)', text, flags=re.M)
        return inline + refs
    parser = Links()
    parser.feed(text)
    return parser.links


def check_external(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'JohnQuinn-Portfolio-LinkCheck/1.0'}, method='GET')
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            return url, 'ok', str(response.status)
    except urllib.error.HTTPError as error:
        if error.code in {404, 410}:
            return url, 'error', str(error.code)
        return url, 'warning', str(error.code)
    except (OSError, ValueError) as error:
        return url, 'warning', type(error).__name__


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--external', action='store_true')
    parser.add_argument('--portfolio-root', type=Path)
    args = parser.parse_args()
    root = Path.cwd().resolve()
    errors, warnings, urls, count = [], [], set(), 0
    paths = sorted(p for p in root.rglob('*') if p.suffix in {'.md', '.html'} and '.git' not in p.parts)
    for path in paths:
        for raw in extract(path):
            raw = raw.strip('<>')
            parts = urllib.parse.urlsplit(raw)
            if parts.scheme in {'mailto', 'data', 'tel'} or raw.startswith('#'):
                continue
            count += 1
            local = None
            if parts.scheme in {'https', 'http'}:
                if args.portfolio_root and parts.netloc == 'github.com':
                    match = re.fullmatch(r'/johnmquinnv/([^/]+)/(?:blob|tree)/main/(.+)', parts.path)
                    if match:
                        local = args.portfolio_root / match[1] / urllib.parse.unquote(match[2])
                if local is None:
                    urls.add(urllib.parse.urlunsplit(parts._replace(fragment='')))
                    continue
            elif parts.scheme:
                continue
            elif parts.netloc:
                urls.add('https:' + raw)
                continue
            else:
                local = (root if parts.path.startswith('/') else path.parent) / urllib.parse.unquote(parts.path.lstrip('/'))
            if not local.exists():
                errors.append(f'{path.relative_to(root)} -> {raw}')
    if args.external:
        with ThreadPoolExecutor(max_workers=8) as pool:
            for url, status, detail in pool.map(check_external, sorted(urls)):
                if status == 'error':
                    errors.append(f'{detail}: {url}')
                elif status == 'warning':
                    warnings.append(f'{detail}: {url}')
    for error in errors:
        print('ERROR', error)
    for warning in warnings:
        print('WARNING (manual review)', warning)
    print(f'{len(paths)} text files; {count} links; {len(urls)} external URLs; {len(errors)} errors; {len(warnings)} warnings')
    print('Checks confirm file existence and HTTP availability, not page meaning or clinical currency. Fragments are not validated.')
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
