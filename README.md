# Monzo Cli
A (third-party) command line interface to your monzo account.

_Sometimes_ the command line is more convient then swiping and tapping.

The full monzo API isn't availible yet but the plan is to let easy
payments via the command line.

### Features
- Human-first interface
- Secure credential management
- One-time and session-based login

### Command Examples
```fish
# monzo pay <name>... <amount> [--daily|--weekly|--monthly|--yearly|--every <x> (days|weeks|months|years) [--from (monday|tuesday|wednesday|thursday|friday|saturday|sunday)] [--sort-code <code> --account-number <number>]] [--message <message>]

$ monzo pay john 50.40

$ monzo pay patrick selman 30

$ monzo pay james 5 --weekly --from tomorrow

$ monzo pay vlad 2 --every 4 days --from friday

$ monzo pay dash 5 --sort-code 40-01-03 --account-number 123456789 --message "give it back"
```


### Credentials File
OAuth credentials are saved to `~/.monzo/credentials` and are encrypted
with the user provided key.

### Config File
A user editable config file at `~/.monzo/config`.
```toml
[default]
account_id = "xxxxxxxxxxx"
output_format = "<user|json|csv>"
```
