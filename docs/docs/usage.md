# Usage

## Initial Authorization
Once you have installed the CLI, the first things you'll need to do is
authorize the application to have access to your Monzo account. Monzo
handles this using OAuth 2. You are probably familiar with this type of
authorization flow from websites that allow you to sign in using your
existing Facebook, Google, etc. accounts.

This CLI uses that same flow to authorize itself to access your Monzo account
the first time you try and login.

::: warning
Due to the current limitations imposed on the Monzo Developer API,
there is an additional step that is required the first time you want to use
the Monzo CLI.

There is currently a limit on how many user's a single developer can have
using their applications. So to work around this, during the development of
this application, there is an extra step where you'll need to register as
a developer yourself. You can then become your own user.

You will be additionally guided through this step from the command-line
on invoking `eval $(mzo login)` for the first time.

Later releases will remove this extra step, simplifying the initial login
process.
:::

You should be able to call the command below to start the process and follow
the instructions provided in the prompt:

```bash
$ eval $(mzo login)
```

At the end of this process you will have both authorized the application to
have access to your Monzo account as well as started your first
[login session](/docs/usage.html#Sessions).

## Logins
All commands through the CLI require your password in order to be executed -
you would have provided this during the initial authorization step of the
application. If you have not completed this step see [Initial Authorization](/docs/usage.html#Initial-Authorization)
before continuing.

### One-off
If you call a command (such as displaying your balance with `mzo balance`)
you will be prompted for your password. You can simply provide the password
and the command will complete.

Authenticating commands in this one-off style will be most convenient when
you just want to open the terminal and perform a single action on your account.

```bash
$ mzo balance
No login session currently active.
  You can authorize this one-off command
  by providing your password, or see
  `mzo login --help` for persisting
  authentication between commands.

Password:
+--------------------+---------+
| Name               | Balance |
+--------------------+---------+
| 💸 Current Account | 1337.00 |
| 🎾 Disposable      |    0.00 |
|                    |         |
| 💰 Total           | 1337.00 |
+--------------------+---------+
```

### Sessions
There will be times when you want to perform a number of commands without needing
to provide your password for each command. For this the Monzo CLI provides login
sessions.

```bash
# start login session providing your password
$ eval $(mzo login)
Password:
Login Session Active

# invoke x number of commands
$ mzo balance
+--------------------+---------+
| Name               | Balance |
+--------------------+---------+
| 💸 Current Account | 1337.00 |
| 🎾 Disposable      |    0.00 |
|                    |         |
| 💰 Total           | 1337.00 |
+--------------------+---------+

# Log back out of the session.
# Requiring commands to either use one-off authentication
# or a new login session to be started.
# Sessions can also be ended by closing the
# terminal window.
$ eval $(mzo logout)
Login Session Ended
```

::: tip What's with the eval?
Sessions are managed by temporarily storing a decrypted access token in
your terminal session's environment variables. you can see this if you
issue the `env` command during a login session.

A command-line application can not set a environment variable directly in the
shell session which invoked it. Instead, both `mzo login` and `mzo logout`
both return commands for (un)setting the access token which can be automatically
executed by the parent shell by wrapping it in its `eval` function.

You'll be able to see this by calling these commands without the eval function:

```bash
$ mzo login
Password:
Login Session Active
export MZO_ACCESS_TOKEN="xxxxxx.xxxxxxxxxxxxxxxxxxx.xxxxxxx"
# This command is meant to be used with your shell's eval function.
# Run 'eval $(mzo login)' to sign into your Monzo account.
```

If your shell doesn't support that syntax (`bash` and `fish` do that I
know of), you can use the `--format raw` option to handle setting the
`MZO_ACCESS_TOKEN` environment variable yourself. If you are not sure
which shell you are running, it is probably bash.
:::

## Balance
The balance command returns the current balance of your current account along
with the balance of all of your pots.

```bash
$ mzo balance
+--------------------+---------+
| Name               | Balance |
+--------------------+---------+
| 💸 Current Account | 1337.00 |
| 🎾 Disposable      |    0.00 |
|                    |         |
| 💰 Total           | 1337.00 |
+--------------------+---------+
```

For full documentation check out `mzo balance --help`.

## Transactions
::: warning
Work in progress. Available by setting `MZO_PRERELEASE=1` in terminal session's
environment variables.
:::

List historic transactions.

```bash
$ mzo transactions
+------------------+----------------------------------+----------+---------------+
| Created          | Name                             | Amount   | Category      |
+------------------+----------------------------------+----------+---------------+
| ...              | ...                              | ...      | ...           |
| Sun 16 February  | You Wish                         | +100.00  | General       |
| Sun 16 February  | Amazon                           | 12.99    | Shopping      |
| Mon 17 February  | Sainsbury's                      | 24.61    | Groceries     |
+------------------+----------------------------------+----------+---------------+
```

For full documentation check out `mzo transactions --help`.

## Pots
::: warning
Work in progress. Available by setting `MZO_PRERELEASE=1` in terminal session's
environment variables.
:::

Transfer money between pots and your current account. You can directly transfer from
one pot to another, and `mzo` will make to transfers `Pot 1 -> Current Account -> Pot 2`.

If only a `--from` or `--into` account is provided, the destination or source, 
respectively, is assumed to be your current account.

The pot names provided are also fuzzy matched, so don't worry about getting exactly the
right name for the pot. If you have a pot called "Bike Fund", for example, try
something like `mzo pots move 100 --into bike`.

```bash
$ mzo pots move 50 --into disposable
+--------------------+---------+---------+
| Name               | Current |   Final |
+--------------------+---------+---------+
| 💸 Current Account | 1337.00 | 1287.00 |
| 🎾 Disposable      |    0.00 |   50.00 |
+--------------------+---------+---------+

Confirm this transfer [y/N]: y
Transfer Successful
```

For full documentation check out `mzo pots move --help`.

## Formats
Most commands support different output formats like `human`, `csv`, and `json`.

Here's a example with the balance command:

```bash
$ mzo balance --format csv
name,balance
Current Account,1337.0
Disposable,0.0
Total,1337.0

$ mzo balance --format json
[
  {
    "name": "Current Account",
    "balance": 1337.0
  },
  {
    "name": "Disposable",
    "balance": 0.0
  },
  {
    "name": "Total",
    "balance": 1337.0
  }
]
```

You can use this to create spreadsheets or to pipe into other applications like
[jq](https://stedolan.github.io/jq/).

```bash
$ mzo balance --format csv > ~/Desktop/balance.csv

$ mzo balance --format json | jq '.[] | select(.name == "Total") | .balance'
1337.0
```

By default the formats for commands is set to `human`. You can change this by
editing the `~/.mzo/config` file and setting the default format to either
`human`, `csv` or `json`.

```toml
[default]
account_id = "acc_xxxxx"
format = "human"

[oauth]
client_id = "oauth2client_xxxxx"
client_secret = "xxxxxxxxxxxxxx"
```

Check out the documentation for each command with `--help` for full documentation.
