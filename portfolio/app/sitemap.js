const baseUrl = 'https://syam-prakash-portfolio.onrender.com';

export default function sitemap() {
  return [{
    url: baseUrl,
    lastModified: new Date(),
    changeFrequency: 'monthly',
    priority: 1,
  }];
}
