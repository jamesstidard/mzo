# Install Options

## Homebrew
[Homebrew](https://brew.sh/) is the de-facto package manager on macOS.
If you are installing on macOS, this is the way to go.

```bash
$ brew tap jamesstidard/mzo
$ brew install mzo
```

## Snap
The Monzo CLI can also be grabbe from [Snap](https://snapcraft.io/), for
those using Linux distros (such as Ubuntu).

```bash
$ sudo snap install --edge mzo --devmod
```

## PyPI
::: warning
For those familiar with Python package management.
:::
Monzo CLI is a Python application and is hosted on PyPI so can be
installed as a Python package.

I'd personally recommend using [pipsi](https://github.com/mitsuhiko/pipsi)
for installing global Python packages as it manages creating specific
Python virtual environments for each package - preventing any dependency
conflicts with other installed python packages.

```bash
# install
$ pipsi install mzo --python path/to/python3.6
```

Though if you've opted to install through this method, you probably
already have a install process in mind.

## Source
If you'd like to get it directly from the source, it can be found
hosted on GitHub [here](https://github.com/jamesstidard/mzo-cli).

The documentation on how to build the environment should be on the
project's README.

```bash
$ git clone https://github.com/jamesstidard/mzo-cli.git
$ cat mzo-cli/README.md
```
