<template><div><h1 id="install-options" tabindex="-1"><a class="header-anchor" href="#install-options" aria-hidden="true">#</a> Install Options</h1>
<h2 id="homebrew" tabindex="-1"><a class="header-anchor" href="#homebrew" aria-hidden="true">#</a> Homebrew</h2>
<p><a href="https://brew.sh/" target="_blank" rel="noopener noreferrer">Homebrew<ExternalLinkIcon/></a> is the de-facto package manager on macOS.
If you are installing on macOS, this is the way to go.</p>
<div class="language-bash line-numbers-mode" data-ext="sh"><pre v-pre class="language-bash"><code>$ brew tap jamesstidard/formulas
$ brew <span class="token function">install</span> mzo
</code></pre><div class="line-numbers" aria-hidden="true"><div class="line-number"></div><div class="line-number"></div></div></div><h2 id="pypi" tabindex="-1"><a class="header-anchor" href="#pypi" aria-hidden="true">#</a> PyPI</h2>
<div class="custom-container warning"><p class="custom-container-title">WARNING</p>
<p>For those familiar with Python package management.</p>
</div>
<p>Monzo CLI is a Python application and is hosted on PyPI so can be
installed as a Python package.</p>
<p>I personally use <a href="https://github.com/pyenv/pyenv" target="_blank" rel="noopener noreferrer">pyenv<ExternalLinkIcon/></a> for managing
multiple Python versions on a single machine in combination with
<a href="https://github.com/mitsuhiko/pipsi" target="_blank" rel="noopener noreferrer">pipsi<ExternalLinkIcon/></a> for installing global Python
packages as it manages creating specific Python virtual environments for
each package - preventing any dependency conflicts with other installed
python packages.</p>
<div class="language-bash line-numbers-mode" data-ext="sh"><pre v-pre class="language-bash"><code><span class="token comment"># install</span>
$ pipsi <span class="token function">install</span> mzo <span class="token parameter variable">--python</span> <span class="token number">3.6</span>.5
</code></pre><div class="line-numbers" aria-hidden="true"><div class="line-number"></div><div class="line-number"></div></div></div><p>Though if you've opted to install through this method, you probably
already have a install process in mind.</p>
<h2 id="source" tabindex="-1"><a class="header-anchor" href="#source" aria-hidden="true">#</a> Source</h2>
<p>If you'd like to get it directly from the source, it can be found
hosted on GitHub <a href="https://github.com/jamesstidard/mzo-cli" target="_blank" rel="noopener noreferrer">here<ExternalLinkIcon/></a>.</p>
<p>The documentation on how to build the environment should be on the
project's README.</p>
<div class="language-bash line-numbers-mode" data-ext="sh"><pre v-pre class="language-bash"><code>$ <span class="token function">git</span> clone https://github.com/jamesstidard/mzo-cli.git
$ <span class="token function">cat</span> mzo-cli/README.md
</code></pre><div class="line-numbers" aria-hidden="true"><div class="line-number"></div><div class="line-number"></div></div></div></div></template>


