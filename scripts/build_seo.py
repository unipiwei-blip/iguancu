# -*- coding: utf-8 -*-
"""生成 SEO 配套：sitemap.xml / robots.txt / 404.html / .htaccess / nginx 示例。"""
import os, sys, io, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import BASE, BRAND, CONTACT, BRAND_NAV, NEWS

SITE = r"D:\项目管理文件夹\2026-11-19-15-27-25\site"
TODAY = datetime.date.today().isoformat()  # lastmod 用生成当天

PAGES = [
    ("", "1.0", "daily"),
    ("about.html", "0.9", "monthly"),
    ("group.html", "0.7", "monthly"),
    ("culture.html", "0.7", "monthly"),
    ("team.html", "0.6", "monthly"),
    ("honors.html", "0.6", "monthly"),
    ("services.html", "0.9", "monthly"),
    ("service-patent.html", "0.8", "monthly"),
    ("service-trademark.html", "0.8", "monthly"),
    ("service-copyright.html", "0.7", "monthly"),
    ("service-international.html", "0.7", "monthly"),
    ("service-litigation.html", "0.7", "monthly"),
    ("service-project.html", "0.8", "monthly"),
    ("service-operation.html", "0.7", "monthly"),
    ("process.html", "0.6", "monthly"),
    ("news.html", "0.8", "daily"),
    ("notice.html", "0.7", "daily"),
    ("policy.html", "0.7", "daily"),
    ("knowledge.html", "0.7", "daily"),
    ("cases.html", "0.6", "monthly"),
    ("faq.html", "0.6", "monthly"),
    ("contact.html", "0.8", "monthly"),
    ("sitemap.html", "0.3", "monthly"),
]

# 文章页按 NEWS 自动生成，确保与 build.py 产出页面始终一致
PAGES += [(n["file"], "0.6", "monthly") for n in NEWS]

def build_sitemap_xml():
    entries = []
    for p, pri, freq in PAGES:
        entries.append(
            "  <url>\n    <loc>%s/%s</loc>\n    <lastmod>%s</lastmod>\n    <changefreq>%s</changefreq>\n    <priority>%s</priority>\n  </url>"
            % (BASE, p, TODAY, freq, pri)
        )
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(entries) + "\n</urlset>\n"
    with open(os.path.join(SITE, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(xml)
    print("sitemap.xml done, urls=%d, lastmod=%s" % (len(PAGES), TODAY))

def build_robots():
    robots = (
        "# robots.txt for __BASE__\n\n"
        "User-agent: *\nAllow: /\n\n"
        "User-agent: Baiduspider\nAllow: /\n\n"
        "User-agent: Googlebot\nAllow: /\n\n"
        "Host: __BASE__\nSitemap: __BASE__/sitemap.xml\n"
    ).replace("__BASE__", BASE)
    with open(os.path.join(SITE, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots)
    print("robots.txt done")

def build_404():
    html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>页面未找到（404）｜__BRAND__</title>
<meta name="description" content="您访问的页面不存在或已移动。">
<meta name="robots" content="noindex,follow">
<link rel="stylesheet" href="/assets/css/style.css">
</head>
<body>
<header class="site-header"><div class="container header-inner">
  <a class="brand" href="/" aria-label="返回首页">
    <img class="brand__mark" src="/assets/img/logo-blue.png" alt="">
    <span class="brand__name">__NAV__</span>
  </a>
</div></header>
<main>
<div class="error-page"><div>
  <div class="error-code">4<span>0</span>4</div>
  <h1>页面未找到</h1>
  <p>您访问的页面不存在或已移动。您可以返回首页，或通过网站地图查找需要的栏目。</p>
  <div class="cta-btns" style="justify-content:center">
    <a class="btn btn--primary btn--lg" href="/">返回首页</a>
    <a class="btn btn--outline btn--lg" href="/sitemap.html">网站地图</a>
  </div>
  <div style="margin-top:24px;color:#5A6B85;font-size:14px">
    <a href="/about.html">关于莞促</a> · <a href="/services.html">专业服务</a> · <a href="/news.html">新闻资讯</a> · <a href="/contact.html">联系我们</a>
  </div>
</div></div>
</main>
<footer class="site-footer"><div class="container footer-bottom" style="justify-content:center">
  <span>© 2026 __BRAND__ 版权所有 ｜ 服务时间：__WORKTIME__</span>
</div></footer>
</body>
</html>
'''.replace("__BRAND__", BRAND).replace("__NAV__", BRAND_NAV).replace("__WORKTIME__", CONTACT["worktime"])
    with open(os.path.join(SITE, "404.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("404.html done (noindex,follow, no redirect)")

def build_server_configs():
    host = BASE.replace("https://", "").replace("http://", "")
    apex = host[4:] if host.startswith("www.") else host

    htaccess = '''# ============ 301 规范化（Apache）============
RewriteEngine On

# 强制 HTTPS
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://__HOST__/$1 [R=301,L]

# 统一主域名到 www（若主域不带 www，请删除这两行并调整上方规则）
RewriteCond %{HTTP_HOST} !^__HOST__$ [NC]
RewriteRule ^(.*)$ https://__HOST__/$1 [R=301,L]

# 目录默认页规范化
RewriteRule ^index\.html$ / [R=301,L]

# ============ 404 返回正确 HTTP 状态 ============
ErrorDocument 404 /404.html

# ============ MIME / 缓存 ============
AddType text/html .html
<FilesMatch "\.(css|js|png|jpg|jpeg|gif|svg|webp)$">
  Header set Cache-Control "public, max-age=604800"
</FilesMatch>
'''.replace("__HOST__", host)
    with open(os.path.join(SITE, ".htaccess"), "w", encoding="utf-8") as f:
        f.write(htaccess)

    nginx = '''# ============ 301 规范化与 404（Nginx）============
server {
    listen 80;
    server_name __APEX__ www.__APEX__;
    return 301 https://www.__APEX__$request_uri;
}

server {
    listen 443 ssl http2;
    server_name __APEX__ www.__APEX__;
    # ssl_certificate /path/to/cert.pem;
    # ssl_certificate_key /path/to/key.pem;
    root /path/to/site;
    index index.html;

    # 非 www 跳转 www（若主域不带 www 可删除本段并调整 server_name）
    if ($host = '__APEX__') { return 301 https://www.__APEX__$request_uri; }

    # 404 返回正确状态码（不要用 JS/meta 跳转）
    error_page 404 /404.html;
    location = /404.html { internal; }

    location / { try_files $uri $uri/ =404; }
    location ~* \.(css|js|png|jpg|jpeg|gif|svg|webp)$ {
        expires 7d;
        add_header Cache-Control "public";
    }
}
'''.replace("__APEX__", apex)
    with open(os.path.join(SITE, "nginx.conf.example"), "w", encoding="utf-8") as f:
        f.write(nginx)
    print(".htaccess & nginx.conf.example done")

if __name__ == "__main__":
    build_sitemap_xml(); build_robots(); build_404(); build_server_configs()
    print("SEO FILES DONE")
