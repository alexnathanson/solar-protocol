export default {
  layout: "detail.njk",
  showHomeButton: true,
  homeUrl: "/",
  pagination: {
    data: "artworks",
    size: 1,
    alias: "artwork"
  },
  permalink: (data) => `/detail/${data.artwork.slug}.html`,
  eleventyComputed: {
    artist: (data) => data.artwork.artist,
    title: (data) => data.artwork.title,
    year: (data) => data.artwork.year,
    medium: (data) => data.artwork.medium,
    duration: (data) => data.artwork.duration,
    description: (data) => data.artwork.description,
    hasEssay: (data) => data.artwork.hasEssay,
    hasApplication: (data) => data.artwork.hasApplication,
    slug: (data) => data.artwork.slug,
    presentationType: (data) => data.artwork.presentationType,
    mediaUrl: (data) => data.artwork.mediaUrl,
    customTemplate: (data) => data.artwork.customTemplate,
    autoplay: (data) => data.artwork.autoplay !== false,
    loop: (data) => data.artwork.loop || false,
    iframeWidth: (data) => data.artwork.iframeWidth,
    iframeHeight: (data) => data.artwork.iframeHeight,
    allowSandbox: (data) => data.artwork.allowSandbox,
    applicationTitle: (data) => data.artwork.applicationTitle,
    applicationLinks: (data) => data.artwork.applicationLinks,
    essayLinkText: (data) => data.artwork.essayLinkText
  }
};
