import './globals.css';

export const metadata = {
  title: 'Vemula Syam Prakash — Python · AI/ML · GenAI · Backend',
  description: 'Vemula Syam Prakash builds practical AI products, backend systems and cloud/data workflows with Python, GenAI and modern engineering tools.',
  keywords: ['Vemula Syam Prakash','Python Developer','AI/ML Engineer','GenAI','Backend Developer','AWS','Data Engineering'],
  openGraph: {
    title: 'Vemula Syam Prakash — Software Engineer & AI Builder',
    description: 'Practical AI products, backend systems and cloud/data workflows.',
    type: 'website',
  },
};

export default function RootLayout({ children }) {
  return <html lang="en"><body>{children}</body></html>;
}
