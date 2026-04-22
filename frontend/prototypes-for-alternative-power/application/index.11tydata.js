export default {
  layout: "application.njk",
  showHomeButton: true,
  homeUrl: "/",
  pagination: {
    data: "artworks",
    size: 1,
    alias: "artwork"
  },
  permalink: (data) => `/detail/${data.artwork.slug}/application/`,
  eleventyComputed: {
    artist: (data) => data.artwork.artist,
    title: (data) => data.artwork.title,
    year: (data) => data.artwork.year,
    medium: (data) => data.artwork.medium,
    duration: (data) => data.artwork.duration,
    description: (data) => data.artwork.description,
    hasApplication: (data) => data.artwork.hasApplication,
    slug: (data) => data.artwork.slug,
    applicationTitle: (data) => data.artwork.applicationTitle,
    applicationLinks: (data) => data.artwork.applicationLinks
  }
};
