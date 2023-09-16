<template><div><h1 id="uninstall" tabindex="-1"><a class="header-anchor" href="#uninstall" aria-hidden="true">#</a> Uninstall</h1>
<p>The Monzo CLI consists of two parts which you will want to remove when
uninstalling the application. These are the binary itself along with
application data (which stores your encrypted credentials and personal
configurations).</p>
<h2 id="removing-the-application" tabindex="-1"><a class="header-anchor" href="#removing-the-application" aria-hidden="true">#</a> Removing the Application</h2>
<p>Removing the binary depends on which method you used to initially install
the application:</p>
<div class="language-bash line-numbers-mode" data-ext="sh"><pre v-pre class="language-bash"><code><span class="token comment"># Homebrew</span>
$ brew uninstall mzo
$ brew untap jamesstidard/formulas
</code></pre><div class="line-numbers" aria-hidden="true"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h2 id="removing-application-data" tabindex="-1"><a class="header-anchor" href="#removing-application-data" aria-hidden="true">#</a> Removing Application Data</h2>
<p>Application data is stored in a hidden folder in your home directory
named <code v-pre>.mzo</code>. This can be removed from your terminal with:</p>
<div class="language-bash line-numbers-mode" data-ext="sh"><pre v-pre class="language-bash"><code>$ <span class="token function">rm</span> <span class="token parameter variable">-rf</span> ~/.mzo
</code></pre><div class="line-numbers" aria-hidden="true"><div class="line-number"></div></div></div></div></template>


