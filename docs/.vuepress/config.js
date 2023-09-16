import { defineUserConfig } from 'vuepress'
import { defaultTheme } from '@vuepress/theme-default'

export default defineUserConfig({
  lang: 'en-US',
  title: 'MZO CLI',
  description: 'Sometimes typing is more convenient then swiping and tapping... Sometimes.',
  theme: defaultTheme({
    navbar: [
      { text: 'Documentation', link: '/docs/' },
    ],
    repo: 'https://github.com/jamesstidard/mzo-cli',
    sidebar: [
      '/docs/',
      '/docs/install',
      '/docs/usage',
      '/docs/uninstall',
    ],
  })
})
