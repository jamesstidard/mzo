<template><div><h1 id="usage" tabindex="-1"><a class="header-anchor" href="#usage" aria-hidden="true">#</a> Usage</h1>
<h2 id="initial-authorization" tabindex="-1"><a class="header-anchor" href="#initial-authorization" aria-hidden="true">#</a> Initial Authorization</h2>
<p>Once you have installed the CLI, the first things you'll need to do is
authorize the application to have access to your Monzo account. Monzo
handles this using OAuth 2. You are probably familiar with this type of
authorization flow from websites that allow you to sign in using your
existing Facebook, Google, etc. accounts.</p>
<p>This CLI uses that same flow to authorize itself to access your Monzo account
the first time you try and login.</p>
<div class="custom-container warning"><p class="custom-container-title">WARNING</p>
<p>Due to the current limitations imposed on the Monzo Developer API,
there is an additional step that is required the first time you want to use
the Monzo CLI.</p>
<p>There is currently a limit on how many user's a single developer can have
using their applications. So to work around this, during the development of
this application, there is an extra step where you'll need to register as
a developer yourself. You can then become your own user.</p>
<p>You will be additionally guided through this step from the command-line
on invoking <code v-pre>eval $(mzo login)</code> for the first time.</p>
<p>Later releases will remove this extra step, simplifying the initial login
process.</p>
</div>
<p>You should be able to call the command below to start the process and follow
the instructions provided in the prompt:</p>
<div class="language-bash line-numbers-mode" data-ext="sh"><pre v-pre class="language-bash"><code>$ <span class="token builtin class-name">eval</span> <span class="token variable"><span class="token variable">$(</span>mzo login<span class="token variable">)</span></span>
</code></pre><div class="line-numbers" aria-hidden="true"><div class="line-number"></div></div></div><p>At the end of this process you will have both authorized the application to
have access to your Monzo account as well as started your first
<RouterLink to="/docs/usage.html#Sessions">login session</RouterLink>.</p>
<h2 id="logins" tabindex="-1"><a class="header-anchor" href="#logins" aria-hidden="true">#</a> Logins</h2>
<p>All commands through the CLI require your password in order to be executed -
you would have provided this during the initial authorization step of the
application. If you have not completed this step see <RouterLink to="/docs/usage.html#Initial-Authorization">Initial Authorization</RouterLink>
before continuing.</p>
<h3 id="one-off" tabindex="-1"><a class="header-anchor" href="#one-off" aria-hidden="true">#</a> One-off</h3>
<p>If you call a command (such as displaying your balance with <code v-pre>mzo balance</code>)
you will be prompted for your password. You can simply provide the password
and the command will complete.</p>
<p>Authenticating commands in this one-off style will be most convenient when
you just want to open the terminal and perform a single action on your account.</p>
<div class="language-bash line-numbers-mode" data-ext="sh"><pre v-pre class="language-bash"><code>$ mzo balance
No login session currently active.
  You can authorize this one-off <span class="token builtin class-name">command</span>
  by providing your password, or see
  <span class="token variable"><span class="token variable">`</span>mzo login <span class="token parameter variable">--help</span><span class="token variable">`</span></span> <span class="token keyword">for</span> persisting
  authentication between commands.

Password:
+--------------------+---------+
<span class="token operator">|</span> Name               <span class="token operator">|</span> Balance <span class="token operator">|</span>
+--------------------+---------+
<span class="token operator">|</span> 💸 Current Account <span class="token operator">|</span> <span class="token number">1337.00</span> <span class="token operator">|</span>
<span class="token operator">|</span> 🎾 Disposable      <span class="token operator">|</span>    <span class="token number">0.00</span> <span class="token operator">|</span>
<span class="token operator">|</span>                    <span class="token operator">|</span>         <span class="token operator">|</span>
<span class="token operator">|</span> 💰 Total           <span class="token operator">|</span> <span class="token number">1337.00</span> <span class="token operator">|</span>
+--------------------+---------+
</code></pre><div class="line-numbers" aria-hidden="true"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h3 id="sessions" tabindex="-1"><a class="header-anchor" href="#sessions" aria-hidden="true">#</a> Sessions</h3>
<p>There will be times when you want to perform a number of commands without needing
to provide your password for each command. For this the Monzo CLI provides login
sessions.</p>
<div class="language-bash line-numbers-mode" data-ext="sh"><pre v-pre class="language-bash"><code><span class="token comment"># start login session providing your password</span>
$ <span class="token builtin class-name">eval</span> <span class="token variable"><span class="token variable">$(</span>mzo login<span class="token variable">)</span></span>
Password:
Login Session Active

