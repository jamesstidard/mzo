# Install Options

## Homebrew
[Homebrew](https://brew.sh/) is the de-facto package manager on macOS.
If you are installing on macOS, this is the way to go.

```bash
# install
$ brew install mzo

# update
$ brew update mzo
```

## Snap
The Monzo CLI is also available on the [Snap](https://docs.snapcraft.io/)
package manager for those running Ubuntu and other Linux distros.

```bash
# install
$ snap install mzo

# update
$ snap refresh mzo
```

## Binaries
If you do not use a package manager (or at least the ones currently
supported), you can get the pre-compiled versions of each release on
the [projects GitHub releases page](https://github.com/jamesstidard/mzo-cli/releases).

Download the appropriate binary for your machine and place it somewhere
in your shell's `$PATH`.

::: warning
There is no self-update mechanism built into this application so new
versions will need to be manually downloaded to replace the existing
binary. A package manager is recommended because of this.
:::

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

# update
$ pipsi upgrade mzo
```

Though if you've opted to install through this method, you probably
already have a install process in mind.

## Source
If you'd like to get it directly from the source, it can be found
hosted on GitHub [here](https://github.com/jamesstidard/monzo-cli).

The documentation on how to build the environment should be on the
project's README.

```bash
$ git clone https://github.com/jamesstidard/monzo-cli.git
$ cat monzo-cli/README.md
```
