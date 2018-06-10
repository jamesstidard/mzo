---
home: true
title: Monzo CLI
lang: en-US
meta:
  - name: description
    content: A command line interface between you and your Monzo account.
  - name: keywords
    content: Monzo Command Line Interface CLI
actionText: Install Options →
actionLink: /install
features:
- title: Human First
  details: The application should be easy to install and setup. While the commands and outputs should to be intuative and even pretty at times.
- title: Secure
  details: Your credentials are encrypted and stored locally on your machine with the password of your choosing. While no data is sent to any parties other then your machine and Monzo.
- title: Convenient
  details: Login sessions allow all encompased commands to be authenticated, or commands can be indavidually authenticated with a password on execution outside a login session.
footer: Everything Looks Better with a Footer
---

::: warning Disclosure
This is not an offical command-line application from Monzo, but a
third-party, open-source one implemented using Monzo's developer API.
:::

# Example Usage
```bash
$ eval (monzo login)
Password:

$ monzo balance
+--------------------+---------+
| Name               | Balance |
+--------------------+---------+
| 💸 Current Account | 1337.00 |
| 🎾 Disposable      |    0.00 |
|                    |         |
| 💰 Total           | 1337.00 |
+--------------------+---------+

$ monzo pots deposit 50 --into disposable
+--------------------+---------+---------+
| Name               | Current |   Final |
+--------------------+---------+---------+
| 💸 Current Account | 1337.00 | 1287.00 |
| 🎾 Disposable      |    0.00 |   50.00 |
+--------------------+---------+---------+

Confirm this transfer [y/N]: y
Transfer Successful

$ eval (monzo logout)
```