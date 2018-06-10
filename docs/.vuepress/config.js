module.exports = {
  title: 'Monzo CLI',
  description: 'Sometimes typing is more convenient then swiping and tapping... Sometimes.',
  ga: 'UA-33148627-2',
  base: '/Monzo-Cli/', // For github pages
  themeConfig: {
    nav: [
      { text: 'Documentation', link: '/docs/' },
      { text: 'GitHub', link: 'https://github.com/jamesstidard/monzo-cli' },
    ],
    sidebar: [
      '/docs/',
      '/docs/install',
      '/docs/usage',
      '/docs/uninstall',
    ],
  },
}
