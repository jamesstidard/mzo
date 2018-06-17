import os
import hashlib

from tempfile import TemporaryDirectory
from contextlib import contextmanager


@contextmanager
def change_dir(dir_):
    cwd = os.getcwd()
    os.chdir(dir_)
    yield
    os.chdir(cwd)


SNAPCRAFT_TMPL = """\
name: mzo
version: '{version:}'
summary: A command-line interface to your monzo account.
description: |
  This is a third-party, command-line tool which allows
  control over your Monzo bank account. Allows you to
  you balance, move money between pots, view transaction
  history, etc.

grade: devel # must be 'stable' to release into candidate/stable channels
confinement: devmode # use 'strict' once you have the right plugs and slots

apps:
  mzo:
    command: /usr/local/bin/mzo
    plugs: [network, network-bind]

parts:
  python36:
    plugin: nil
    stage-packages:
      - make
      - zlib1g-dev
      - openssl
      - libssl-dev
    source: https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tar.xz
    source-checksum: md5/9f49654a4d6f733ff3284ab9d227e9fd
    override-build: |
      ./configure --enable-optimizations
      make
      make install
  mzo:
    after: [python36]
    plugin: nil
    source: https://github.com/jamesstidard/Mzo-Cli/archive/v{version:}.tar.gz
    source-checksum: sha256/{sha256:}
    override-build: |
      /usr/local/bin/python3 -m pip install --upgrade pip wheel setuptools pipenv
      pipenv lock --requirements > requirements.txt
      /usr/local/bin/python3 -m pip install -r requirements.txt
"""

here = os.path.abspath(os.path.dirname(__file__))
about = {}

with open(os.path.join(here, '..', 'mzo', '__version__.py')) as f:
    exec(f.read(), about)

version = about['__version__']


with TemporaryDirectory() as td:
    # Download current release source from git tag
    tar_release_url = f'https://github.com/jamesstidard/Mzo-Cli/archive/v{version}.tar.gz'
    tar_release_path = os.path.join(td, 'release.tar.gz')
    os.system(f'curl --location "{tar_release_url}" --output {tar_release_path}')

    with open(tar_release_path, 'rb') as fp:
        tar_release_sha256 = hashlib.sha256(fp.read()).hexdigest()

    os.system(f'git clone git@github.com:jamesstidard/mzo-cli')
    with change_dir('mzo-cli'):
        snap = SNAPCRAFT_TMPL.format(
            version=version,
            sha256=tar_release_sha256)

        with open('snapcraft.yaml', 'w') as fp:
            fp.write(snap)

        os.system('git add .')
        os.system(f'git commit -m "snap v{version}"')
        os.system('git push origin master')
