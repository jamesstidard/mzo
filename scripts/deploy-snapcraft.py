import os
import hashlib
import subprocess

from tempfile import TemporaryDirectory
from contextlib import contextmanager


@contextmanager
def change_dir(dir_):
    cwd = os.getcwd()
    os.chdir(dir_)
    yield
    os.chdir(cwd)


here = os.path.abspath(os.path.dirname(__file__))
about = {}

with open(os.path.join(here, "snapcraft.yaml.tmpl")) as f:
    SNAPCRAFT_TMPL = f.read()

with open(os.path.join(here, "..", "mzo", "__version__.py")) as f:
    exec(f.read(), about)

version = about["__version__"]


with TemporaryDirectory() as td:
    # Download current release source from git tag
    tar_release_url = (
        f"https://github.com/jamesstidard/Mzo-Cli/archive/v{version}.tar.gz"
    )
    tar_release_path = os.path.join(td, "release.tar.gz")
    os.system(f'curl --location "{tar_release_url}" --output {tar_release_path}')

    with open(tar_release_path, "rb") as fp:
        tar_release_sha256 = hashlib.sha256(fp.read()).hexdigest()

    with change_dir(td):
        os.system(f"git clone git@github.com:jamesstidard/mzo-cli")

        with change_dir(os.path.join(td, "mzo-cli")):
            requirements = subprocess.check_output(
                "pipenv lock --requirements", shell=True
            )
            requirements = [
                r.split(";")[0].strip()
                for r in requirements.decode("utf8").split("\n")
                if r and not r.startswith("-")
            ]

            snap = SNAPCRAFT_TMPL.format(
                version=version,
                sha256=tar_release_sha256,
                requirements="\n      - ".join(requirements),
            )

            with open("snapcraft.yaml", "w") as fp:
                fp.write(snap)

            os.system("git add .")
            os.system(f'git commit -m "snap v{version}"')
            os.system("git push origin master")
