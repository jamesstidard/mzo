# mzo
A (third-party) command-line interface to your monzo account. 
Because _Sometimes_ the command-line is more convient then 
swiping and tapping.

This README covers the enviroment setup if you are looking to
run the applications source code / work on the project. If you
are looking for the documentation and more straight forward
installation instructions [see the docs](https://jamesstidard.github.io/Mzo-Cli/).

## Prerequisites
At the time of writing this the project is using Python 3.6.5.
You will need that version of python installed before starting.
If you don't currently have a method of managing multiple Python
versions on your machine, I would recommend checking out [pyenv](https://github.com/pyenv/pyenv).

The projects dependancies are also managed by [pipenv](https://docs.pipenv.org/).
You should head over there and make sure that you also have that
tool setup.

Finally I've used a `package.json` in my Python project (herasy
I'm sure), which aggrigates all ansilary project scripts together
for building and deploying. Specifically I'm using the [yarn](https://yarnpkg.com/lang/en/)
package manager for these npm dependancies.

## Summoning Ritual
Once you've completed the prerequisets above you should be able
to bring the application to life with the following commands.

```bash
# clone the source code to your machine
$ git clone https://github.com/jamesstidard/mzo-cli

$ cd mzo-cli/

$ pipenv install --dev --python 3.6.5
$ pipenv shell
```

### Run
```bash
$ mzo --help
```

### Test
```bash
$ yarn test
```

### Document
```bash
$ yarn docs:dev
```

### Deploy mzo
```bash
$ yarn mzo:deploy
```

### Deploy Docs
```bash
$ yarn docs:deploy
```