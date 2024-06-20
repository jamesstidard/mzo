import os
import re
import time
import tarfile
import hashlib
import subprocess
import urllib.request
import urllib.error
from datetime import datetime

from tempfile import TemporaryDirectory
from contextlib import contextmanager


TAP_TEMPLATE = """
class Mzo < Formula
  include Language::Python::Virtualenv

  desc "A command-line interface between you and your Monzo account."
  homepage "https://mzo.stidard.com"
  url "{url:}"
  sha256 "{sha256:}"

  depends_on "python"

{resources:}

  def install
    virtualenv_install_with_resources
  end

end
"""


@contextmanager
def change_dir(dir_):
    cwd = os.getcwd()
    os.chdir(dir_)
    yield
    os.chdir(cwd)


@contextmanager
def env(dict_):
    current_env = os.environ.copy()
    os.environ.update(dict_)
    yield
    os.environ = current_env


here = os.path.abspath(os.path.dirname(__file__))
about = {}

with open(os.path.join(here, "..", "mzo", "__version__.py")) as f:
    exec(f.read(), about)

mzo_version = about["__version__"]

with TemporaryDirectory() as td:
    # Download current release source from git tag
    tar_release_url = (
        f"https://github.com/jamesstidard/Mzo-Cli/archive/v{mzo_version}.tar.gz"
    )
    tar_release_path = os.path.join(td, "release.tar.gz")
    os.system(f'curl --location "{tar_release_url}" --output {tar_release_path}')

    with open(tar_release_path, "rb") as fp:
        tar_release_sha256 = hashlib.sha256(fp.read()).hexdigest()

    # Extract to td
    with tarfile.open(tar_release_path, "r:gz") as tar:
        source_path = os.path.join(td, os.path.commonprefix(tar.getnames()))
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(tar, path=td)

    # Init dependencies with pipenv
    with change_dir(source_path):
        # Ignore development pipenv environment and make a new one for release
        with env(
            {
                "PIPENV_IGNORE_VIRTUALENVS": "1",
                "PIPENV_VENV_IN_PROJECT": "1",
                "LANG": "en_US.utf8",
            }
        ):
            os.system("pipenv install --dev")

            # wait for mzo to be available on pypi
            pypi_url = f"https://pypi.org/project/mzo/{mzo_version}/"
            print(f"Waiting for release to be visible on PyPI... {pypi_url}")

            while True:
                try:
                    urllib.request.urlopen(pypi_url)
                except urllib.error.HTTPError:
                    time.sleep(5)
                else:
                    print(f"Found PyPi release")
                    break

            resources = subprocess.check_output(
                "pipenv run poet mzo", shell=True
            ).decode("ascii")
            # remove mzo so homebrew detects mzo as a new binary
            resources = re.sub(
                ' {2}resource "mzo".+?end', "", resources, flags=re.DOTALL
            )

    # Update Homebrew tap repo
    homebrew_repo = os.path.join(td, "homebrew-formulas")
    os.system(
        f'git clone git@github.com:jamesstidard/homebrew-formulas "{homebrew_repo}"'
    )
    with change_dir(homebrew_repo):
        tap = TAP_TEMPLATE.format(
            url=tar_release_url, sha256=tar_release_sha256, resources=resources
        )

        with open("mzo.rb", "w") as fp:
            fp.write(tap)

        now = datetime.utcnow()
        start = datetime(now.year, now.month, now.day)
        delta = (now - start).total_seconds()
        repo_version = f"v{now:%Y.%m.%d}.{delta:.0f}"

        os.system("git add .")
        os.system(f'git commit -m "mzo v{mzo_version}"')
        os.system("git push origin master")
        os.system(f"git tag {repo_version}")
        os.system(f"git push origin {repo_version}")

print("Homebrew tap updated")
