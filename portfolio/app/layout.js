import './globals.css';

export const metadata = {
  metadataBase: new URL('https://syam-prakash-portfolio.onrender.com'),
  title: 'Vemula Syam Prakash — Python · AI/ML · GenAI · Backend',
  description: 'Vemula Syam Prakash builds practical AI products, backend systems and cloud/data workflows with Python, GenAI and modern engineering tools.',
  keywords: ['Vemula Syam Prakash','Python Developer','AI/ML Engineer','GenAI','Backend Developer','AWS','Data Engineering'],
  authors: [{ name: 'Vemula Syam Prakash' }],
  creator: 'Vemula Syam Prakash',
  alternates: { canonical: '/' },
  openGraph: {
    title: 'Vemula Syam Prakash — Software Engineer & AI Builder',
    description: 'Practical AI products, backend systems and cloud/data workflows.',
    url: 'https://syam-prakash-portfolio.onrender.com',
    siteName: 'Vemula Syam Prakash',
    type: 'website',
    locale: 'en_IN',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Vemula Syam Prakash — Software Engineer & AI Builder',
    description: 'Practical AI products, backend systems and cloud/data workflows.',
  },
  robots: {
    index: true,
    follow: true,
    googleBot: { index: true, follow: true, 'max-image-preview': 'large' },
  },
};

export const viewport = {
  width: 'device-width',
  initialScale: 1,
  viewportFit: 'cover',
  themeColor: '#050505',
  colorScheme: 'dark',
};

export default function RootLayout({ children }) {
  return <html lang="en"><body>{children}</body></html>;
}
