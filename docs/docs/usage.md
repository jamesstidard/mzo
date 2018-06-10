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
on invoking `eval $(monzo login)` for the first time.

Later releases will remove this extra step, simplifying the initial login
process.
:::

You should be able to call the command below to start the process and follow
the instructions provided in the prompt:

```bash
$ eval $(monzo login)
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
If you call a command (such as displaying your balance with `monzo balance`)
you will be prompted for your password. You can simply provide the password
and the command will complete.

Authenticating commands in this one-off style will be most convenient when
you just want to open the terminal and perform a single action on your account.

```bash
$ monzo balance
No login session currently active.
  You can authorize this one-off command
  by providing your password, or see
  `monzo login --help` for persisting
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
The will be times when you want to perform a number of commands without needing
to provide your password for each command. For this the Monzo CLI provides login
sessions.

```bash
# start login session providing your password
$ eval $(monzo login)
Password:
Login Session Active

# invoke x number of commands
$ monzo balance
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
$ eval $(monzo logout)
Login Session Ended
```

::: tip What's with the eval?
Sessions are managed by temporarily storing the a access token in your terminal
session's environment variables. you can see this if you issue the `env` command
during a login session.

A command-line application can not set a environment variable directly in the
shell session which invoked it. Instead, both `monzo login` and `monzo logout`
both return commands for (un)setting the access token which can be automatically
executed by the parent shell by wrapping it in its `eval` function.

You'll be able to see this by calling these commands without the eval function:

```bash
$ monzo login
Password:
Login Session Active
export MONZO_ACCESS_TOKEN="xxxxxx.xxxxxxxxxxxxxxxxxxx.xxxxxxx"
# This command is meant to be used with your shell's eval function.
# Run 'eval $(monzo login)' to sign into your Monzo account.
```
:::

## Balance
The balance command returns the current balance of your current account along
with the balance of all of your pots.

```bash
$ monzo balance
+--------------------+---------+
| Name               | Balance |
+--------------------+---------+
| 💸 Current Account | 1337.00 |
| 🎾 Disposable      |    0.00 |
|                    |         |
| 💰 Total           | 1337.00 |
+--------------------+---------+
```

The balance command also supports different output formats like `csv` and `json`.

```bash
$ monzo balance --format csv
name,balance
Current Account,1337.0
Disposable,0.0
Total,1337.0

$ monzo balance --format json
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
$ monzo balance --format csv > ~/Desktop/balance.csv

$ monzo balance --format json | jq '.[] | select(.name == "Total") | .balance'
1337.0
```

For full documentation check out `monzo balance --help`.

## Transactions
...

## Pots
...