<span class="token comment"># invoke x number of commands</span>
$ mzo balance
+--------------------+---------+
<span class="token operator">|</span> Name               <span class="token operator">|</span> Balance <span class="token operator">|</span>
+--------------------+---------+
<span class="token operator">|</span> 💸 Current Account <span class="token operator">|</span> <span class="token number">1337.00</span> <span class="token operator">|</span>
<span class="token operator">|</span> 🎾 Disposable      <span class="token operator">|</span>    <span class="token number">0.00</span> <span class="token operator">|</span>
<span class="token operator">|</span>                    <span class="token operator">|</span>         <span class="token operator">|</span>
<span class="token operator">|</span> 💰 Total           <span class="token operator">|</span> <span class="token number">1337.00</span> <span class="token operator">|</span>
+--------------------+---------+

<span class="token comment"># Log back out of the session.</span>
<span class="token comment"># Requiring commands to either use one-off authentication</span>
<span class="token comment"># or a new login session to be started.</span>
<span class="token comment"># Sessions can also be ended by closing the</span>
<span class="token comment"># terminal window.</span>
$ <span class="token builtin class-name">eval</span> <span class="token variable"><span class="token variable">$(</span>mzo <span class="token builtin class-name">logout</span><span class="token variable">)</span></span>
Login Session Ended
</code></pre><div class="line-numbers" aria-hidden="true"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div class="custom-container tip"><p class="custom-container-title">What's with the eval?</p>
<p>Sessions are managed by temporarily storing a decrypted access token in
your terminal session's environment variables. you can see this if you
issue the <code v-pre>env</code> command during a login session.</p>
<p>A command-line application can not set a environment variable directly in the
shell session which invoked it. Instead, both <code v-pre>mzo login</code> and <code v-pre>mzo logout</code>
both return commands for (un)setting the access token which can be automatically
executed by the parent shell by wrapping it in its <code v-pre>eval</code> function.</p>
<p>You'll be able to see this by calling these commands without the eval function:</p>
<div class="language-bash line-numbers-mode" data-ext="sh"><pre v-pre class="language-bash"><code>$ mzo login
Password:
Login Session Active
<span class="token builtin class-name">export</span> <span class="token assign-left variable">MZO_ACCESS_TOKEN</span><span class="token operator">=</span><span class="token string">"xxxxxx.xxxxxxxxxxxxxxxxxxx.xxxxxxx"</span>
<span class="token comment"># This command is meant to be used with your shell's eval function.</span>
<span class="token comment"># Run 'eval $(mzo login)' to sign into your Monzo account.</span>
</code></pre><div class="line-numbers" aria-hidden="true"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><p>If your shell doesn't support that syntax (<code v-pre>bash</code> and <code v-pre>fish</code> do that I
know of), you can use the <code v-pre>--format raw</code> option to handle setting the
<code v-pre>MZO_ACCESS_TOKEN</code> environment variable yourself. If you are not sure
which shell you are running, it is probably bash.</p>
</div>
<h2 id="balance" tabindex="-1"><a class="header-anchor" href="#balance" aria-hidden="true">#</a> Balance</h2>
<p>The balance command returns the current balance of your current account along
with the balance of all of your pots.</p>
<div class="language-bash line-numbers-mode" data-ext="sh"><pre v-pre class="language-bash"><code>$ mzo balance
+--------------------+---------+
<span class="token operator">|</span> Name               <span class="token operator">|</span> Balance <span class="token operator">|</span>
+--------------------+---------+
<span class="token operator">|</span> 💸 Current Account <span class="token operator">|</span> <span class="token number">1337.00</span> <span class="token operator">|</span>
<span class="token operator">|</span> 🎾 Disposable      <span class="token operator">|</span>    <span class="token number">0.00</span> <span class="token operator">|</span>
<span class="token operator">|</span>                    <span class="token operator">|</span>         <span class="token operator">|</span>
<span class="token operator">|</span> 💰 Total           <span class="token operator">|</span> <span class="token number">1337.00</span> <span class="token operator">|</span>
+--------------------+---------+
</code></pre><div class="line-numbers" aria-hidden="true"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><p>For full documentation check out <code v-pre>mzo balance --help</code>.</p>
<h2 id="transactions" tabindex="-1"><a class="header-anchor" href="#transactions" aria-hidden="true">#</a> Transactions</h2>
<div class="custom-container warning"><p class="custom-container-title">WARNING</p>
<p>Work in progress. Available by setting <code v-pre>MZO_PRERELEASE=1</code> in terminal session's
environment variables.</p>
</div>
<p>List historic transactions.</p>
<div class="language-bash line-numbers-mode" data-ext="sh"><pre v-pre class="language-bash"><code>$ mzo transactions
+------------------+----------------------------------+----------+---------------+
<span class="token operator">|</span> Created          <span class="token operator">|</span> Name                             <span class="token operator">|</span> Amount   <span class="token operator">|</span> Category      <span class="token operator">|</span>
+------------------+----------------------------------+----------+---------------+
<span class="token operator">|</span> <span class="token punctuation">..</span>.              <span class="token operator">|</span> <span class="token punctuation">..</span>.                              <span class="token operator">|</span> <span class="token punctuation">..</span>.      <span class="token operator">|</span> <span class="token punctuation">..</span>.           <span class="token operator">|</span>
<span class="token operator">|</span> Sun <span class="token number">16</span> February  <span class="token operator">|</span> You Wish                         <span class="token operator">|</span> +100.00  <span class="token operator">|</span> General       <span class="token operator">|</span>
<span class="token operator">|</span> Sun <span class="token number">16</span> February  <span class="token operator">|</span> Amazon                           <span class="token operator">|</span> <span class="token number">12.99</span>    <span class="token operator">|</span> Shopping      <span class="token operator">|</span>
<span class="token operator">|</span> Mon <span class="token number">17</span> February  <span class="token operator">|</span> Sainsbury's                      <span class="token operator">|</span> <span class="token number">24.61</span>    <span class="token operator">|</span> Groceries     <span class="token operator">|</span>
+------------------+----------------------------------+----------+---------------+
</code></pre><div class="line-numbers" aria-hidden="true"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><p>For full documentation check out <code v-pre>mzo transactions --help</code>.</p>
<h2 id="pots" tabindex="-1"><a class="header-anchor" href="#pots" aria-hidden="true">#</a> Pots</h2>
<div class="custom-container warning"><p class="custom-container-title">WARNING</p>
<p>Work in progress. Available by setting <code v-pre>MZO_PRERELEASE=1</code> in terminal session's
environment variables.</p>
</div>
<p>Transfer money between pots and your current account. You can directly transfer from
one pot to another, and <code v-pre>mzo</code> will make to transfers <code v-pre>Pot 1 -&gt; Current Account -&gt; Pot 2</code>.</p>
<p>If only a <code v-pre>--from</code> or <code v-pre>--into</code> account is provided, the destination or source,
respectively, is assumed to be your current account.</p>
<p>The pot names provided are also fuzzy matched, so don't worry about getting exactly the
right name for the pot. If you have a pot called &quot;Bike Fund&quot;, for example, try
something like <code v-pre>mzo pots move 100 --into bike</code>.</p>
<div class="language-bash line-numbers-mode" data-ext="sh"><pre v-pre class="language-bash"><code>$ mzo pots move <span class="token number">50</span> <span class="token parameter variable">--into</span> disposable
+--------------------+---------+---------+
<span class="token operator">|</span> Name               <span class="token operator">|</span> Current <span class="token operator">|</span>   Final <span class="token operator">|</span>
+--------------------+---------+---------+
<span class="token operator">|</span> 💸 Current Account <span class="token operator">|</span> <span class="token number">1337.00</span> <span class="token operator">|</span> <span class="token number">1287.00</span> <span class="token operator">|</span>
<span class="token operator">|</span> 🎾 Disposable      <span class="token operator">|</span>    <span class="token number">0.00</span> <span class="token operator">|</span>   <span class="token number">50.00</span> <span class="token operator">|</span>
+--------------------+---------+---------+

