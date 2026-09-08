from datetime import datetime, timezone

from .config import BASE, DIST, JSON_HASHES, PAGES

def support_files():
    # O endereço antigo continua levando para a home.
    csp_hashes = ' '.join("'" + h + "'" for h in sorted(JSON_HASHES))
    config = f'''Options -Indexes
DirectoryIndex index.html
ErrorDocument 404 /404.html
AddDefaultCharset UTF-8
<IfModule mod_rewrite.c>
RewriteEngine On
RewriteCond %{{HTTP_HOST}} ^www\\.xn--hugoservios-u9a\\.com$ [NC]
RewriteRule ^ https://xn--hugoservios-u9a.com%{{REQUEST_URI}} [R=301,L,NE]
RewriteCond %{{HTTPS}} !=on
RewriteCond %{{HTTP:X-Forwarded-Proto}} !https [NC]
RewriteCond %{{HTTP:X-Forwarded-SSL}} !on [NC]
RewriteRule ^ https://xn--hugoservios-u9a.com%{{REQUEST_URI}} [R=301,L,NE]
RewriteCond %{{THE_REQUEST}} \\s/+(.*/)?index\\.html[?\\s] [NC]
RewriteRule ^ /%1 [R=301,L,NE]
RewriteRule ^default\\.php$ / [R=301,L]
</IfModule>
<IfModule mod_headers.c>
Header always set X-Content-Type-Options "nosniff"
Header always set Referrer-Policy "strict-origin-when-cross-origin"
Header always set X-Frame-Options "DENY"
Header always set Permissions-Policy "camera=(), microphone=(), geolocation=()"
Header always set Content-Security-Policy "default-src 'self'; script-src 'self' {csp_hashes}; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'; form-action https://wa.me; upgrade-insecure-requests"
<FilesMatch "\\.(html|xml|txt)$">
Header set Cache-Control "public, max-age=0, must-revalidate"
</FilesMatch>
<FilesMatch "\\.(webp|svg|woff2)$">
Header set Cache-Control "public, max-age=604800"
</FilesMatch>
<FilesMatch "\\.[a-f0-9]{{10}}\\.(css|js)$">
Header set Cache-Control "public, max-age=31536000, immutable"
</FilesMatch>
</IfModule>
<IfModule mod_deflate.c>
AddOutputFilterByType DEFLATE text/html text/css text/plain text/javascript application/javascript application/json application/ld+json application/xml image/svg+xml
</IfModule>
<IfModule mod_mime.c>
AddType image/webp .webp
AddType font/woff2 .woff2
</IfModule>
'''
    (DIST / '.htaccess').write_text(config, encoding='utf-8')
    (DIST / 'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n', encoding='utf-8')
    today = datetime.now(timezone.utc).date().isoformat()
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{BASE}{path}</loc><lastmod>{today}</lastmod></url>\n' for path in PAGES) + '</urlset>\n'
    (DIST / 'sitemap.xml').write_text(sitemap, encoding='utf-8')
    (DIST / 'favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#1558e8"/><path d="M14 14h9v13h15V14h9v36h-9V36H23v14h-9Z" fill="#fff"/><circle cx="53" cy="49" r="5" fill="#ff8c42"/></svg>', encoding='utf-8')
