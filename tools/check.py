"""Gera o site e roda as verificações locais."""
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    node = shutil.which('node')
    if not node:
        raise SystemExit('Instale o Node.js e deixe o comando node disponível no terminal.')

    commands = [
        [sys.executable, 'build.py'],
        [sys.executable, 'tools/verify.py'],
        [node, 'tools/verify_contact.cjs'],
        [node, 'tools/verify_menu.cjs'],
    ]
    for command in commands:
        subprocess.run(command, cwd=ROOT, check=True)


if __name__ == '__main__':
    main()
