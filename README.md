# Monzo Cli
A command line interface to your monzo account.

The full monzo API isn't availible yet but the plan is to let easy
payments via the command line.

- Same auth as 1Password cli
- XOR store refresh token

### Command Examples
```sh
# mzo pay <name>... <amount> [--daily|--weekly|--monthly|--yearly|--every <x> (days|weeks|months|years) [--from (monday|tuesday|wednesday|thursday|friday|saturday|sunday)] [--sort-code <code> --account-number <number>]] [--message <message>]

$ mzo pay john 50.40

$ mzo pay patrick selman 30

$ mzo pay james 5 --weekly --from tomorrow

$ mzo pay vlad 2 --every 4 days --from friday

$ mzo pay dash 5 --sort-code 40-01-03 --account-number 123456789 --message "give it back"
```
