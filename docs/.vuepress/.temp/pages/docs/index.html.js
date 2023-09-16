export const data = JSON.parse("{\"key\":\"v-147825fb\",\"path\":\"/docs/\",\"title\":\"Overview\",\"lang\":\"en-US\",\"frontmatter\":{},\"headers\":[],\"git\":{\"updatedTime\":1587479019000,\"contributors\":[{\"name\":\"James Stidard\",\"email\":\"james@stidard.com\",\"commits\":9},{\"name\":\"James Stidard\",\"email\":\"james@wave-venture.com\",\"commits\":6}]},\"filePathRelative\":\"docs/README.md\"}")

if (import.meta.webpackHot) {
  import.meta.webpackHot.accept()
  if (__VUE_HMR_RUNTIME__.updatePageData) {
    __VUE_HMR_RUNTIME__.updatePageData(data)
  }
}

if (import.meta.hot) {
  import.meta.hot.accept(({ data }) => {
    __VUE_HMR_RUNTIME__.updatePageData(data)
  })
}
