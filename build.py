"""Gera os arquivos que vão para a hospedagem."""
from datetime import datetime, timezone
import json
import shutil

from sitegen.config import CSS, DIST, JS, JSON_HASHES, PAGES, ROOT, SERVICES, SRC, BASE
from sitegen.output import support_files
from sitegen.pages import detail, home, legal_and_error

def main():
    PAGES.clear()
    JSON_HASHES.clear()
    (ROOT / 'reports').mkdir(exist_ok=True)
    DIST.mkdir(parents=True, exist_ok=True)
    (DIST / 'assets').mkdir(exist_ok=True)
    for file in (SRC / 'assets').iterdir():
        if file.is_file():
            shutil.copy2(file, DIST / 'assets' / file.name)
    shutil.copy2(SRC / 'site.css', DIST / CSS.lstrip('/'))
    shutil.copy2(SRC / 'site.js', DIST / JS.lstrip('/'))
    assert (DIST / 'assets/manrope-latin.woff2').is_file(), 'Prepare assets first'
    assert (DIST / 'assets/hugo-ferramentas-800.webp').is_file(), 'Prepare hero first'
    home()
    for service in SERVICES:
        detail(service)
    legal_and_error()
    support_files()
    report = {'generated_at': datetime.now(timezone.utc).isoformat(), 'domain': BASE, 'pages': PAGES, 'css': CSS, 'js': JS, 'public_files': len([p for p in DIST.rglob('*') if p.is_file()]), 'public_bytes': sum(p.stat().st_size for p in DIST.rglob('*') if p.is_file())}
    (ROOT / 'reports/build.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
