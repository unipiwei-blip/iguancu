# -*- coding: utf-8 -*-
"""统一模板：SEO head、页头、页脚、JSON-LD。所有页面复用，保证一致性与 SEO 完整。"""
import json
from config import BASE, BRAND, BRAND_SHORT, BRAND_NAV, BRAND_EN, SLOGAN, LOC, CONTACT, FRIENDS, NAV

YEAR = 2026

def seo_head(title, description, keywords, canonical, og_type="website", og_image=None, jsonld=None, extra_css=""):
    img = og_image or (BASE + "/assets/img/share-brand.jpg")
    canon = BASE + "/" + canonical
    ld = jsonld if jsonld is not None else org_jsonld()
    ld_script = ('<script type="application/ld+json">%s</script>' % json.dumps(ld, ensure_ascii=False)) if ld else ""
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="keywords" content="{keywords}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{img}">
<meta property="og:site_name" content="{BRAND}">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index,follow">
<meta name="author" content="{BRAND}">
<link rel="icon" href="/assets/img/logo-blue.png" type="image/png">
<link rel="stylesheet" href="/assets/css/style.css">
{ld_script}
{extra_css}
</head>'''

def org_jsonld():
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": BRAND,
        "alternateName": BRAND_SHORT,
        "url": BASE + "/",
        "logo": BASE + "/assets/img/logo-blue.png",
        "image": BASE + "/assets/img/share-brand.jpg",
        "telephone": CONTACT["tel"],
        "email": CONTACT["email"],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": CONTACT["address_full"],
            "postalCode": CONTACT["postcode"],
            "addressRegion": "广东省",
            "addressLocality": "东莞市",
            "addressCountry": "CN"
        },
        "contactPoint": [{
            "@type": "ContactPoint",
            "telephone": CONTACT["mobile"],
            "contactType": "customer service",
            "contactOption": "TollFree",
            "areaServed": "CN",
            "availableLanguage": ["Chinese"]
        }],
        "parentOrganization": {"@type": "Organization", "name": "莞促集团", "url": "https://www.guancu.com/"}
    }

def web_page_jsonld(name, desc, url, ptype="WebPage"):
    return {
        "@context": "https://schema.org",
        "@type": ptype,
        "name": name,
        "description": desc,
        "url": BASE + "/" + url,
        "inLanguage": "zh-CN",
        "isPartOf": {"@type": "WebSite", "name": BRAND_SHORT, "url": BASE + "/"},
        "publisher": {"@type": "Organization", "name": BRAND}
    }

def header(active=""):
    def link(h):
        return "" if h == "index.html" else h
    nav_html = []
    for item in NAV:
        is_active = " is-active" if item["href"] == active or active.startswith(item["href"].replace(".html","")) and item["href"] != "index.html" else ""
        if item.get("children"):
            subs = "".join(f'<a href="/{link(h)}"><span class="dot"></span>{l}</a>' for l, h in item["children"])
            nav_html.append(f'''<li class="nav-drop">
              <a class="nav-link{is_active}" href="/{link(item['href'])}">{item['label']}</a>
              <div class="nav-drop__menu">{subs}</div>
            </li>''')
        else:
            nav_html.append(f'<li><a class="nav-link{is_active}" href="/{link(item["href"])}">{item["label"]}</a></li>')
    nav = "\n".join(nav_html)
    return f'''<div class="topbar">莞促集团 · 企业服务 · 财税 · 知识产权 ｜ 扎根东莞，服务粤港澳大湾区</div>
<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="/" aria-label="{BRAND}首页">
      <img class="brand__mark" src="/assets/img/logo-blue.png" alt="">
      <span class="brand__name">{BRAND_NAV}</span>
    </a>
    <nav class="main-nav" aria-label="主导航"><ul>
{nav}
    </ul></nav>
    <div class="header-actions">
      <a class="btn btn--gold nav-cta" href="/contact.html">业务咨询</a>
      <button class="nav-toggle" aria-label="打开菜单" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>'''

def footer(page_type="WebPage"):
    friends = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{n}</a></li>' for n, u in FRIENDS)
    return f'''<footer class="site-footer">
  <div class="container">
    <div class="footer-top">
      <div class="footer-brand">
        <div class="footer-brand__head">
          <img class="footer-logo" src="/assets/img/logo-blue.png" alt="{BRAND_SHORT}">
          <div>
            <div class="footer-brand__name">{BRAND_NAV}</div>
          </div>
        </div>
        <p class="footer-brand__desc">{LOC}，提供专利、商标、版权、涉外知识产权、维权与科技项目申报等一站式服务。</p>
      </div>
      <div class="footer-contact">
        <h4 class="footer-contact__title">联系方式</h4>
        <div class="footer-qr">
          <img src="/assets/img/qr-contact.png" alt="扫码咨询">
          <p>扫码添加微信咨询</p>
        </div>
        <div class="footer-contact-lines">
          <div>咨询电话：{CONTACT['mobile']}</div>
          <div>服务热线：{CONTACT['tel']}</div>
          <div>邮箱：{CONTACT['email']}</div>
        </div>
      </div>
    </div>
    <div class="footer-navwrap">
      <div class="footer-navrow">
        <h4>重点业务</h4>
        <ul class="footer-inline">
          <li><a href="/service-patent.html">专利服务</a></li>
          <li><a href="/service-trademark.html">商标服务</a></li>
          <li><a href="/service-copyright.html">版权服务</a></li>
          <li><a href="/service-international.html">涉外知识产权</a></li>
          <li><a href="/service-litigation.html">维权与法律</a></li>
          <li><a href="/service-project.html">科技项目申报</a></li>
          <li><a href="/service-operation.html">知产运营与托管</a></li>
          <li><a href="/process.html">服务流程</a></li>
        </ul>
      </div>
      <div class="footer-navrow">
        <h4>网站导航</h4>
        <ul class="footer-inline">
          <li><a href="/about.html">关于莞促</a></li>
          <li><a href="/group.html">莞促集团</a></li>
          <li><a href="/culture.html">企业文化</a></li>
          <li><a href="/news.html">新闻资讯</a></li>
          <li><a href="/notice.html">通知公告</a></li>
          <li><a href="/cases.html">成功案例</a></li>
          <li><a href="/faq.html">常见问题</a></li>
          <li><a href="/contact.html">联系我们</a></li>
          <li><a href="/sitemap.html">网站地图</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-fulladdr">办公地址：{CONTACT['address_full']}（邮编 {CONTACT['postcode']}）</div>
    <div class="footer-links">
      <h4>友情链接</h4>
      <ul>{friends}</ul>
    </div>
    <div class="footer-bottom">
      <span>© {YEAR} {BRAND} 版权所有</span>
      <span>官网：{BASE} ｜ 服务时间：{CONTACT['worktime']}</span>
    </div>
  </div>
</footer>
<script src="/assets/js/main.js"></script>'''

def page(title, description, keywords, canonical, body, og_type="website", og_image=None, jsonld=None, active="", body_class=""):
    return f'''{seo_head(title, description, keywords, canonical, og_type, og_image, jsonld)}
<body class="{body_class}">
{header(active)}
<main>
{body}
</main>
{footer()}
</body>
</html>'''
