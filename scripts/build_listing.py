"""Aggregate published VPM release assets into a repository listing."""

import hashlib
import io
import json
import os
from pathlib import Path
import re
from urllib.request import Request, urlopen
import zipfile


ROOT = Path(__file__).resolve().parents[1]


def fetch(url, api=False):
    headers = {'User-Agent': 'T_Y_Tools-listing'}
    if api and os.environ.get('GITHUB_TOKEN'):
        headers['Authorization'] = 'Bearer ' + os.environ['GITHUB_TOKEN']
    with urlopen(Request(url, headers=headers), timeout=60) as response:
        return response.read()


def main():
    config = json.loads((ROOT / 'repository.json').read_text(encoding='utf-8'))
    listing = {key: config[key] for key in ('name', 'id', 'url', 'author')}
    listing['packages'] = {}
    for repository in config['repositories']:
        page = 1
        while True:
            releases = json.loads(fetch(f'https://api.github.com/repos/{repository}/releases?per_page=100&page={page}', api=True))
            for release in releases:
                if release['draft']:
                    continue
                assets = {asset['name']: asset for asset in release['assets']}
                if 'package.json' not in assets:
                    continue
                manifest = json.loads(fetch(assets['package.json']['browser_download_url']))
                url = manifest.get('url', '')
                if not url:
                    continue
                if not any(asset['browser_download_url'] == url for asset in assets.values()):
                    raise ValueError(f'ZIP URL is not an asset of release {release["tag_name"]}')
                name, version = manifest['name'], manifest['version']
                if not re.fullmatch(r'[a-z0-9]+(?:[.\-][a-z0-9]+)+', name):
                    raise ValueError(f'Invalid package name: {name}')
                if release['tag_name'] != f'v{version}':
                    raise ValueError(f'Version/tag mismatch: {name} {version}')
                data = fetch(url)
                with zipfile.ZipFile(io.BytesIO(data)) as archive:
                    if any(p.startswith(('/', '\\')) or '..' in p.replace('\\', '/').split('/') for p in archive.namelist()):
                        raise ValueError('Unsafe ZIP path')
                    if json.loads(archive.read('package.json')) != manifest:
                        raise ValueError(f'ZIP manifest mismatch: {name} {version}')
                versions = listing['packages'].setdefault(name, {'versions': {}})['versions']
                if version in versions:
                    raise ValueError(f'Duplicate package version: {name} {version}')
                versions[version] = {**manifest, 'zipSHA256': hashlib.sha256(data).hexdigest()}
            if len(releases) < 100:
                break
            page += 1
    output = ROOT / 'public'
    output.mkdir(exist_ok=True)
    (output / 'index.json').write_text(json.dumps(listing, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    count = sum(len(p['versions']) for p in listing['packages'].values())
    print(f'{len(listing["packages"])} packages, {count} versions')


if __name__ == '__main__':
    main()
