import fs from 'node:fs';
import path from 'node:path';
import matrixData from '../data/compute_matrix.json';

export async function GET() {
  const siteUrl = 'https://technommy.github.io';
  const now = new Date().toISOString().split('T')[0];

  // Read archive dates
  const digestsDir = path.resolve(process.cwd(), 'src/data/digests');
  let archiveUrls: { loc: string; priority: string; changefreq: string }[] = [];
  if (fs.existsSync(digestsDir)) {
    const files = fs.readdirSync(digestsDir).filter((f) => f.endsWith('.json'));
    archiveUrls = files.map((file) => ({
      loc: `${siteUrl}/digest/${file.replace('.json', '')}/`,
      priority: '0.7',
      changefreq: 'never',
    }));
  }

  const urls = [
    { loc: `${siteUrl}/`, priority: '1.0', changefreq: 'daily' },
    { loc: `${siteUrl}/compare/`, priority: '0.9', changefreq: 'weekly' },
    ...archiveUrls,
    ...matrixData.map((sc) => ({
      loc: `${siteUrl}/compare/${sc.slug}/`,
      priority: '0.8',
      changefreq: 'weekly',
    })),
  ];

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls
  .map(
    (u) => `  <url>
    <loc>${u.loc}</loc>
    <lastmod>${now}</lastmod>
    <changefreq>${u.changefreq}</changefreq>
    <priority>${u.priority}</priority>
  </url>`
  )
  .join('\n')}
</urlset>`;

  return new Response(xml, {
    headers: {
      'Content-Type': 'application/xml; charset=utf-8',
    },
  });
}
