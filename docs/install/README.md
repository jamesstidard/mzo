# Install

## Homebrew
[Homebrew](https://brew.sh/) is the defacto package manager on macOS.
If you are installing on a macOS, this is the way to go.

```bash
$ brew install monzo-cli
```

## Snap
The Monzo CLI is also available on the [Snap](https://docs.snapcraft.io/)
package manager for those running Ubuntu and other Linux distros.

```bash
$ snap install monzo-cli
```

## PyPI
::: warning
For those familier with Python package management.
:::
Monzo CLI is a Python application and is hosted on PyPI so can be
installed as a Python package.

I'd personally recommend using [pipsi](https://github.com/mitsuhiko/pipsi)
for installing global Python packages as it manages creating specific
Python virtual enviroments for each package - preventing any dependancy
conflicts with other installed python packages.

```bash
$ pipsi install monzo-cli --python 3.6.7
```

Though if you've opted to install through this method, you probably
already have a install process in mind.