Confirm this transfer <span class="token punctuation">[</span>y/N<span class="token punctuation">]</span>: y
Transfer Successful
</code></pre><div class="line-numbers" aria-hidden="true"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><p>For full documentation check out <code v-pre>mzo pots move --help</code>.</p>
<h2 id="formats" tabindex="-1"><a class="header-anchor" href="#formats" aria-hidden="true">#</a> Formats</h2>
<p>Most commands support different output formats like <code v-pre>human</code>, <code v-pre>csv</code>, and <code v-pre>json</code>.</p>
<p>Here's a example with the balance command:</p>
<div class="language-bash line-numbers-mode" data-ext="sh"><pre v-pre class="language-bash"><code>$ mzo balance <span class="token parameter variable">--format</span> csv
name,balance
Current Account,1337.0
Disposable,0.0
Total,1337.0

$ mzo balance <span class="token parameter variable">--format</span> json
<span class="token punctuation">[</span>
  <span class="token punctuation">{</span>
    <span class="token string">"name"</span><span class="token builtin class-name">:</span> <span class="token string">"Current Account"</span>,
    <span class="token string">"balance"</span><span class="token builtin class-name">:</span> <span class="token number">1337.0</span>
  <span class="token punctuation">}</span>,
  <span class="token punctuation">{</span>
    <span class="token string">"name"</span><span class="token builtin class-name">:</span> <span class="token string">"Disposable"</span>,
    <span class="token string">"balance"</span><span class="token builtin class-name">:</span> <span class="token number">0.0</span>
  <span class="token punctuation">}</span>,
  <span class="token punctuation">{</span>
    <span class="token string">"name"</span><span class="token builtin class-name">:</span> <span class="token string">"Total"</span>,
    <span class="token string">"balance"</span><span class="token builtin class-name">:</span> <span class="token number">1337.0</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">]</span>
</code></pre><div class="line-numbers" aria-hidden="true"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><p>You can use this to create spreadsheets or to pipe into other applications like
<a href="https://stedolan.github.io/jq/" target="_blank" rel="noopener noreferrer">jq<ExternalLinkIcon/></a>.</p>
<div class="language-bash line-numbers-mode" data-ext="sh"><pre v-pre class="language-bash"><code>$ mzo balance <span class="token parameter variable">--format</span> csv <span class="token operator">></span> ~/Desktop/balance.csv

$ mzo balance <span class="token parameter variable">--format</span> json <span class="token operator">|</span> jq <span class="token string">'.[] | select(.name == "Total") | .balance'</span>
<span class="token number">1337.0</span>
</code></pre><div class="line-numbers" aria-hidden="true"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><p>By default the formats for commands is set to <code v-pre>human</code>. You can change this by
editing the <code v-pre>~/.mzo/config</code> file and setting the default format to either
<code v-pre>human</code>, <code v-pre>csv</code> or <code v-pre>json</code>.</p>
<div class="language-toml line-numbers-mode" data-ext="toml"><pre v-pre class="language-toml"><code><span class="token punctuation">[</span><span class="token table class-name">default</span><span class="token punctuation">]</span>
<span class="token key property">account_id</span> <span class="token punctuation">=</span> <span class="token string">"acc_xxxxx"</span>
<span class="token key property">format</span> <span class="token punctuation">=</span> <span class="token string">"human"</span>

<span class="token punctuation">[</span><span class="token table class-name">oauth</span><span class="token punctuation">]</span>
<span class="token key property">client_id</span> <span class="token punctuation">=</span> <span class="token string">"oauth2client_xxxxx"</span>
<span class="token key property">client_secret</span> <span class="token punctuation">=</span> <span class="token string">"xxxxxxxxxxxxxx"</span>
</code></pre><div class="line-numbers" aria-hidden="true"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><p>Check out the documentation for each command with <code v-pre>--help</code> for full documentation.</p>
</div></template>


