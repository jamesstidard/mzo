<template><div><div class="custom-container warning"><p class="custom-container-title">Disclosure</p>
<p>This is not an official command-line application from Monzo, but a
third-party, open-source one implemented using Monzo's Developer API.</p>
</div>
<div class="custom-container danger"><p class="custom-container-title">Beta Software</p>
<p>The Monzo Developer API and this application are still under development
so both could break at any time.</p>
</div>
<h1 id="example-usage" tabindex="-1"><a class="header-anchor" href="#example-usage" aria-hidden="true">#</a> Example Usage</h1>
<div class="language-bash line-numbers-mode" data-ext="sh"><pre v-pre class="language-bash"><code>$ <span class="token builtin class-name">eval</span> <span class="token variable"><span class="token variable">$(</span>mzo login<span class="token variable">)</span></span>
Password: ********

$ mzo balance
+--------------------+---------+
<span class="token operator">|</span> Name               <span class="token operator">|</span> Balance <span class="token operator">|</span>
+--------------------+---------+
<span class="token operator">|</span> 💸 Current Account <span class="token operator">|</span> <span class="token number">1337.00</span> <span class="token operator">|</span>
<span class="token operator">|</span> 🎾 Disposable      <span class="token operator">|</span>    <span class="token number">0.00</span> <span class="token operator">|</span>
<span class="token operator">|</span>                    <span class="token operator">|</span>         <span class="token operator">|</span>
<span class="token operator">|</span> 💰 Total           <span class="token operator">|</span> <span class="token number">1337.00</span> <span class="token operator">|</span>
+--------------------+---------+

$ mzo pots move <span class="token number">50</span> <span class="token parameter variable">--into</span> disposable
+--------------------+---------+---------+
<span class="token operator">|</span> Name               <span class="token operator">|</span> Current <span class="token operator">|</span>   Final <span class="token operator">|</span>
+--------------------+---------+---------+
<span class="token operator">|</span> 💸 Current Account <span class="token operator">|</span> <span class="token number">1337.00</span> <span class="token operator">|</span> <span class="token number">1287.00</span> <span class="token operator">|</span>
<span class="token operator">|</span> 🎾 Disposable      <span class="token operator">|</span>    <span class="token number">0.00</span> <span class="token operator">|</span>   <span class="token number">50.00</span> <span class="token operator">|</span>
+--------------------+---------+---------+

Confirm this transfer <span class="token punctuation">[</span>y/N<span class="token punctuation">]</span>: y
Transfer Successful

$ <span class="token builtin class-name">eval</span> <span class="token variable"><span class="token variable">$(</span>mzo <span class="token builtin class-name">logout</span><span class="token variable">)</span></span>
</code></pre><div class="line-numbers" aria-hidden="true"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div></div></template>


