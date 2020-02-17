# Overview
The aim of this project is to provide a quick way, for those who spend
more of their life glued to a desktop operating system rather then their
mobiles, of accessing their Monzo account details.

The Monzo CLI does this by making itself present in your machine's terminal,
addressable with the name `mzo`.

Each command can be invoked with the `--help` option which can be used to
explore all available commands/options.

```bash
$ mzo --help
Usage: mzo [options] COMMAND [ARGS]...

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  balance       View account's current balance.
  login         Authorization & session management.
  logout        Logout of authenticated session.
  pots          View and manage your pots.
  transactions  View account's current balance.
```

The installation, set-up process, and usage should be accessible enough
for both command-line veterans and toe-dippers alike.
[Let me know](https://github.com/jamesstidard/Mzo-Cli/issues) if you
have any problems and I'll update and clarify the documentation. Or make
a pull request.
