# -*- coding: utf-8 -*-
"""生成全站静态页面。运行：python build.py"""
import os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import *
from tpl import page, web_page_jsonld, org_jsonld

SITE = r"D:\项目管理文件夹\2026-11-19-15-27-25\site"
os.chdir(SITE)

def write(path, html):
    full = os.path.join(SITE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)

def seo(key):
    """从统一配置取 (title, description, keywords)，避免各页面重复硬编码。"""
    t, d, k = SEO[key]
    return t, d, k

def crumb(*items):
    parts = ['<a href="/">首页</a>']
    for name, href in items:
        parts.append((' / <a href="/%s">%s</a>' % (href, name)) if href else (' / ' + name))
    return '<div class="crumb">' + ''.join(parts) + '</div>'

def ph(title, sub, en=""):
    enhtml = '<div class="ph-en">%s</div>' % en if en else ''
    return '''<section class="page-hero">
  <div class="hero-city"></div>
  <div class="container page-hero-inner">
%s<h1>%s</h1><p class="ph-sub">%s</p>
  </div>
</section>''' % (enhtml, title, sub)

# ============ 首页 ============
# 集团式彩色渐变（与集团官网 biz-ico 一致的多彩配色）
GRADS = [
    "linear-gradient(135deg,#2b7bff,#4d9bff)",
    "linear-gradient(135deg,#e2157f,#ff7a4d)",
    "linear-gradient(135deg,#7a4bff,#a06bff)",
    "linear-gradient(135deg,#2fbfe0,#2b7bff)",
    "linear-gradient(135deg,#0b47d6,#5b5bff)",
    "linear-gradient(135deg,#ffa62b,#ff7a4d)",
    "linear-gradient(135deg,#1fb894,#2fbfe0)",
]
# 图标统一用两字中文标签（用户规则：所有图标类元素均用两字，不用单字/小字）
SERVICE_GLYPH = {"patent":"专利","trademark":"商标","copyright":"版权","international":"涉外","litigation":"维权","project":"申报","operation":"托管"}

def build_index():
    def sector_card(s, i):
        return '''<a class="sector-card" href="/service-%s.html">
      <div class="sector-ico" style="background:%s">%s</div>
      <div class="sector-name">%s</div>
      <div class="sector-desc">%s</div>
      <span class="sector-more">了解详情</span>
    </a>''' % (s["id"], GRADS[i%len(GRADS)], SERVICE_GLYPH.get(s["id"], s["name"][0]), s["name"], s["desc"])
    # 上三下四，两行各自居中，卡片等大
    sector_top = "".join(sector_card(s, i) for i, s in enumerate(SERVICES[:3]))
    sector_bottom = "".join(sector_card(s, i) for i, s in enumerate(SERVICES[3:], start=3))
    advs = "".join('''<div class="adv-item"><div class="adv-icon adv-icon--2" style="background:%s">%s</div><h3>%s</h3><p>%s</p></div>''' % (GRADS[i%len(GRADS)], ["团队","方案","服务","效率","保障","协同"][i%6], t, d) for i,(t,d) in enumerate(ADVANTAGES))
    # 首页资讯展示3条非通知类文章，保持封面风格统一（通知公告由新闻中心/通知栏目呈现）
    home_news = [n for n in NEWS if n["cat"] != "通知公告"][:3]
    news = "".join('''<a class="news-card" href="/%s">
      <div class="news-card__img" style="background-image:url('/%s')"></div>
      <div class="news-card__body"><div class="news-meta"><span class="news-cat">%s</span><span>%s</span></div>
      <div class="news-card__title">%s</div><div class="news-card__desc">%s</div>
      <span class="news-card__more">阅读全文 →</span></div>
    </a>''' % (n["file"], n["cover"], n["cat"], n["date"], n["title"], n["desc"]) for n in home_news)
    body = '''
<section class="hero">
  <div class="hero-city"></div>
  <div class="container hero-inner">
  <div>
    <div class="hero-eyebrow">%s</div>
    <h1>守护创新<br><em>成就价值</em></h1>
    <p class="hero-lead">%s（简称莞促知产，官网 %s）是莞促集团旗下关联机构。我们拥有一批在专利申请、商标注册、高新认定、知识产权维权等方面资深的代理人团队，为企业提供一站式的知识产权与科技创新解决方案。</p>
    <div class="hero-btns">
      <a class="btn btn--gold btn--lg" href="/services.html">专业服务</a>
      <a class="btn btn--ghost btn--lg" href="/about.html">了解莞促</a>
    </div>
  </div>
  <div class="hero-visual">
    <div class="hero-ring"></div><div class="hero-ring two"></div>
    <div class="hero-badge"><img src="/assets/img/logo-blue.png" alt="莞促知产"></div>
    <span class="float-tag t1"><b>专利</b> · 商标 · 版权</span>
    <span class="float-tag t2">国家级<b>知识产权</b>服务</span>
    <span class="float-tag t3">一对一<b>专属顾问</b></span>
    <span class="float-tag t4">扎根东莞 · <b>服务湾区</b></span>
  </div>
</div></section>

<section class="stats"><div class="container stats-inner">
  <div class="stat"><div class="stat-num">7 大业务板块</div><div class="stat-label">确权 · 运用 · 保护 · 管理</div></div>
  <div class="stat"><div class="stat-num">一对一顾问</div><div class="stat-label">专属对接，全程跟进</div></div>
  <div class="stat"><div class="stat-num">当天申报</div><div class="stat-label">问题第一时间处理</div></div>
  <div class="stat"><div class="stat-num">莞促集团旗下</div><div class="stat-label">连锁运营，协同支撑</div></div>
</div></section>

<section class="section section--alt"><div class="container">
  <div class="section-head"><div class="section-kicker">Our Services</div>
    <h2 class="section-title">七大板块，护航创新全程</h2>
    <p class="section-sub">从确权、运用到保护、管理，专业分工协同推进，为企业构建完整的知识产权保护与价值实现体系。</p>
  </div>
  <div class="sector-rows">
    <div class="sector-row sector-row--top">%s</div>
    <div class="sector-row sector-row--bottom">%s</div>
  </div>
</div></section>

<section class="section section--alt"><div class="container">
  <div class="section-head"><div class="section-kicker">Why Us</div>
    <h2 class="section-title">为什么选择莞促知产</h2>
    <p class="section-sub">专业团队、规范流程、严格保密，以长期服务陪伴企业成长。</p>
  </div>
  <div class="adv-grid">%s</div>
</div></section>

<section class="section"><div class="container">
  <div class="section-head"><div class="section-kicker">News</div>
    <h2 class="section-title">近期资讯</h2>
    <p class="section-sub">政策法规、专业解读与行业动态，持续为企业传递知识产权领域的有用信息。</p>
  </div>
  <div class="news-grid">%s</div>
  <div style="text-align:center;margin-top:34px"><a class="btn btn--outline" href="/news.html">查看全部资讯 →</a></div>
</div></section>

<section class="cta"><div class="container cta-inner">
  <h2>让 <em>知识产权</em> 成为企业增长的护栏</h2>
  <p>无论是确权申请、维权保护，还是科技项目申报，欢迎与我们沟通需求。</p>
  <div class="cta-btns">
    <a class="btn btn--gold btn--lg" href="/contact.html">业务咨询</a>
    <a class="btn btn--ghost btn--lg" href="/process.html">了解服务流程</a>
  </div>
</div></section>
''' % (LOC, BRAND, BASE, sector_top, sector_bottom, advs, news)
    write("index.html", page(
        *seo("index"), "", body, active="index", jsonld=org_jsonld()))

# ============ 关于莞促 ============
def build_about():
    body = ph("关于莞促", "了解我们的定位、团队与服务理念", "ABOUT US") + '''
<div class="container" style="padding-top:36px;padding-bottom:80px">
  <div class="content-block">
    <h2>事务所简介</h2>
    <div class="lead-box">广东莞促知识产权代理事务所（普通合伙），简称莞促知产，官方网站 %s，是莞促集团旗下关联的公司，在集团管理下实行连锁运营，下设 8 家分公司及 1 家自主产权科技孵化器。</div>
    <p>我们拥有一批在专利申请、商标注册、高新认定、知识产权维权等方面资深的强大专业代理人团队，为客户提供一站式的解决方案。</p>
    <p>所有知识产权案件当天申报，涉及相关问题在第一时间处理，提供一对一顾问服务，并具备完善的售后保障体系。严格遵守执业道德，忠诚执业信仰，公司建立有严格的保密体系，与客户之间所有业务均签订规范的保密协议。</p>
  </div>
  <div class="content-block">
    <h2>主体名称说明</h2>
    <p>本站为广东莞促知识产权代理事务所（普通合伙）官方网站，对外简称莞促知产，域名为 %s。事务所专注于专利代理、商标代理、版权登记、涉外知识产权、维权与法律、科技项目申报及知产运营托管服务，与企业服务、财税及产业投资等其他集团业务分属不同主体。</p>
    <p>名称相近的莞促（广东）知识产权代理有限公司、东莞市莞促知识产权代理有限公司为其他市场主体，与本站所属事务所并非同一机构。企业在办理知识产权业务时，请以本站公布的机构名称、联系方式与办公地址为准，避免混淆。</p>
  </div>
  <div class="content-block">
    <h2>服务网络</h2>
    <p>依托集团连锁运营体系，事务所下设 8 家分公司及 1 家自主产权科技孵化器，形成覆盖多地的服务网络，为湾区企业提供贴近、便捷的知识产权服务。</p>
    <div class="card-grid" style="margin-top:18px">
      <div class="mini-card"><div class="mi">8</div><h4>家分公司</h4><p>连锁运营，就近服务</p></div>
      <div class="mini-card"><div class="mi">1</div><h4>家科技孵化器</h4><p>自主产权，产业协同</p></div>
      <div class="mini-card"><div class="mi">1:1</div><h4>专属顾问</h4><p>一对一对接服务</p></div>
      <div class="mini-card"><div class="mi">全天</div><h4>当天申报</h4><p>问题第一时间处理</p></div>
    </div>
  </div>
  <div class="content-block">
    <h2>我们的承诺</h2>
    <ul>
      <li>严格遵守执业道德，忠诚执业信仰，规范执业。</li>
      <li>对商业信息、公司信息、专利信息严格保密，签订规范保密协议。</li>
      <li>案件当天申报，相关问题第一时间响应处理。</li>
      <li>一对一顾问服务，配套完善的售后保障体系。</li>
    </ul>
  </div>
</div>''' % (BASE, BASE)
    write("about.html", page(*seo("about"), "about.html", body, active="about", jsonld=web_page_jsonld("关于莞促", "事务所简介与服务理念", "about.html", "AboutPage")))

def build_group():
    body = ph("莞促集团", "扎根东莞，与产业共同成长", "GUANCU GROUP") + '''
<div class="container" style="padding-top:36px;padding-bottom:80px">
  <div class="content-block">
    <h2>集团概览</h2>
    <p>莞促集团（www.guancu.com）从企业事务代理起步，已形成覆盖企业服务、财税工商、知识产权、数字科技、产业投资与教育文旅的协同格局，以多家成员与投资企业，为湾区企业提供全周期专业支持。</p>
    <p>集团秉持“扎根东莞，与产业共同成长”的发展理念，主张“把专业做深，把协同做实”，围绕企业经营的真实需求组织能力，以持续服务陪伴企业成长。</p>
  </div>
  <div class="content-block">
    <h2>六大业务板块</h2>
    <div class="card-grid">
      <div class="mini-card"><div class="mi mi--2">总部</div><h4>企业总部管理与咨询</h4><p>集团管控、组织设计与经营顾问</p></div>
      <div class="mini-card"><div class="mi mi--2">财税</div><h4>财税与工商服务</h4><p>注册记账、审计税筹与资质代办</p></div>
      <div class="mini-card"><div class="mi mi--2">知产</div><h4>知识产权与科技申报</h4><p>商标专利、著作权与项目申报</p></div>
      <div class="mini-card"><div class="mi mi--2">数科</div><h4>数字科技与大数据</h4><p>数据服务、软件开发与系统集成</p></div>
      <div class="mini-card"><div class="mi mi--2">投资</div><h4>产业投资与园区运营</h4><p>产业投资、园区管理与新能源</p></div>
      <div class="mini-card"><div class="mi mi--2">文旅</div><h4>教育与文旅发展</h4><p>教育投资、文旅运营与传媒</p></div>
    </div>
  </div>
  <div class="content-block">
    <h2>我们的定位</h2>
    <p>广东莞促知识产权代理事务所是集团“知识产权与科技申报”板块的专业承接平台。依托集团的资源与协同优势，我们专注于知识产权的确权、运用、保护与管理，并与集团财税、工商、科技服务等领域形成协同，为客户提供更完整的解决方案。</p>
    <div style="text-align:center;margin-top:22px"><a class="btn btn--primary" href="https://www.guancu.com/" target="_blank" rel="noopener">访问莞促集团官网 →</a></div>
  </div>
</div>'''
    write("group.html", page(*seo("group"), "group.html", body, active="about", jsonld=web_page_jsonld("莞促集团", "集团概览与业务板块", "group.html", "AboutPage")))

def build_culture():
    cult = "".join('''<div class="cult-card"><div class="cc-label">%s</div><div class="cc-main">%s</div></div>''' % p for p in [
        ("事务所定位 POSITION", CULTURE["position"]),
        ("服务宗旨 PURPOSE", CULTURE["purpose"]),
        ("使命 MISSION", CULTURE["mission"]),
        ("愿景 VISION", CULTURE["vision"]),
    ])
    vals = "".join('''<div class="value-item"><div class="v-name">%s</div><div class="v-desc">%s</div></div>''' % p for p in CULTURE["values"])
    body = ph("企业文化", "与莞促集团一脉相承的价值主张", "CULTURE") + '''
<div class="container" style="padding-top:36px;padding-bottom:80px">
  <div class="lead-box" style="text-align:center">承接莞促集团“扎根东莞，与产业共同成长”的发展理念与“把专业做深，把协同做实”的务实精神，形成以专业、诚信、协同、长期为核心的文化基调。</div>
  <div class="cult-grid" style="margin-bottom:28px">%s</div>
  <div class="section-head" style="margin-bottom:22px"><h2 class="section-title" style="font-size:26px">核心价值观</h2></div>
  <div class="values-grid">%s</div>
  <div class="content-block" style="margin-top:28px;text-align:center">
    <h2 style="border:none;padding:0">企业精神</h2>
    <p style="font-size:22px;color:var(--gold-500);font-weight:700">%s</p>
  </div>
</div>''' % (cult, vals, CULTURE["spirit"])
    write("culture.html", page(*seo("culture"), "culture.html", body, active="about", jsonld=web_page_jsonld("企业文化", "企业文化与价值主张", "culture.html", "AboutPage")))

def build_team():
    items = [("团队", "专业代理人团队", "覆盖专利、商标、版权等领域，具备扎实的专业能力与实务经验。"),
             ("专利", "专利代理专家", "擅长专利挖掘、撰写与审查意见答复，处理复杂专利事务。"),
             ("商标", "商标版权顾问", "专注商标确权、异议复审与版权登记，熟悉审查实践。"),
             ("申报", "项目申报顾问", "熟悉高企认定、贯标等政策，辅导企业高效申报。"),
             ("涉外", "涉外服务团队", "对接 PCT、马德里体系，支持企业海外知识产权布局。"),
             ("客服", "客户服务员", "一对一跟进案件进度，及时同步关键节点信息。")]
    cards = "".join('''<div class="mini-card"><div class="mi mi--2">%s</div><h4>%s</h4><p>%s</p></div>''' % item for item in items)
    body = ph("专业团队", "专业分工，对口服务每一项业务", "OUR TEAM") + '''
<div class="container" style="padding-top:36px;padding-bottom:80px">
  <div class="content-block">
    <h2>团队构成</h2>
    <p>我们拥有一批在专利申请、商标注册、高新认定、知识产权维权等方面资深的强大专业代理人团队。依托专业分工机制，按业务类型匹配对应团队，让每一项业务都获得专业的处理。</p>
    <div class="card-grid" style="margin-top:20px">%s</div>
  </div>
  <div class="content-block">
    <h2>服务方式</h2>
    <ul>
      <li>专家级顾问一对一服务，明确对接人与沟通机制。</li>
      <li>案件当天申报，关键节点主动同步。</li>
      <li>严格保密，签订规范保密协议。</li>
      <li>配套完善售后保障体系，交付后持续跟进。</li>
    </ul>
  </div>
</div>''' % cards
    write("team.html", page(*seo("team"), "team.html", body, active="about", jsonld=web_page_jsonld("专业团队", "团队构成与服务方式", "team.html", "AboutPage")))

def build_honors():
    cards = "".join('''<div class="mini-card"><div class="mi mi--2">%s</div><h4>%s</h4><p>专业资质与行业认可</p></div>''' % (h[:2], h) for h in HONORS)
    body = ph("荣誉资质", "规范执业，诚信经营", "HONORS") + '''
<div class="container" style="padding-top:36px;padding-bottom:80px">
  <div class="content-block">
    <h2>公司资质</h2>
    <p>我们在传承中发展，在感恩中前行。事务所持有专利代理机构执业许可，并为行业协会会员单位，连续获得多项信用与诚信类认定。</p>
    <div class="card-grid" style="margin-top:20px">%s</div>
  </div>
  <div class="content-block">
    <h2>合作与认可</h2>
    <p>%s。我们将继续以规范执业和诚信服务，为客户创造长期价值。</p>
  </div>
</div>''' % (cards, PARTNERS_NOTE)
    write("honors.html", page(*seo("honors"), "honors.html", body, active="about", jsonld=web_page_jsonld("荣誉资质", "专业资质与行业认可", "honors.html", "AboutPage")))

# ============ 专业服务总览 ============
def build_services():
    sectors = "".join('''<a class="sector-card" href="/service-%s.html">
      <div class="sector-ico" style="background:%s">%s</div>
      <div class="sector-name">%s</div>
      <div class="sector-desc">%s</div>
      <span class="sector-more">查看服务</span></a>''' % (s["id"], GRADS[i%len(GRADS)], SERVICE_GLYPH.get(s["id"], s["name"][0]), s["name"], s["desc"]) for i,s in enumerate(SERVICES))
    list_items = [{"@type":"ListItem","position":i+1,"name":s["name"],"url":BASE+"/service-"+s["id"]+".html"} for i,s in enumerate(SERVICES)]
    ld = {"@context":"https://schema.org","@type":"ItemList","itemListElement":list_items,"name":"莞促知产专业服务"}
    body = ph("专业服务", "从确权到维权，从申报到运营的全链条服务", "OUR SERVICES") + '''
<div class="container" style="padding-top:36px;padding-bottom:80px">
  <div class="lead-box">以客户需求和产品发展理念为驱动力，围绕知识产权的创造、运用、保护与管理，形成七大专业服务板块，为企业提供一站式解决方案。</div>
  <div class="sector-grid">%s</div>
  <div class="content-block" style="margin-top:28px">
    <h2>东莞本地服务</h2>
    <ul>%s</ul>
  </div>
  <div class="content-block" style="margin-top:28px;text-align:center">
    <h2 style="border:none;padding:0">需要哪方面的帮助？</h2>
    <p>欢迎说明业务类型与企业情况，我们将匹配专业团队与您对接。</p>
    <a class="btn btn--gold" href="/contact.html" style="margin-top:10px">立即咨询 →</a>
  </div>
</div>''' % (sectors, "".join('<li><a href="/%s">%s</a></li>' % (c["file"], c["kw"]) for c in CITY_PAGES))
    write("services.html", page(*seo("services"), "services.html", body, active="services", jsonld=ld))

def build_service_detail(s):
    items = "".join('''<div class="item-card"><h4>%s</h4><p>%s</p></div>''' % p for p in s["items"])
    others = "".join('''<a class="sector-card" href="/service-%s.html" style="padding:22px"><div class="sector-ico" style="width:48px;height:48px;border-radius:15px;font-size:20px;background:%s">%s</div><div class="sector-name" style="font-size:17px">%s</div></a>''' % (o["id"], GRADS[i%len(GRADS)], SERVICE_GLYPH.get(o["id"], o["name"][0]), o["name"]) for i,o in enumerate(SERVICES) if o["id"] != s["id"])
    body = ph(s["name"], s["desc"], s["en"]) + '''
<div class="container" style="padding-top:36px;padding-bottom:80px">
  <div class="content-block">
    <h2>服务概述</h2>
    <p>%s</p>
    <p>%s</p>
  </div>
  <div class="content-block">
    <h2>服务内容</h2>
    <div class="item-list">%s</div>
  </div>
  <div class="content-block">
    <h2>服务流程</h2>
    <p>需求沟通 → 方案梳理 → 资料准备 → 服务实施 → 交付跟进。专业团队全程对接，关键节点及时同步。</p>
    <div style="text-align:center;margin-top:16px"><a class="btn btn--outline" href="/process.html">查看完整服务流程 →</a></div>
  </div>
  <div class="section-head" style="margin:34px 0 22px"><h2 class="section-title" style="font-size:26px">其他服务</h2></div>
  <div class="sector-grid">%s</div>
</div>''' % (s["desc"], s["short"]+"。", items, others)
    fn = "service-"+s["id"]+".html"
    st, sd, sk = SERVICE_SEO[s["id"]]
    write(fn, page(st, sd, sk, fn, body, active="services", jsonld=web_page_jsonld(s["name"], s["desc"], fn, "ServicePage")))

# ============ 东莞地域核心词落地页 ============
def build_city_pages():
    for c in CITY_PAGES:
        blocks = []
        for title, paras in c["sections"]:
            ps = "".join("<p>%s</p>" % p for p in paras)
            blocks.append('<div class="content-block"><h2>%s</h2>%s</div>' % (title, ps))
        blocks_html = "".join(blocks)
        faq_items = "".join(
            '<div class="faq-item"><div class="faq-q"><span class="qmark">问</span><span>%s</span></div><div class="faq-a"><strong>答：</strong>%s</div></div>' % (q, a)
            for q, a in c["faqs"]
        )
        related = "".join(
            '<li><a href="/%s">%s</a></li>' % (o["file"], o["kw"])
            for o in CITY_PAGES if o["file"] != c["file"]
        )
        body = ph(c["kw"], c["service"], "DONGGUAN SERVICE") + '''
<div class="container" style="padding-top:36px;padding-bottom:80px">
  <div class="lead-box">%s</div>
  %s
  <div class="content-block">
    <h2>常见问题</h2>
    %s
  </div>
  <div class="content-block">
    <h2>相关服务</h2>
    <ul>%s</ul>
    <div style="text-align:center;margin-top:18px">
      <a class="btn btn--gold" href="/contact.html">咨询 %s →</a>
    </div>
  </div>
</div>''' % (c["lead"], blocks_html, faq_items, related, c["kw"])
        # Service + LocalBusiness 结构化数据，标注东莞本地服务属性与 FAQ
        ld = {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "Service",
                    "name": c["service"],
                    "serviceType": c["kw"],
                    "description": c["desc"],
                    "provider": {"@type": "Organization", "name": BRAND, "url": BASE + "/"},
                    "areaServed": {"@type": "AdministrativeArea", "name": "东莞市"},
                    "url": BASE + "/" + c["file"],
                },
                {
                    "@type": "FAQPage",
                    "mainEntity": [
                        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                        for q, a in c["faqs"]
                    ],
                },
            ],
        }
        write(c["file"], page(c["title"], c["desc"], c["keywords"], c["file"], body,
                              active="services", jsonld=ld))

# ============ 服务流程 ============
def build_process():
    steps = "".join('''<div class="step"><div class="step-num">%s</div><h3>%s</h3><p>%s</p></div>''' % p for p in PROCESS)
    body = ph("服务流程", "从一次沟通，到长期同行", "SERVICE PROCESS") + '''
<div class="container" style="padding-top:36px;padding-bottom:80px">
  <div class="content-block"><h2>五步服务流程</h2>
    <div class="process" style="margin-top:24px">%s</div></div>
  <div class="content-block">
    <h2>服务保障</h2>
    <ul>
      <li>专家级顾问一对一服务，明确对接人与响应机制。</li>
      <li>案件当天申报，涉及问题第一时间处理。</li>
      <li>商业信息、公司信息、专利信息严格保密，签订规范保密协议。</li>
      <li>完善的售后保障体系，交付后持续跟进。</li>
    </ul>
  </div>
</div>''' % steps
    write("process.html", page(*seo("process"), "process.html", body, active="process", jsonld=web_page_jsonld("服务流程", "五步服务流程与服务保障", "process.html")))

# ============ 新闻资讯 ============
def news_listing(title, sub, en, items, fn, active, cats=None):
    cards = "".join('''<a class="news-card" href="/%s">
      <div class="news-card__img" style="background-image:url('/%s')"></div>
      <div class="news-card__body"><div class="news-meta"><span class="news-cat">%s</span><span>%s</span></div>
      <div class="news-card__title">%s</div><div class="news-card__desc">%s</div>
      <span class="news-card__more">阅读全文 →</span></div></a>''' % (n["file"], n["cover"], n["cat"], n["date"], n["title"], n["desc"]) for n in items)
    body = ph(title, sub, en) + '''
<div class="container" style="padding-top:36px;padding-bottom:80px">
  <div class="news-grid">%s</div>
</div>''' % cards
    key = fn.replace(".html", "")
    write(fn, page(*seo(key), fn, body, active=active, jsonld=web_page_jsonld(title, sub, fn, "CollectionPage")))

def build_news():
    # 统一资讯中心：一个栏目发布通知公告、政策速递、事务所动态、知产课堂等文章，带分类筛选与分页
    cards = "".join('''<a class="news-card" href="/%s" data-cat="%s">
      <div class="news-card__img" style="background-image:url('/%s')"></div>
      <div class="news-card__body"><div class="news-meta"><span class="news-cat">%s</span><span>%s</span></div>
      <div class="news-card__title">%s</div><div class="news-card__desc">%s</div>
      <span class="news-card__more">阅读全文 →</span></div></a>''' % (n["file"], n["cat"], n["cover"], n["cat"], n["date"], n["title"], n["desc"]) for n in NEWS)
    cats = ["全部"] + list(dict.fromkeys(n["cat"] for n in NEWS))
    tabs = "".join('<span class="news-tab%s" data-filter="%s">%s</span>' % (" active" if c=="全部" else "", c, c) for c in cats)
    body = ph("新闻资讯", "通知公告、政策速递、事务所动态与专业知识解读", "NEWS & INSIGHTS") + '''
<div class="container" style="padding-top:36px;padding-bottom:80px">
  <div class="news-tabs">%s</div>
  <div class="news-grid" id="newsGrid">%s</div>
  <div class="news-pager" id="newsPager" aria-label="资讯分页"></div>
</div>
<script>
(function(){
  var pageSize=9;
  var tabs=Array.prototype.slice.call(document.querySelectorAll('.news-tab'));
  var cards=Array.prototype.slice.call(document.querySelectorAll('#newsGrid .news-card'));
  var pager=document.getElementById('newsPager');
  var grid=document.getElementById('newsGrid');
  var filter='全部';
  var current=1;
  function visibleCards(){
    return cards.filter(function(c){
      return filter==='全部'||c.getAttribute('data-cat')===filter;
    });
  }
  function render(){
    var list=visibleCards();
    var total=Math.max(1,Math.ceil(list.length/pageSize));
    if(current>total) current=total;
    cards.forEach(function(c){c.style.display='none'});
    list.slice((current-1)*pageSize,current*pageSize).forEach(function(c){c.style.display=''});
    var html='<button class="pager-btn" data-page="'+(current-1)+'"'+(current===1?' disabled':'')+'>上一页</button>';
    for(var i=1;i<=total;i++){
      html+='<button class="pager-btn'+(i===current?' is-active':'')+'" data-page="'+i+'">'+i+'</button>';
    }
    html+='<button class="pager-btn" data-page="'+(current+1)+'"'+(current===total?' disabled':'')+'>下一页</button>';
    pager.innerHTML=html;
    Array.prototype.slice.call(pager.querySelectorAll('.pager-btn')).forEach(function(b){
      b.addEventListener('click',function(){
        if(b.disabled) return;
        current=parseInt(b.getAttribute('data-page'),10);
        render();
        var anchor=document.querySelector('.news-tabs');
        var y=anchor.getBoundingClientRect().top+window.pageYOffset-130;
        window.scrollTo({top:y<0?0:y,behavior:'smooth'});
      });
    });
  }
  tabs.forEach(function(t){
    t.addEventListener('click',function(){
      tabs.forEach(function(x){x.classList.remove('active')});
      t.classList.add('active');
      filter=t.getAttribute('data-filter');
      current=1;
      render();
    });
  });
  render();
})();
</script>''' % (tabs, cards)
    write("news.html", page(*seo("news"), "news.html", body, active="news", jsonld=web_page_jsonld("新闻资讯", "通知公告、政策与专业知识资讯", "news.html", "CollectionPage")))

    news_listing("通知公告", "本所服务通知与重要事项公告", "NOTICE", [n for n in NEWS if n["cat"]=="通知公告"] or NEWS[:2], "notice.html", "news")
    news_listing("知产课堂", "用通俗的方式讲清专业知识", "IP CLASSROOM", [n for n in NEWS if n["cat"]=="知产课堂"] or NEWS[:3], "knowledge.html", "news")
    news_listing("政策速递", "及时传递知识产权与科技政策要点", "POLICY", [n for n in NEWS if n["cat"]=="政策速递"] or NEWS[:3], "policy.html", "news")

# 文章正文（按文章标题提供贴合内容；键为文件名，未提供则用通用模板）
# 文章 → 东莞地域落地页内链映射（集中主关键词权重）
CITY_LINK_BY_ARTICLE = {
    # 商标类 → 东莞商标注册
    "news/n44.html": ("dongguan-shangbiao-zhuce.html", "东莞商标注册"),
    "news/n45.html": ("dongguan-zhuanli-shenqing.html", "东莞专利申请"),
    "news/n46.html": ("dongguan-zhuanli-shenqing.html", "东莞专利申请"),
    "news/n41.html": ("dongguan-shangbiao-zhuce.html", "东莞商标注册"),
    "news/n43.html": ("dongguan-shangbiao-zhuce.html", "东莞商标注册"),
    "news/n42.html": ("dongguan-zhishichanquan.html", "东莞知识产权"),
    "news/n40.html": ("dongguan-shangbiao-zhuce.html", "东莞商标注册"),
    "news/n19.html": ("dongguan-shangbiao-zhuce.html", "东莞商标注册"),
    "news/n34.html": ("dongguan-shangbiao-zhuce.html", "东莞商标注册"),
    "news/n35.html": ("dongguan-shangbiao-zhuce.html", "东莞商标注册"),
    "news/n36.html": ("dongguan-shangbiao-zhuce.html", "东莞商标注册"),
    "news/n11.html": ("dongguan-shangbiao-zhuce.html", "东莞商标注册"),
    "news/n14.html": ("dongguan-shangbiao-zhuce.html", "东莞商标注册"),
    "news/n28.html": ("dongguan-shangbiao-zhuce.html", "东莞商标注册"),
    "news/n27.html": ("dongguan-shangbiao-zhuce.html", "东莞商标注册"),
    # 专利类 → 东莞专利申请
    "news/n20.html": ("dongguan-zhuanli-shenqing.html", "东莞专利申请"),
    "news/n29.html": ("dongguan-zhuanli-shenqing.html", "东莞专利申请"),
    "news/n37.html": ("dongguan-zhuanli-shenqing.html", "东莞专利申请"),
    "news/n38.html": ("dongguan-zhuanli-shenqing.html", "东莞专利申请"),
    "news/n05.html": ("dongguan-zhuanli-shenqing.html", "东莞专利申请"),
    "news/n08.html": ("dongguan-zhuanli-shenqing.html", "东莞专利申请"),
    "news/n10.html": ("dongguan-zhuanli-shenqing.html", "东莞专利申请"),
    # 布局/高企/综合类 → 东莞知识产权
    "news/n24.html": ("dongguan-zhishichanquan.html", "东莞知识产权"),
    "news/n30.html": ("dongguan-zhishichanquan.html", "东莞知识产权"),
    "news/n23.html": ("dongguan-zhishichanquan.html", "东莞知识产权"),
    "news/n22.html": ("dongguan-zhishichanquan.html", "东莞知识产权"),
    "news/n25.html": ("dongguan-zhishichanquan.html", "东莞知识产权"),
    "news/n31.html": ("dongguan-zhishichanquan.html", "东莞知识产权"),
    "news/n32.html": ("dongguan-zhishichanquan.html", "东莞知识产权"),
    "news/n33.html": ("dongguan-zhishichanquan.html", "东莞知识产权"),
    "news/n39.html": ("dongguan-zhishichanquan.html", "东莞知识产权"),
}

ARTICLE_BODIES = {
    "news/n44.html": [
        "商标续展这件事，平时很少被想起，真到需要时却容易手忙脚乱。有的企业忙着换包装、扩渠道，把续展节点错过了；有的企业提交申请后才发现主体名称与登记信息不一致，来回补正。商标是有期限的权利，想继续用下去，就要按规定办理续展。莞促知产把办理顺序和常见注意点讲清楚。",
        "一、先弄清续展是什么",
        "商标注册成功后，专用权有法定的有效期限。期限届满前，注册人可以按程序申请续展，经核准后继续享有商标专用权。续展不是重新申请一件新商标，而是延长原有注册的权利期限，因此通常与原注册号、原核定类别和项目直接对应。企业应把续展视为品牌资产管理中的固定动作，而不是临时补救。",
        "二、第一步：提前核对权利状态",
        "办理前先做一次核对：商标注册证上的主体名称、地址是否与当前营业执照一致；核定使用的类别和项目是否覆盖现在实际经营的业务；是否存在地址变更、名义变更尚未登记的情况；是否收到过异议、无效或撤销相关通知。信息不一致会影响续展受理，类别项目不足则意味着某些实际使用并未被覆盖，可以借续展契机一并规划补充注册。",
        "三、第二步：准备申请材料",
        "通常需要提交续展注册申请书、申请人身份证明材料；委托代理机构办理的，还需提供代理委托书。申请信息要与商标局登记记录保持一致，尤其是注册人名称和地址。如果企业名称已经变更但商标记录未同步，应先办理变更手续，再办续展，避免申请被要求补正。",
        "四、第三步：提交与审查",
        "材料准备齐全后，按规定渠道提交申请。受理后会进入审查环节，审查通过后予以核准并公告，企业取得续展证明。实务中要留意通知信息，收到补正要求时按要求及时修改。把主体信息、类别项目和送达方式提前核对好，通常能减少来回修改，让续展顺利落地。",
        "五、常见的退回与补正原因",
        "比较常见的情况有：申请书填写的注册信息与登记记录不一致；主体名称变更后未先办变更；委托手续不完整；遗漏需一并办理的类别；联系方式失效导致通知收不到。这些问题大多源于前期核对不细，而不是续展本身复杂。按清单逐项对照，基本都能避开。",
        "六、续展之后还要做什么",
        "拿到续展证明，建议与商标注册证一并归档，并在品牌台账中更新权利期限。同时留存实际使用证据，如带有商标的产品包装、销售凭证、广告宣传材料，这些材料在日后应对撤销或侵权争议时很有价值。对业务已经扩展的企业，还可以借机评估关联类别、防御类别是否需要补充布局。",
        "七、莞促知产能提供哪些帮助",
        "莞促知产扎根东莞松山湖，可协助企业梳理商标权利状态、核对主体与类别信息、准备续展材料，并在商标变更、补充注册、监测与维权等方面提供持续支持。对企业名下多件商标的情况，也可以建立统一台账，把续展节点管理起来。",
        "写在最后",
        "商标续展的关键是提前核对、按序办理、留好凭证。品牌做起来不容易，别让权利期限成为被忽略的缺口。有续展或商标管理需求的企业，欢迎与莞促知产交流。",
    ],
    "news/n45.html": [
        "企业花精力研发出来的技术，投放市场后发现别人也在生产类似产品，甚至卖得比自己还快。这时候最怕两种反应：一是凭感觉认定对方侵权，匆忙投诉；二是觉得维权太麻烦，干脆不了了之。专利维权有它的判断逻辑和推进顺序。莞促知产按流程讲清楚，帮企业把第一步走对。",
        "一、第一步：核查自己的权利是否稳固",
        "维权之前先向内看：专利是否有效、年费是否按规定缴纳、权利状态有没有终止或质押等异常；更关键的是看权利要求的保护范围是否清楚、是否经得起无效宣告的检验。如果专利本身稳定性不足，贸然发起投诉或诉讼，反而可能被对方反制。把权利底牌摸清，是维权的基本功。",
        "二、第二步：做侵权比对",
        "判断他人产品是否落入保护范围，要把被诉产品与专利权利要求逐项比对。发明和实用新型通常看技术方案是否覆盖了权利要求的全部技术特征；外观设计则看整体视觉效果是否近似。比对时要针对具体产品、具体型号，而不是凭宣传图或口头描述下结论。技术细节复杂的，可借助专业人员出具比对意见。",
        "三、第三步：把证据固定下来",
        "专利维权的证据通常包括被诉产品实物、购买凭证、网页与店铺页面、宣传资料、生产与销售规模线索等。线上销售建议完整保存链接、页面和交易记录，必要时通过可信方式保全；线下购买要注意过程记录和实物封存。证据固定越及时、越完整，后面的协商、投诉与诉讼越有支撑。",
        "四、第四步：选择维权路径",
        "常见选择包括：与对方协商许可或停止侵权；向电商平台提交专利侵权投诉，要求下架相关链接；向管理专利工作的部门请求行政处理；向人民法院提起侵权诉讼，主张停止侵权与赔偿。几条路径可以组合使用，例如先平台投诉止损，再通过行政或诉讼解决赔偿问题。选哪条，要看证据强度、对方规模和企业目标。",
        "五、留意对方可能的抗辩",
        "被诉方常见主张包括：技术属于现有技术、自己享有先用权、产品具有合法来源、与专利技术方案并不相同，或者对专利提出无效宣告。企业应在行动前预判这些抗辩方向，准备好相应材料。提前做过专利检索与无效风险评估的产品，应对起来会从容许多。",
        "六、莞促知产能提供哪些帮助",
        "莞促知产扎根东莞松山湖，可协助企业核查专利权利状态、开展侵权比对分析、整理证据清单、制定维权路径，并在专利无效应对、行政处理与诉讼衔接等环节提供专业支持。对尚未建立保护体系的企业，也会同步给出专利布局与监测建议。",
        "写在最后",
        "专利维权的顺序是：先核查权利，再做比对，然后固定证据，最后选择路径。把这几步做扎实，维权才有胜算。发现疑似侵权行为的企业，欢迎与莞促知产交流，由专业顾问结合技术方案和证据情况提供初步评估。",
    ],
    "news/n46.html": [
        "外观专利看起来门槛不高，实际提交的图片五花八门：有的背景杂乱、有的角度缺失、有的把商标和文字一起拍进图里。结果不是补正，就是授权后保护范围模糊，别人稍作改动就绕开了。外观专利保护的是产品外形，图片就是权利边界本身。莞促知产讲清图片和材料的准备要点。",
        "一、先明确外观专利保护什么",
        "外观设计保护的是产品的形状、图案、色彩或者其结合所作出的富有美感并适于工业应用的新设计。它不保护产品的功能、技术效果，也不保护品牌名称。因此申请前应确认：真正想保护的是产品外形，还是技术方案或品牌标识。三者对应的申请路径不同，选错方向会浪费时间和预算。",
        "二、视图要成体系，不能只给一个角度",
        "申请通常需要提交能够清楚显示设计要点的成套视图，一般包括正、背、左、右、顶、底等角度的视图以及立体图。哪些角度必须提交，取决于产品类型和设计要点所在。如果设计要点集中在某一面，就要保证该面清晰完整；如果产品是立体造型，各视图之间要相互对应、前后一致。缺角度或视图相互矛盾，是常见的补正原因。",
        "三、拍摄与绘制的规范要求",
        "图片应清晰、背景干净、光线均匀，避免阴影、反光和透视变形；产品边缘轮廓要完整，不要被道具遮挡。图中不宜出现与外观无关的商标、文字、水印或价格标签，除非这些元素本身就是设计要点并已说明。提交彩色图片的，色彩要真实稳定；不要求保护颜色的，应按规定提交相应图样。缩放比例也要合适，缩小后仍能看清设计细节。",
        "四、设计要点与简要说明怎么写",
        "简要说明用于解释图片、指明设计要点，并说明是否存在色彩保护、是否请求保护某一局部等事项。写法要客观克制，与图片显示的内容一致，不要用宣传性语言描述产品效果。设计要点应当指向具体的形状或图案特征，而不是笼统写“造型美观”。一份清楚的简要说明，能帮助审查员和后续实施方准确理解保护范围。",
        "五、提交前的自查清单",
        "逐项核对：视图是否覆盖必要角度；各视图是否一致；图片是否清晰、背景是否干净；是否带入无关标识；简要说明与图片是否对应；申请人信息是否与证照一致；委托手续是否完整。涉及成套产品的，还要确认是否应作为一件申请提出。把这些细节做好，申请过程会顺畅很多。",
        "六、莞促知产能提供哪些帮助",
        "莞促知产扎根东莞松山湖，可协助企业判断产品是否适合申请外观专利、梳理需要提交的角度、规范图片与简要说明的表述，并在专利检索、申请提交和后续维权环节提供专业支持。对同时涉及结构创新与外形设计的产品，我们会从发明、实用新型与外观组合保护的角度给出建议。",
        "写在最后",
        "外观专利的图片不是随便拍几张就能用，它直接决定保护范围是否清楚。提前按规范准备，授权后的权利才扎实。有外观专利申请需求的企业，欢迎与莞促知产交流。",
    ],
    "news/n41.html": [
        "在电商平台上看到自家商标被人用在相似商品上，或在线下门店发现包装、店招“长得几乎一样”，很多企业的第一反应是生气，第二反应是不知道该从哪一步开始。商标维权不是发一封律师函就结束，而是一套从判断、取证到路径选择的工作。莞促知产把常见流程讲清楚，帮企业少走弯路。",
        "一、先判断：这是不是商标意义上的侵权",
        "发现相似标识，先别急着下结论。判断通常看几件事：对方使用的标识与你的注册商标是否相同或近似；使用的商品或服务是否相同或类似；这种使用是不是作为商标来识别商品来源；会不会让相关公众产生混淆。此外还要留意对方是否提出在先使用、正当使用等抗辩。把这几项逐一对照，才能确定值不值得投入维权资源。",
        "二、第一步：把证据固定下来",
        "维权的基础是证据。网页、店铺链接、商品页面、宣传物料、交易记录、发货单、票据，都应系统保存。线上侵权建议对页面完整截图并记录访问路径，必要时通过可信方式保全，避免对方下架后无据可查。线下发现侵权商品，应注意购买过程与实物封存，保留销售凭证。证据越完整，后面的投诉、答辩和索赔越有底气。",
        "三、第二步：看清自己的权利底牌",
        "维权前先核对商标注册证：核定使用的类别和项目是什么、商标图样是否与实际使用一致、登记的主体名称与地址是否有变更、续展是否办理。权利状态有瑕疵，会直接影响案件走向。如果企业实际使用的标识与注册图样差别较大，还要评估该标识本身的保护力度。",
        "四、第三步：选择适合的维权路径",
        "常见路径有几条：与对方协商，要求停止使用并赔偿；向市场监督管理部门投诉，借助行政力量查处；向电商平台提交知识产权投诉，要求下架链接；向人民法院提起侵权诉讼，主张停止侵权与赔偿。几条路径并不互斥，实务中经常是平台下架、行政投诉与民事诉讼相互衔接。选哪条，取决于侵权规模、证据强度、对方态度和企业目标。",
        "五、第四步：行政投诉与诉讼怎么衔接",
        "行政投诉的优势是处理节奏较快，适合制止正在发生的侵权行为；诉讼的优势在于可以主张赔偿、形成具有执行力的结果。需要注意，行政程序中形成的调查材料、询问笔录、查处决定，往往可以成为后续诉讼的重要证据。企业若计划两条路一起走，应提前统一事实陈述与证据口径，避免前后不一致。",
        "六、企业容易忽略的几个问题",
        "其一，只盯着仿冒成品，忽略生产源头与销售渠道，治标不治本。其二，把维权当成一次性行动，没有把监测做成常态，过一段时间又出现新链接。其三，索赔主张缺乏依据，没有提前整理销售数据、许可费、维权支出等材料。其四，忽视对方可能提出的合法来源抗辩，导致策略被动。这些问题在起诉之前就应该想清楚。",
        "七、莞促知产能提供哪些帮助",
        "莞促知产扎根东莞松山湖，可协助企业核查商标权利状态、分析侵权线索、整理证据清单、制定维权路径，并在商标监测、行政投诉、异议无效与侵权应对等环节提供专业支持。对尚未完成布局的企业，也会同步给出补充注册与类别完善的建议，把维权和布局放在一张图上考虑。",
        "写在最后",
        "商标维权的顺序很重要：先判断是否构成侵权，再把证据固定好，然后核对自身权利，最后选择路径。顺序对了，投入才不会白费。如果发现市场上存在仿冒线索，欢迎与莞促知产交流，由专业顾问结合具体情况提供初步评估。",
    ],
    "news/n42.html": [
        "软件写完、产品上线，很多科技企业第一件事是申请软著。有人觉得它只是一张证书，有人直到融资、投标或发生纠纷时才发现，当初没登记会带来麻烦。软件著作权登记怎么做、材料怎么准备，看似流程简单，实际常因为源代码和文档不规范被反复补正。莞促知产把常见要点讲清楚。",
        "一、先弄清登记的是什么权利",
        "软件著作权属于著作权的一种，保护的是软件作品本身。登记是对权利归属的一种初步证明，有助于企业在融资、项目申报、软件上架、维权举证时提供权利凭证。需要区分的是，著作权自作品完成之日起产生，登记并非权利产生的前提，但登记证书在证明归属方面具有实际价值。此外，软件的思路、算法本身与代码表达是不同层面的问题，登记不替代专利保护。",
        "二、准备材料：源代码、文档与主体信息",
        "办理登记通常需要准备源代码、软件说明书或设计文档、申请人身份材料以及登记表。源代码要前后连续、逻辑完整，能体现软件的实际内容；文档要说明软件的功能、运行环境、主要模块与使用方式，与代码相互对应。以公司名义申请的，主体信息要与营业执照一致；委托办理的，还需签署委托书。材料之间的名称、版本号应保持一致。",
        "三、办理流程：从提交到领证",
        "实务中大致是：先确定软件名称、版本号与开发完成日期，再整理源代码和文档，随后通过规定渠道提交申请，受理后进入审查环节，审查通过后发放登记证书。若材料存在格式、内容或信息一致性问题，会收到补正要求，企业按要求修改后继续审查。把前期整理做细，通常能减少来回修改。",
        "四、源代码与文档最容易被退回的地方",
        "常见问题包括：源代码只截取片段、前后不连贯；代码中出现与申请主体无关的其他公司或第三方信息；文档描述过于简单，无法看出软件功能与结构；软件名称与文档标题、页面显示不一致；版本号填写随意，后续版本管理混乱。这些问题看似细节，却直接影响审查效率，也影响证书在后续使用中的说服力。",
        "五、登记之后还要做什么",
        "拿到证书不是终点。企业应建立版本管理记录，保存开发过程文档、需求说明与测试记录，形成完整的权利证据链。软件发生实质性变更、权利人名称变更或需要许可他人使用时，要按规定办理相应手续。发现他人未经许可复制、传播或销售软件时，登记证书与开发过程材料一起，才能构成有力的维权基础。",
        "六、莞促知产能提供哪些帮助",
        "莞促知产扎根东莞松山湖，可协助企业判断软件是否需要登记、梳理材料清单、规范源代码与文档的表述、核对主体与版本信息，并在版权布局、权利管理和侵权应对方面提供专业建议。对同时涉及专利、商标与软著的产品，我们会从整体保护角度给出组合方案。",
        "写在最后",
        "软件著作权登记的关键，在于把代码、文档和主体信息整理成一套互相印证的材料。企业提前把版本与归档做规范，办理会顺畅很多。有登记或版权保护需求的科技企业，欢迎与莞促知产交流。",
    ],
    "news/n43.html": [
        "东莞企业做外贸、跨境电商或在海外设点，常常先把货发出去、店铺开起来，才想起商标还没在当地注册。等到产品卖顺了，却发现品牌名已被他人抢注，改包装、换店名、谈回购，代价往往远高于当初注册的成本。海外商标到底怎么布局，莞促知产把常见路径和判断思路讲清楚。",
        "一、国内注册不等于海外受保护",
        "商标权具有地域性。在中国核准注册的商标，并不会自动在境外产生权利。企业要在某个国家或地区获得商标保护，通常需要按照当地制度提出申请并取得注册。即使通过电商平台销售，平台处理侵权投诉时往往也要求提供对应国家或地区的权利证明。这一点是出海企业最容易踩的坑。",
        "二、常见路径：单一国家、马德里体系与地区注册",
        "第一条路径是单一国家申请，直接向目标国家的商标主管机构提交，适合目标市场明确、数量不多的企业。第二条是通过马德里体系办理国际注册，以基础注册或申请为前提，指定多个成员国，便于后续统一管理。第三条是地区性注册，在部分区域通过一次申请获得多个成员国的保护。三种路径在前期成本、后续管理、指定范围上各有特点，需要结合企业市场计划选择。",
        "三、目标市场怎么选",
        "不要凭感觉列国家。建议按业务实际来排：先看货物主要销往哪些国家，再看生产、仓储、展会和电商站点设在哪些地方，接着考虑供应链与代理商所在区域，最后预留未来一两年可能开拓的市场。核心市场优先完成注册，再逐步扩展。对贴牌加工企业，还要确认品牌归属与委托方安排，避免替他人做了嫁衣。",
        "四、注册前要做的功课",
        "确定目标市场后，先做当地近似查询，判断拟用标识是否与在先权利冲突；再核对商品或服务项目的表述，不同国家分类习惯与译文要求存在差异，翻译不准确可能影响保护范围；同时确认申请主体信息、委托书等文件要求。商标图样、文字语种、音译与意译方案最好一并规划，避免进入市场后发现当地不能使用。",
        "五、东莞企业常见的三个误区",
        "一是先卖后注，以为销量起来再补注册也来得及，结果被抢注后被动谈判。二是只注册中文或只注册英文，忽略当地消费者实际使用的称呼和拼写方式。三是注册后不管续展和使用证据，权利形同虚设。海外商标不是一次性动作，而是需要随市场变化持续维护的资产。",
        "六、莞促知产能提供哪些帮助",
        "莞促知产扎根东莞松山湖，是莞促集团旗下专注知识产权与科技申报的机构。我们可协助企业梳理目标市场优先级、比较不同注册路径、开展前期查询与材料准备，并在国内商标布局、马德里国际注册后续管理、海外侵权应对等环节提供专业支持，让国内与海外的品牌保护衔接起来。",
        "写在最后",
        "出海之前，先把商标的地域边界画清楚：市场到哪里，保护就先跟到哪里。路径没有绝对优劣，关键是匹配企业自身的销售计划与预算。有海外商标布局需求的企业，欢迎与莞促知产交流。",
    ],
    "news/n40.html": [
        "最近，酱香白酒市场上的“创始王”品牌受到关注。围绕它的话题，常被简化成“谁才是正宗”的争论。但如果把镜头拉近，这场持续多年的争议真正涉及的，是两件容易被混为一谈的事：历史能不能讲，商标能不能用。对做品牌的企业来说，这条边界比单纯的输赢更值得研究。",
        "一、品牌故事：从荣太和烧房到创始王",
        "公开史料记载，清光绪五年（1879年），茅台镇人王立夫（字泽履）与石荣霄、孙全太在杨柳湾合股开办“荣太和烧房”，后因股东变更更名为“荣和烧房”，所产酒被称为“荣和茅酒”，也就是后来俗称的“王茅”的由来。民国四年（1915年），荣和烧房与成义烧房选送的酒以“茅台造酒公司”名义参加巴拿马万国博览会并获奖。",
        "二十世纪五十年代初，国家陆续收购荣和烧房等三家烧房，组建国营企业，“王茅”商标随之进入国营酒厂体系，王家后人不再使用该标识。此后，王家第五代传人王宗德在政策放开后恢复传统酿造，技艺在家族内部延续。到第七代传人王诗琳，注册成立贵州创始王茅酿酒（集团）有限公司，推出“创始王”品牌——按品牌方的解释，三个字指向“王茅的创始人”。",
        "二、纷争焦点：一句话引发的诉讼",
        "争议并非始于酒本身，而是始于表述。王家后人在宣传中讲述家族与荣和烧房的渊源，使用“茅台酒创始人之一”“茅酒起源”等说法。据公开信息，贵州茅台方面认为这类表述构成虚假宣传与不正当竞争并提起诉讼；贵州省高级人民法院作出（2022）黔民终564号终审判决，认定王立夫（字泽履）是“荣和烧房”创立人、茅台酒创始人之一，并认为有史料支撑的相关历史陈述不构成虚假宣传或不正当竞争，撤销一审判决、驳回诉讼请求。",
        "这里需要看清判决的准确含义。它解决的是“历史表述是否虚假、是否构成不正当竞争”的问题，并没有重新分配“王茅”“茅台”等注册商标的权属，也没有给任何一方随意使用他人注册商标的许可。网络上把它解读成“夺回商标”“品牌归谁”，实际上超出了裁判本身的范围。",
        "三、莞促知产分析：商标专用权与历史叙事权是两条线",
        "在莞促知产看来，这个案件最有价值的提示，是把两条边界画清楚了。第一条线是商标专用权。注册商标用于识别商品来源，权利人依法享有排他使用的权利；他人把相同或近似标识用在相同或类似商品上，突出使用、攀附商誉、容易导致混淆的，就可能落入商标侵权或不正当竞争的争议范围。",
        "第二条线是客观叙事权。历史不属于某一家企业的私有资产。家族后人依据族谱、地方志、档案资料，平实地讲述先辈创业与工艺传承，属于对客观事实的叙述。这类表述是否正当，关键看有没有事实依据、表达方式是否克制、是否借历史之名指向商品来源。判决确认的是这一叙述空间，而不是商业标识的共用空间。",
        "四、企业最容易踩的三条线",
        "第一条线，是把历史称谓写成商品名称。讲“祖上做过什么”，与把这段历史直接做成酒名、店招、包装主视觉，是性质不同的两种使用。一旦历史称谓被当作识别商品来源的标记，就从叙述滑向了商标性使用。",
        "第二条线，是表述从客观变成攀附。有史料支撑的“创始人之一”是事实陈述；如果把同一句话放进与知名品牌的对比广告，再配上近似包装、暗示授权或联名，表达的性质就变了。判断时看的不是孤立的一句话，而是它所在的整体语境。",
        "第三条线，是以为赢了名誉官司就拿到了商标使用权。诉讼中确认历史事实，与能否注册、使用某个商标，属于不同程序、不同审查标准。企业若要使用特定标识，仍要走近似查询、注册申请、异议与无效等确权路径。",
        "五、给企业的实操建议",
        "先做确权，再做传播。品牌名确定之前，先做近似检索，判断与在先商标的冲突风险；核心类别、关联类别与防御类别一并规划，别等宣传做大了才发现名字用不了。",
        "给历史表达做一次合规体检。把官网、包装、短视频脚本、直播话术里的历史表述逐条过一遍：有没有史料支撑、有没有绝对化用语、有没有让人误以为与某个品牌存在授权或关联。留存史料出处，比事后解释更有说服力。",
        "发现争议要及时固定证据。宣传物料的发布时间、修改记录、销售与传播数据、对方的沟通函件，都应系统留存。面对异议、无效宣告或侵权主张，证据链完整才有答辩与谈判的基础。",
        "把商标管理做成长期机制。注册成功不等于一劳永逸，续展、实际使用证据留存、近似商标监测、及时异议，都是守住品牌资产的日常动作。",
        "写在最后",
        "创始王事件提醒我们：尊重历史事实与尊重注册商标秩序并不矛盾。企业可以骄傲地讲清自己从哪里来，但要把“讲历史”和“用商标”分开。莞促知产扎根东莞松山湖，围绕商标注册、近似查询、异议无效、品牌布局与维权提供专业服务，欢迎有品牌确权需求的企业与我们交流。",
    ],
    "news/n37.html": [
        "在东莞申请专利，很多企业不是输在技术不够好，而是栽在材料准备上：技术交底写得笼统、附图不清楚、申请人信息对不上，来回补正耽误不少时间。材料是专利申请的地基，地基打不牢，后面写得再漂亮也稳不住。莞促知产就把东莞专利申请需要准备的材料和常见要点讲清楚。",
        "一、先确定申请主体与发明人信息",
        "专利申请要写明申请人是谁。以公司名义申请的，准备营业执照信息；以个人名义申请的，提供身份信息。同时要列明发明人——即对技术方案作出创造性贡献的实际人员。申请人可以不是发明人，两者不要混为一谈；姓名、地址等信息要与证照一致，避免形式审查时被要求补正。",
        "二、技术交底书：最关键的一份材料",
        "技术交底书是代理人撰写申请文件的基础。要写清要解决的技术问题、采用的技术方案以及带来的有益效果，并配合附图或实验数据说明。交底越具体，代理人越能准确把握发明点，权利要求也写得越准。只写一句“提升了效率”，往往支撑不起一份有保护力的申请。",
        "三、按专利类型准备对应材料",
        "发明专利侧重技术方案本身，需要充分公开技术细节并说明创造性；实用新型专利保护产品的形状、构造及其结合，要提供能体现结构特征的附图；外观设计专利保护产品外形，需提交清晰的外观图片或照片，必要时说明设计要点。不同类型要求不同，准备前先明确要申请哪一种。",
        "四、附图与图纸要求",
        "涉及结构或外观的申请，附图直接决定保护范围是否清楚。图纸要线条清晰、标记规范、各视图一致，避免出现模糊、涂改或前后矛盾的情况。外观设计图片还要注意背景干净、角度完整，让审查员和实施方都能准确理解设计要点。",
        "五、委托代理的授权材料",
        "委托专利代理机构办理的，需要签署代理委托书，明确委托事项与权限。同时建议与代理机构签订保密协议，对技术资料、交底文件做好保密约定。东莞企业在委托前，可核验机构是否具备合法执业资质。",
        "六、提交前的自查清单",
        "提交前逐项核对：申请人信息是否与证照一致、发明人是否列全、技术交底是否写透、附图是否清晰规范、委托书是否签署完整。企业也可以先做一次专利检索，判断技术方案是否具备新颖性，避免盲目提交。把这些基础工作做扎实，审查流程会顺畅很多。",
        "写在最后",
        "东莞专利申请的材料准备，核心是把技术讲清楚、把信息填准确、把附图做规范。前期多花一点功夫，后面少很多返工。莞促知产扎根东莞松山湖，为企业提供专利检索、技术交底指导、申请撰写与审查答复等专业服务，欢迎与我们交流。",
    ],
    "news/n38.html": [
        "东莞企业在办专利申请时，经常听到“预审”这个词：有人说东莞专利申请走预审能加快审查，有人说要先备案才能用。到底东莞专利申请的预审怎么办、企业怎么才能用上？莞促知产按办事指南的思路，把备案和申请两个环节讲清楚，帮企业判断自己适不适合走这条通道。",
        "一、什么是东莞专利申请预审",
        "专利预审是知识产权保护中心为备案主体提供的前置审查服务。企业通过保护中心提交专利申请，保护中心对符合要求的申请进行预审，预审通过后，申请人再向国家知识产权局正式提交，可以缩短东莞专利申请的审查周期。预审服务本身通常不收取费用，对符合条件的企业是一项实实在在的便利。",
        "二、先判断企业是否符合备案条件",
        "要使用东莞的预审服务，企业一般需要先完成备案。备案通常要求登记注册地在东莞、属于保护中心服务的产业领域，并具备一定的知识产权管理基础。东莞保护中心的服务领域和具体备案条件以当期公布的规定为准，企业申请前应先对照官方要求自查。",
        "三、备案大致要走哪些环节",
        "从实务看，东莞专利申请预审的备案一般包括：在保护中心指定平台注册用户、提交备案申请表及营业执照等材料、由保护中心审核、审核通过后纳入备案主体名单。材料要真实完整，产业领域、主营业务等信息要如实填报。备案通过后，还要注意按要求参加年审或信息更新，保持备案资格有效。",
        "四、预审申请怎么提交",
        "成为备案主体后，企业通过保护中心的专利预审系统提交申请材料。保护中心对申请文件、技术领域、发明人信息等进行预审，符合要求的出具相关意见，申请人据此向国家知识产权局正式提交申请。需要注意，预审只是前置环节，最终的授权仍由国知局依法审查决定。",
        "五、哪些情况不适合走预审",
        "如果企业不属于服务领域、技术方案与备案领域关联度低，或者申请文件质量不高，东莞专利申请走预审可能难以通过。此时不如按普通途径申请，先把文件质量做扎实。对技术交底不清、权利要求不规范的申请，无论走哪条通道，都容易在实质审查中遇到障碍。",
        "六、莞促知产能提供哪些帮助",
        "莞促知产扎根东莞松山湖，可以协助企业判断是否符合备案条件、准备备案材料，并在专利检索、技术交底撰写、预审申请文件准备等环节提供专业支持。对不适合预审的技术方案，也会给出更合适的申请路径建议。",
        "写在最后",
        "东莞专利预审是一项对符合条件企业很有价值的服务，但前提是要先搞清楚备案条件和办理流程。企业不妨先对照官方要求自查，再决定是否申请备案。莞促知产欢迎有需求的企业与我们交流，一起把专利布局这条路走稳。",
    ],
    "news/n39.html": [
        "东莞企业要找知识产权代理机构，打开搜索一搜，满屏都是“专业代理”“高通过率”，很难分辨谁更靠谱。代理机构的选择，直接影响申请质量、权利稳定性和后续维权效果。莞促知产站在企业视角，讲清楚选择东莞知识产权代理机构时应该看什么。",
        "一、先看资质是否正规",
        "选择代理机构，第一关是资质。专利代理机构应依法取得执业许可，商标代理机构应符合相应备案要求。企业可以通过国家主管部门的公开渠道核验机构资质，避免遇到没有资质的“二传手”。资质是底线，过不了这一关，其他承诺都不用考虑。",
        "二、看是否懂你的行业和技术",
        "知识产权服务专业性强，不同行业的技术、不同类别的商标，规则细节差异很大。好的代理机构会先听懂企业的业务——技术是什么、产品卖到哪、品牌怎么用，再谈方案。如果一上来就报价、包授权，却问不清技术背景，往往做不出贴合业务的保护方案。",
        "三、看流程是否透明",
        "很多企业抱怨“交了钱就没人管”。判断机构是否可靠，可以问清楚：受理、审查、公告、授权这些节点会不会主动同步？遇到补正或审查意见怎么处理？材料清单是不是一次讲清？流程透明的机构，让企业随时知道事情办到哪一步，合作起来更放心。",
        "四、看服务是否覆盖确权之后的环节",
        "知识产权的价值在确权之后才开始：专利能不能用于高企认定、商标能不能质押融资、遇到侵权怎么维权。只管申请、不管后续的机构，很难帮企业把权利用起来。选择时可以问问对方是否提供布局规划、风险排查、维权应对和后续管理等服务。",
        "五、看保密与诚信做得实不实",
        "知识产权服务接触的是企业最核心的技术和商业秘密。靠谱的机构会主动签订保密协议、限定资料接触范围，并且如实说明成功率、不夸大承诺。那些张口就“保证授权”“包过”的说法，反而值得警惕。",
        "六、结合本地服务与长期陪伴",
        "对东莞企业来说，选择熟悉本地产业、能够面对面沟通的机构，沟通成本更低、响应更快。企业业务会成长，知识产权需求也会变化，能长期陪伴、定期回访、把续展年费等节点管起来的机构，更值得托付。",
        "写在最后",
        "选东莞知识产权代理机构，不用看广告打得响不响，重点看资质、专业匹配度、流程透明度、服务链条、保密诚信和本地服务能力。把这几点问清楚，基本就能筛出靠谱的合作伙伴。莞促知产扎根东莞松山湖，是莞促集团旗下专注知识产权与科技申报的机构，欢迎企业前来了解与交流。",
    ],
    "news/n34.html": [
        "在东莞办商标注册，很多人第一反应是先想名字，等到真正要提交时才发现材料没备齐，来回补件耽误不少时间。材料准备看似琐碎，却直接关系到申请能不能顺利受理。莞促知产就把东莞商标注册通常需要准备的材料和常见注意点讲清楚，帮企业少走弯路。",
        "一、先确定申请主体身份材料",
        "商标注册的第一步，是明确以谁的名义申请。以公司名义申请的，需要准备营业执照复印件并加盖公章；以个体工商户名义申请的，需提供营业执照及经营者身份证明；以个人名义申请的，则需要个人身份证复印件和相应的经营范围证明。主体信息要与营业执照或身份证件完全一致，名称、地址任何一个字对不上，都可能被要求补正。",
        "二、准备商标图样",
        "商标图样是申请的核心材料。需要提供清晰、规范的标志图样，如果是文字商标，按标准字体提交；如果是图形或图文组合商标，要保证图样清晰、边界完整。指定颜色的，要提交彩色图样并说明；不指定颜色的，提交黑白图样即可。图样的清晰度直接影响后续审查与公告，建议提前处理好。",
        "三、确定商品或服务类别与项目",
        "商标注册是按类别保护的，申请时要写明使用商标的商品或服务类别及具体项目。企业应根据自身主营业务和未来发展，选准类别、选全项目。类别选择不当，会导致保护范围与业务不匹配——这一点比材料本身更值得花时间。不确定的，可先做类别梳理再提交。",
        "四、准备代理委托材料（如委托办理）",
        "委托商标代理机构办理的，需要签署代理委托书，明确委托事项与权限。自行办理的，则由申请人直接向商标局提交材料。对流程不熟悉的申请人，委托专业机构可以帮忙核对材料、规范填报，减少因形式问题被补正的情况。",
        "五、核对联系方式与送达地址",
        "申请书中的联系人、电话、地址等送达信息务必准确有效。审查过程中的补正通知、审查意见、公告信息等都要靠这些信息送达。联系方式失效或地址错误，可能错过答复期限，影响申请进程。地址发生变更的，也要及时办理变更手续。",
        "六、提交前的自查清单",
        "提交前建议逐项核对：主体身份材料是否齐全并与证照一致、商标图样是否清晰规范、类别与项目是否匹配业务、委托书是否签署完整、联系方式是否有效。把这些检查一遍，能大幅减少补件返工。东莞企业在注册前，也可以先通过专业渠道做一次近似查询，降低因冲突被驳回的风险。",
        "写在最后",
        "东莞商标注册的材料并不复杂，关键在于细致和对得上——主体信息对得上、图样规范清晰、类别匹配业务、送达信息有效。把这些基础工作做扎实，后面的审查流程会顺畅很多。莞促知产扎根东莞，为企业提供商标查询、材料核对、注册申报等专业服务，欢迎与我们交流。",
    ],
    "news/n35.html": [
        "在东莞注册商标，几乎每个企业都会遇到同一个问题：我这个商标到底该注册哪几个类别？类别选少了，保护不到位；选多了，成本又上去了。类别选择是商标注册里最考验判断力的环节之一。莞促知产结合实务经验，讲清东莞商标注册时该如何选类别。",
        "一、先弄懂：商标为什么要按类别注册",
        "商标保护不是全类别通用的，而是按商品和服务的类别划分。申请人应当在商标局公布的商品服务分类中，选择与自己业务相关的类别进行注册。也就是说，注册商标只在核定使用的类别和项目上受保护，超出这个范围，保护作用就大打折扣。理解这一点，是选类别的前提。",
        "二、以当前主营业务为核心类别",
        "选类别首先要覆盖当下正在经营的产品或服务。企业做什么、卖什么、提供什么服务，对应的类别就要优先注册。比如生产销售类企业，要覆盖产品本身的类别；提供服务类企业，要覆盖服务对应的类别。核心类别是保护的底座，不能遗漏。",
        "三、围绕业务链条补充关联类别",
        "只看当前主营业务还不够。企业的业务往往是一条链条，从生产、销售到推广、服务，涉及多个环节。莞促知产通常会建议企业沿着业务链条梳理：产品制造、销售渠道、线上平台、广告宣传、售后服务等环节，是否涉及应当保护的类别。把关联类别一并考虑，才能形成较完整的保护。",
        "四、为未来业务预留空间",
        "商标的价值随企业发展而增长。企业计划拓展的新产品、新市场、新业务方向，如果与现有品牌密切相关，可以提前在相应类别布局。等到品牌做大了才发现核心类别被他人抢注，维权和回购的成本往往远高于提前注册。预留不等于盲目多注，而是有依据地规划。",
        "五、留意容易忽视的类别",
        "有些类别常被企业忽略，比如与线上经营、广告推广、品牌管理相关的服务类别。对做电商、做连锁、做品牌授权的企业来说，这些类别与主营业务同样重要。建议在专业检索的基础上，对照企业实际的经营场景逐一排查，避免留下保护空白。",
        "六、类别选择要和近似查询结合",
        "类别确定后，还要在目标类别中做近似查询，看看拟注册标志是否与他人已注册或在先申请的商标构成冲突。类别选择和近似查询是前后衔接的两步：先选对类别，再查清风险。跳过任何一步，都可能让注册效果打了折扣。",
        "写在最后",
        "东莞商标注册选类别，本质是让商标保护范围与企业的业务版图对齐。以主营业务为核心，沿业务链条补充关联类别，为未来预留空间，再结合近似查询确认可行性——按这个思路选，保护才扎实。莞促知产扎根东莞，提供商标类别规划、近似查询与注册申报服务，欢迎与我们交流。",
    ],
    "news/n36.html": [
        "很多东莞企业在注册商标时会纠结一个问题：这个商标是用公司名义申请，还是用老板个人名义申请？看上去只是填一个申请人，实际上会影响权利的归属、使用和后续处置。莞促知产就把两种申请主体的差异讲清楚，帮企业结合实际作出选择。",
        "一、个人与公司都能申请商标注册",
        "按照商标法的规定，自然人、法人或者其他组织都可以申请注册商标。也就是说，个人名义和公司名义都是合法可行的申请方式，不存在哪种一定更好的绝对答案。关键要看哪种方式更匹配企业的实际情况和长期安排。",
        "二、公司名义申请：权利归属清晰",
        "以公司名义申请，商标权归公司所有，与企业经营和品牌使用主体一致。这样做的好处是权属清晰，便于企业进行品牌运营、授权、质押融资和资产评估；融资、尽调或上市时，知识产权归属也更经得起核查。对有规范经营和长期发展规划的企业，公司名义通常是更稳妥的选择。",
        "三、个人名义申请：灵活但要注意归属",
        "以个人名义申请，操作相对灵活，适合一些个体经营或品牌尚未完全公司化的情形。但要特别注意：商标权归个人所有，如果实际由公司使用，应当通过许可或转让等方式把使用关系约定清楚。否则企业做大后，商标却在个人名下，容易在股权变动、合作或融资时产生归属争议。",
        "四、结合经营主体和发展阶段来选",
        "选择申请主体，应从实际出发：如果业务已经由公司统一经营、品牌属于公司资产，就以公司名义申请；如果目前是个体经营、未来可能成立公司，可以先以个人名义注册，并在公司成立后及时办理转让或许可手续。无论哪种，都要让权利主体与实际使用主体保持一致。",
        "五、材料要求有所不同",
        "两种主体提交的材料不同：公司名义需提供营业执照并加盖公章；个人名义需提供身份证及相应经营证明；个体工商户则按其特定要求提供。材料的准确与完整，直接关系申请能否顺利受理，提交前要按对应主体的要求逐一核对。",
        "六、别忽略后续的许可与转让手续",
        "如果商标权人和实际使用人不是同一个主体，务必把许可或转让手续办规范：签订书面协议，明确使用范围、期限，必要时办理备案或变更登记。把这些手续做在前，能避免日后在品牌使用、维权或资产处置时出现权属扯皮。",
        "写在最后",
        "东莞商标注册用个人还是公司名义，没有标准答案，但有一个判断原则：让商标权与实际经营主体一致，让权属经得起长期使用和交易的检验。结合企业现阶段情况和未来规划来选择，必要时把许可、转让关系提前约定清楚。莞促知产扎根东莞，提供商标申请、权属规划与转让许可等专业服务，欢迎与我们交流。",
    ],
    "news/n31.html": [
        "国家知识产权局日前印发《专利和商标审查“十五五”规划》，明确了下一阶段专利和商标审查工作的目标、任务和专项工程。对企业和代理机构来说，这份规划不只是一份工作部署，更传递出一个清晰信号：审查正在从“求快”转向“求稳、求质”，申请的门槛会更加看重质量。莞促知产结合规划内容，谈谈它对企业知识产权布局的实际影响。",
        "一、规划讲了什么",
        "规划围绕专利审查、商标审查、审查业务国际合作、审查能力建设四个方面部署重点任务，并设立了新兴领域专利审查规则完善、商标审查质量提升、“人工智能+”审查等专项工程。总体思路是坚持质量第一、改革创新、服务发展、系统协同与技术赋能，推动专利和商标审查提质增效。",
        "二、信号一：审查质量优先，申请不能只求数量",
        "规划多次强调“全面提升审查质量”“提升商标审查质效”。这意味着，靠大量低质量申请占位的做法，空间会越来越小。对企业来说，与其追求申请数量，不如把每一件申请做扎实：技术交底写充分、权利要求布局合理、商标标志有显著性且经过检索。质量过硬的申请，在审查中更顺畅，权利也更稳定。",
        "三、信号二：新兴领域规则在完善，科技企业要跟上",
        "规划提出完善大数据、人工智能、基因技术等新兴领域的专利审查标准，研究人工智能辅助发明、人工智能生成发明、人工智能使用声明制度等。对从事人工智能、数据业务的东莞企业来说，这些领域的技术成果如何申请专利、如何界定发明人、使用人工智能工具是否需要声明，都值得提前关注并咨询专业意见。",
        "四、信号三：审查更智能，材料规范更重要",
        "规划部署“人工智能+”审查工程，推动多模态大模型等技术应用于审查环节。智能工具能提升检索和比对的效率，也意味着申请文件中的表述、引用和格式会更加规范地被核验。企业提交材料时，更要注意逻辑清晰、表述准确、前后一致，减少因形式问题被补正。",
        "五、信号四：支持海外布局，出海企业有政策支撑",
        "规划在审查业务国际合作方面提出，支持创新主体、经营主体提升海外专利和商标布局水平。对有出海计划的企业，这是一项利好：通过专利合作条约、马德里体系等途径进行海外布局，可以借助政策与专业服务，让权利在目标市场提前到位，避免产品出海后才发现商标被抢注、专利未覆盖。",
        "六、企业现在可以做什么",
        "面对这些变化，企业不妨做三件事：一是对现有知识产权做一次盘点，剔除与业务脱节的低质量申请，把资源集中到核心技术；二是在人工智能、数据等新兴领域，及早咨询专业机构，明确申请策略；三是把海外布局纳入出海计划，在产品进入市场前完成商标和专利的先行布局。",
        "写在最后",
        "审查规划的调整，本质上是引导创新主体把知识产权做实、做精。对愿意长期投入的企业来说，这是更有利的环境。莞促知产扎根东莞松山湖，持续跟踪专利与商标政策变化，为企业提供高质量申请、新兴领域布局与海外知识产权服务，欢迎与我们交流。",
    ],
    "news/n32.html": [
        "国家知识产权局、海关总署联合印发《关于强化知识产权协同保护的意见》，提出推动知识产权管理部门与海关在保护工作中形成合力，构建“严保护、大保护、快保护、同保护”的工作格局。这份意见与进出口企业关系密切——对东莞这样外向型经济活跃的城市，海关环节的保护是否到位，直接关系到企业的货物和品牌安全。莞促知产为你解读其中的企业关切。",
        "一、意见的核心：两个部门打通协作",
        "过去，知识产权保护和海关执法分属不同体系，信息、标准和办案资源相对分散。这次意见从信息共享、调查协助、业务支撑、重点领域保护、会商调研等方面作出部署，让知识产权管理部门与海关之间能够互相提供数据、协助调查、统一判断标准，形成全链条保护。",
        "二、对企业最直接的影响：海关备案更有价值",
        "意见明确提出，知识产权管理部门鼓励有驰名商标确认记录、作为地理标志注册的集体商标与证明商标、光伏等重点产业企业的权利人积极向海关申请知识产权备案，海关对相关备案申请依法审核，备案后结合产业政策和风险分析加强保护。",
        "换句话说，把商标、专利在海关做备案，权利人就多了一道进出口环节的防线。没有备案，海关在口岸发现疑似侵权货物时，往往难以主动采取保护措施；完成备案后，海关能够更及时地依职权对嫌疑货物进行扣留和调查。",
        "三、海关备案要准备什么",
        "企业办理知识产权海关备案，通常需要准备权利证明文件、权利人身份与联系方式、货物和包装图样、合法进出口企业情况等材料。委托专业机构办理的，顾问会协助核对材料、规范填报，减少因信息不全导致的补正。备案不是一劳永逸，权利发生变更、续展或失效时，也要及时办理变更或注销。",
        "四、发现进出口侵权，救济渠道更顺畅",
        "意见强化了调查协助：知识产权管理部门处理涉及进出口货物的商标、专利侵权案件，可请求海关协助；海关对被扣留的侵权嫌疑货物进行调查，也可请知识产权管理部门提供协助，对技术性较强的专利侵权案件，还可推荐技术调查官等专家。对企业来说，遇到进出口环节的侵权纠纷，维权时部门之间的衔接会更顺畅，举证和认定也更有依据。",
        "五、判断标准趋于统一，维权预期更稳定",
        "意见提出，海关办案遇到同种商品、类似商品、相同商标、近似商标、专利侵权等认定问题，可以征求同级知识产权管理部门意见，后者应及时出具专业意见。这意味着商标近似、专利侵权的判断不再因部门不同而口径差异过大，企业的维权结果更可预期。",
        "六、外向型企业现在该做什么",
        "建议做三件事：一是核查自有商标、专利是否已办海关备案，重点品牌优先考虑；二是建立进出口环节的侵权监测，发现疑似仿冒货物及时固定线索并向海关反映；三是把海关备案纳入知识产权台账，与续展、变更等事项同步管理。",
        "写在最后",
        "协同保护意见让知识产权保护从申请端延伸到口岸端。对做外贸、做跨境的企业，海关备案是一道成本低、作用实的保护措施。莞促知产扎根东莞松山湖，提供商标与专利申请、海关备案、侵权维权等一站式服务，欢迎有进出口业务的企业与我们交流。",
    ],
    "news/n33.html": [
        "国家知识产权局、国家数据局联合印发《关于加强知识产权数据资源开发利用的意见》，这是两部门首次就知识产权数据资源开发利用出台专门意见。与此同时，数据知识产权登记试点持续推进，全国统一登记平台也在建设之中。对手里积累着大量数据的企业来说，数据能不能确权、怎么确权、确权后有什么用，正在从概念变成现实问题。莞促知产结合政策，梳理企业关心的要点。",
        "一、两份政策分别在解决什么问题",
        "两部门意见从制度、标准、基础设施、共享开放、信息服务、企业创新六个维度作出部署，目标是让知识产权数据成为数字经济发展的基础资源。数据知识产权登记试点则解决另一头的问题：企业经过加工形成的数据集，如何通过登记获得权属公示凭证。前者打通数据流通，后者明确数据归属，两者共同构成数据资产化的基础。",
        "二、什么是数据知识产权登记",
        "数据知识产权，指的是依法依规获取、经过一定规则处理、具有实用价值的数据集合，通过登记确认数据处理者相应权益的一种制度。它不是给原始数据发证书，而是对经过创造性加工、具备独立价值的数据集予以确权。登记证书可以作为持有相应数据的初步证明，用于数据流通交易、收益分配和权益保护。",
        "三、登记大致要走哪些环节",
        "从各试点地区的实践看，数据知识产权登记一般包括登记申请、登记审查、登记公示、登记公告等环节。申请人需要提交申请人情况、数据来源、处理规则等材料，上传样例数据并签署声明承诺书，对数据来源合法性和处理过程合规性作出承诺。审核通过的申请会进行公示，公示无异议或异议不成立的，登记机构签发登记证书并公告。具体流程和要求，以所在地区登记机构的规定为准。",
        "四、登记之后有什么用",
        "登记证书的价值主要体现在几个方面：一是作为数据权属的初步证明，在合作、交易中减少权属尽调成本；二是用于数据资产入表、质押融资，帮助企业把数据资源转化为可计量的资产；三是在发生争议时作为举证材料，支撑权益保护。对科技型、平台型企业来说，这相当于给核心数据资产办了一张“身份证”。",
        "五、企业现在该怎么做",
        "首先，梳理自有数据：哪些是原始采集、哪些经过加工处理、哪些具有独立应用价值，先分清楚。其次，确认数据来源合法、处理过程可追溯，留存采集授权、清洗规则、加工记录等证据。再次，关注所在地区是否已纳入登记试点、有没有对应的申请指引，符合条件的可尽早尝试登记。涉及数据跨境的，还要同步关注相关合规要求。",
        "六、需要注意的边界",
        "数据知识产权与专利、版权、商业秘密是不同制度，不是所有数据都适合走同一条路径。技术上具备创新性的方案，可能更适合考虑专利；具有独创性的表达，可以考虑版权；不适合公开的核心数据和经营信息，商业秘密保护往往更稳妥。企业应根据数据性质选择合适的保护组合，而不是盲目跟风登记。",
        "写在最后",
        "数据正在成为企业的重要资产，而确权是资产化的第一步。随着政策推进和平台完善，尽早把数据家底盘清、把合规基础打牢的企业，会在未来的数据流通和竞争中占据主动。莞促知产扎根东莞松山湖，持续关注数据知识产权等新兴领域规则，为企业提供确权路径咨询与知识产权布局服务，欢迎与我们交流。",
    ],
    "news/n28.html": [
        "品牌注册走到一半收到驳回通知书，很多创业者会一下子慌了神，以为这个名字彻底用不了了。其实在商标审查中，驳回是很常见的一种结果，它并不意味着申请走到终点。关键在于先读懂驳回的理由，再判断下一步该怎么走。莞促知产就把驳回之后的流程和思路讲清楚。",
        "一、先分清是全部驳回还是部分驳回",
        "商标驳回通常分两种情形：一种是全部驳回，即申请标志在指定商品或服务上都被认为不符合注册条件；另一种是部分驳回，即部分商品或服务项目可以初步核准，另一部分被驳回。两种情形的处理思路不同。收到通知后，第一步是看清楚驳回的范围，确认哪些项目还有机会、哪些需要重新考虑。",
        "二、读懂驳回通知书里的理由",
        "驳回通知书会写明审查意见和引用的在先权利。常见理由包括与在先商标构成近似、缺乏显著性、属于不得注册的标志等。企业要逐条对照：如果是因为近似，就要看冲突的是哪个在先商标、自己是否真的难以避让；如果是因为显著性不足，就要判断能否通过实际使用证据来说明。理由不同，后续的应对方向完全不同。",
        "三、判断值不值得提出驳回复审",
        "不是每一种驳回都适合复审。如果驳回理由是绝对障碍，比如使用了法律禁止的标志，复审成功的空间往往有限；如果是因为在先近似，而自己的标志有独特来源、在先使用事实或可以争取权利人理解，复审就有讨论的价值。企业可以结合品牌对该名称的依赖程度、重新设计的成本，权衡是复审还是换名重来。",
        "四、驳回复审要准备哪些材料",
        "决定复审后，材料准备是核心环节。通常需要围绕驳回理由逐一回应：主张标志不近似的，可以从读音、字形、含义、整体印象等角度说明差异；主张在先使用的，要提供使用时间、范围与知名度的证据；涉及在先权利冲突的，可以提交与在先权利人协商后取得的结果。材料越能直接回应审查意见，说服力越强。",
        "五、复审请求的提交与审查流程",
        "驳回复审要在法定期限内提出，逾期未申请，申请就会失效。复审申请提交后，审查机构会重新审查，企业可能需要按要求补充证据或作出说明。整个过程要保持材料一致、理由聚焦，避免东拉西扯。委托专业机构办理的，顾问会同步关键节点，帮助企业及时应对补正。",
        "六、复审未获支持还有哪些后续途径",
        "如果驳回复审没有获得支持，企业仍可以根据具体情况考虑其他途径：比如对引证的在先商标提出异议或无效宣告，从权利基础上排除障碍；或者调整标志设计、更换类别重新申请。同时，也可以先以未注册状态使用品牌，积累使用证据，为后续再次申请做准备。",
        "写在最后",
        "商标被驳回并不可怕，可怕的是不看理由、放弃救济，或者盲目复审。读懂驳回通知、理性判断价值、按流程准备材料，才是把品牌保住的正确方式。莞促知产扎根东莞松山湖，为企业提供商标近似查询、驳回复审、异议与无效等专业服务，如果您的品牌遇到了驳回难题，欢迎与我们交流。",
    ],
    "news/n29.html": [
        "专利申请被驳回，是不少企业和发明人都会遇到的情况。很多人把它理解为“这项技术没法保护了”，实际上驳回只是审查过程中的一种结果，后面还有答复、复审等救济途径。关键是先弄清楚驳回发生在哪个环节、理由是什么，再决定下一步。莞促知产就按流程把几种救济途径梳理一遍。",
        "一、先弄清驳回发生在哪个阶段",
        "专利申请的不同阶段，对应的救济方式不一样。一种是在审查过程中，审查员发出审查意见，指出新颖性、创造性或文件格式等方面的问题；另一种是经审查后直接作出驳回决定。前者还有答复和陈述意见的机会，后者则要启动复审程序。先看清楚通知的类型，才能选对应对方式。",
        "二、审查意见答复：把问题说清楚",
        "收到审查意见后，申请人可以在规定期限内提交答复。答复的核心是针对审查意见逐条回应：认为审查员对技术方案理解有偏差的，可以结合原始申请文件说明技术要点；认为对比文件不足以否定新颖性或创造性的，可以从区别技术特征和有益效果角度论证。必要时可以对权利要求作适当修改，但修改不能超出原始公开的范围。",
        "三、驳回决定后的复审请求",
        "如果申请最终被驳回，申请人可以在法定期限内提出复审请求。复审请求要写明不服驳回的理由，通常围绕技术方案是否具备新颖性、创造性，以及审查程序是否存在问题展开。复审请求提交后，由专门机构重新审查，申请人可能需要进一步陈述意见或修改权利要求。",
        "四、复审不成的后续途径",
        "复审请求未获支持的，申请人还可以根据具体情况寻求进一步救济，比如依法提起行政诉讼。是否走这一步，要结合专利对本企业的重要程度、争议焦点和成本来权衡。对多数企业而言，更现实的做法是同步调整技术方案，选择另一条申请路径。",
        "五、驳回后如何调整申请策略",
        "驳回往往暴露出原申请文件的问题：权利要求写得过宽、技术交底不够充分、对比文件检索不到位等。企业可以借此重新梳理技术方案，考虑改为实用新型、拆分申请或补充实验数据后再申请。把这些经验反馈到下一次申请中，命中率会明显提高。",
        "写在最后",
        "专利申请被驳回，不是终点，而是一次重新审视技术方案的机会。看懂通知、分清阶段、按流程答复或复审，很多申请仍有挽回空间。莞促知产扎根东莞松山湖，为企业提供专利检索、申请撰写、审查意见答复与复审等专业服务，如果您遇到了专利驳回问题，欢迎与我们交流。",
    ],
    "news/n30.html": [
        "每年到了高新技术企业认定申报的时候，不少企业才发现：专利、软著这些材料临时准备已经来不及。知识产权是高企认定的重要支撑，但它考量的不是“有没有证书”，而是权利与企业的技术创新、主营业务是否真正匹配。莞促知产就把高企认定中知识产权相关的关注点梳理清楚。",
        "一、高企认定为什么看重知识产权",
        "高新技术企业认定的核心，是判断企业是否具备持续的自主创新能力。知识产权是这种能力的直接证据：它记录了企业做了什么研发、形成了什么成果、成果如何转化为产品。因此，审查关注的不只是权利数量，更看重权利与研发活动、主营产品的对应关系。",
        "二、知识产权要与主营产品高度关联",
        "企业用于认定的知识产权，应当能够支撑主营业务收入对应的产品或服务。如果拿一项与主营产品毫无关系的专利去申报，即便权利真实有效，也很难说明企业的创新能力。稳妥的做法是围绕核心产品和技术，梳理出一条从研发到专利、再到产品的清晰链条。",
        "三、权属清晰是最基本的前提",
        "用于认定的知识产权，权属必须清楚：专利证书上的权利人应当是企业本身，或者与被认定主体一致；通过受让取得的，要完成著录项目变更并留存手续；合作研发形成的成果，要通过合同把权属约定明确。权属不清的材料，在认定中很难被采信。",
        "四、权利要处于有效状态",
        "知识产权必须在有效期内并按规定缴纳费用，失效、终止或被宣告无效的权利不能作为有效支撑。企业应在申报前对自有权利做一次全面盘点，确认状态、核对信息，发现地址或名称变更未同步的，及时办理手续，避免材料在审核环节被卡。",
        "五、提前规划，把布局做在日常",
        "高企认定考查的是企业长期的创新积累，临时突击申请很难体现持续性。更合理的做法是把知识产权规划嵌入日常研发：研发立项时同步考虑专利挖掘，成果形成后及时申请，产品迭代时补充布局。这样到了申报时，材料自然齐备，也经得起核查。",
        "写在最后",
        "知识产权不是高企认定的“敲门砖”，而是企业创新能力的外在体现。把布局做在平时，让权利与业务真正对应，申报不过是水到渠成的事。莞促知产扎根东莞松山湖，为企业提供专利挖掘、申请布局、软著登记与高企认定申报的一站式服务，如果您正在准备认定，欢迎与我们交流。",
    ],
    "news/n27.html": [
        "一字之差，可能就是一场千万级的教训。近期，上海市闵行区人民法院审结了一起“山寨”汉堡品牌的商标侵权案：把知名品牌的商标换掉一个字去注册、加盟，签下1300家门店，最终被判赔偿经济损失500万元及维权开支6万余元。这起案件在2026年11月披露后引发广泛关注，也为企业商标注册与品牌保护敲响了警钟。",
        "案情并不复杂，但其中的法律逻辑和经营启示值得每个做品牌、做加盟的企业认真看一看。",
        "一、案情回放：一个近似商标，撑起1300家门店",
        "某餐饮公司是“塔斯汀”系列注册商标的权利人，这个主打“中国汉堡”的品牌在快餐市场拥有较高知名度。2021年，与他人品牌仅一字之差的“塔某汀”商标获准注册。此后，某运营公司受让该商标，与三家推广公司分工合作，把它用于授权许可、广告宣传和加盟招商，在全国多地开出“塔某汀汉堡”门店，招商手册记载签约门店达1300家，其中一家推广公司通过网络平台售卖相关产品金额600余万元。",
        "权利人发现后，向国家知识产权局提出无效宣告请求。2024年8月，国家知识产权局以“塔某汀”与“塔斯汀”构成近似为由，裁定宣告该商标无效。随后，权利人诉至法院，要求停止侵权并赔偿500万元及合理开支。",
        "二、法院为什么全额支持500万赔偿",
        "庭审中，侵权方辩称：“塔某汀”是合法注册的商标，使用时商标仍有效，属于正当使用，没有侵权故意。法院没有采纳这一说法，理由主要有三层。",
        "第一，一字之差构成近似侵权。商标侵权并不要求完全照抄。把他人注册商标中的显著部分替换成读音相似、字形相近的字，在同一种服务上突出使用，足以让公众误认服务来源的，就构成侵权。",
        "第二，注册过不等于合法。根据商标法第四十七条，被宣告无效的注册商标，其专用权视为自始即不存在。也就是说，这张注册证不能当作侵权行为的“护身符”，无效之后，此前的注册状态并不能为攀附行为提供正当性。",
        "第三，主观故意明显。经营方作为同业者，对在先品牌的知名度属于“应知或明知”，却没有合理避让；在权利人已经提起无效宣告、权利状态明显存在瑕疵的情况下，仍继续对外授权、开展加盟、大量销售，主观过错明显。法院据此认定侵权获利和权利人损失已超过500万元，全额支持赔偿请求，二审也维持了原判。",
        "三、教训一：商标注册前，务必做深度近似检索",
        "这起案件最值得记住的一点，是“注册成功不等于安全”。“塔某汀”确实拿到过注册证，但因为与在先品牌构成近似，最终被宣告无效，还带来了巨额赔偿。",
        "对企业来说，品牌创立之初就应该树立合规意识，通过专业渠道做充分的近似检索，把读音、字形、含义相近的标识一并排查，从源头避开“擦边”和模仿。等到被无效宣告、被起诉时才补救，代价往往远高于前期做检索的成本。",
        "四、教训二：别把注册证当成侵权的护身符",
        "不少经营者有一个误区：只要我注册下来了，怎么用都行。这个案子明确否定了这种想法。商标权的基础是诚实信用，如果你明知在先品牌已有较高知名度，仍受让近似商标、大规模招商加盟、刻意攀附商誉，就不属于值得保护的善意信赖。",
        "换句话说，注册只是一个起点，权利的稳定性取决于它是否正当。企业在品牌推广、加盟授权过程中，也要持续关注权利状态，一旦发现瑕疵或争议，及时调整，避免损失扩大。",
        "五、教训三：加盟商要擦亮眼睛，查验权利基础",
        "这起案件里，加盟商也付出了代价。法官特别提醒：有些商标在招商时形式上处于“有效注册”状态，但可能是恶意抢注、囤积的商标，权利基础并不稳定，一旦被宣告无效，加盟商就会面临门店关停、强制改名的风险，前期投入也可能打了水漂。",
        "意向加盟者在考察项目时，务必保持理性，通过官方渠道核实特许经营资质，仔细查验商标注册证与授权文件，不要被“低门槛、高回报”的承诺冲昏头脑。选对品牌，才是守住钱袋子的第一步。",
        "六、给权利人：发现仿冒，要及时固定证据、主动维权",
        "从权利人角度，这起案件也提供了可借鉴的维权路径：先是针对近似商标提出无效宣告，从权利基础上釜底抽薪；再通过诉讼主张赔偿，并围绕侵权规模、持续时间、获利情况举证，最终获得全额支持。",
        "对遭遇“傍名牌”“搭便车”的企业来说，商标监测、证据固定和及时维权同样重要。放任仿冒不管，市场混淆只会越来越严重。",
        "写在最后",
        "一字之差，看似聪明，实则代价高昂。这起案件传递的信号很明确：商标竞争的底色应当是创新与服务，而不是混淆与攀附。无论是创立品牌、申请注册，还是招商加盟，把知识产权的功课做在前面，才是最稳的经营之道。",
        "莞促知产扎根东莞松山湖，为企业提供商标近似查询、注册布局、无效宣告与侵权维权等专业服务。如果您的品牌也遇到了近似仿冒或权利争议，欢迎与我们交流。",
    ],
    "news/n26.html": [
        "近日，英伟达的一则人事公告引发广泛关注：董事会一致投票决定，恢复黄仁勋公司总裁、首席执行官及董事职务。消息公布后，公司股价明显上涨。一家科技企业创始人的去与留，能在市场上掀起如此波澜，本身就说明了一个问题——创始人的个人影响力，早已不只是一段职业经历，而是企业价值中真实存在的一部分。",
        "这件事从一个侧面提示我们：当创始人的个人形象、声誉与企业的品牌深度绑定，并且这种绑定通过知识产权的方式被确认和保护下来，它对企业和创始人本人，都会产生实实在在的价值。本文就从商标与知识产权的角度，谈谈这种“人与品牌融合”背后的商业逻辑。",
        "一、个人IP的本质：一组可以被“注册”的权利",
        "很多人把个人IP理解成知名度、粉丝量，其实从法律角度看，它是一组具体权利的复合体：姓名、肖像、声音属于人格要素；与创始人相连的专业声誉、价值理念、创业故事，则构成抽象的商业认知资产。这些内容一旦与商业经营结合，就可以通过商标、著作权等方式被固定下来，成为能够授权、转让、计量的权利。",
        "换句话说，个人IP不是虚的。它既可以停留在“个人光环”的状态，也可以被转化为一项权属清晰的企业资产。这两种状态的差别，就是知识产权工作要解决的问题。",
        "二、好处之一：信任背书，让品牌自带识别度",
        "用创始人名字做品牌，最大的优势是天然的可信度。消费者看到一个真实的人名，会本能地联想到“有人在为这个品牌负责”，从而更容易建立信任。对于律师、设计师、咨询顾问、手作匠人这类高度依赖个人专业能力的领域，名字本身就是最好的介绍信。",
        "这种信任感能显著降低市场沟通成本——企业不必从零开始“教育”市场记住一个陌生品牌，创始人的名字和声誉，就是现成的传播入口。",
        "三、好处之二：人与品牌互相成就，形成增值飞轮",
        "个人IP与品牌深度绑定后，会产生一种正向循环：创始人的专业能力和信誉为品牌背书，推动品牌成长；品牌影响力扩大之后，又反过来提升创始人的知名度。两者互相赋能，像飞轮一样越转越快。",
        "我们熟悉的李宁、董明珠等名字，早已超越个人本身，成为一个商业符号。这种“人即品牌、品牌即人”的深度融合，是单纯依靠广告投放难以建立的竞争壁垒。",
        "四、好处之三：关键时刻，成为企业的“信用锚”",
        "回到开头那则新闻。创始人复职的消息公布后，市场用真金白银作出了反应。这背后折射出的，正是公众把创始人的个人能力、声誉与企业前景紧紧绑定在一起——创始人的个人IP，已经成了企业信用的重要组成部分。",
        "当企业遇到波动或关键时刻，一个稳定、正面的创始人形象，能够稳住客户、合作伙伴和市场的信心。这种“信用锚”的作用，是品牌资产中最难被复制的部分。",
        "五、好处之四：从个人光环，变成可计量的企业资产",
        "这是知识产权发挥核心作用的地方。当创始人的姓名、昵称、肖像等被注册为商标，相关创意内容做了版权登记，个人IP就从模糊的“个人影响力”，变成了权属清晰、可以授权和转让的资产。",
        "企业可以与创始人签订知识产权许可协议，明确使用范围、期限与对价，把个人IP合法、稳定地纳入公司体系。这样做有三重价值：对外，它是可以计入企业价值的无形资产；融资时，清晰的权属能减少估值上的不确定性；未来创始人退出或发生股权变动时，品牌也能依据事先约定平稳延续，不至于陷入漫长的归属争议。",
        "六、好处之五：让创始人与企业的长期利益更一致",
        "当个人声誉与企业命运深度绑定，创始人会更珍视企业的长期价值——因为企业的每一次失信、每一次失误，都会直接反映到自己身上。这种利益与名誉的双重绑定，本身就是一种内在的约束和激励，推动创始人把企业往更稳、更远的方向带。",
        "七、话说回来：绑定要用知识产权“做实”",
        "当然，深度绑定是一把双刃剑。个人如果出现负面事件或离开企业，风险也可能直接传导到公司。但这恰恰说明，绑不绑定不是关键，关键是用知识产权把绑定关系规范化：该注册的注册，该登记的登记，该签的许可协议、退出机制提前约定清楚。",
        "把模糊的“个人光环”转化为清晰的“制度安排”，才能既享受绑定带来的红利，又为可能的变化留好出口。这正是专业知识产权服务能够创造价值的地方。",
        "写在最后",
        "黄仁勋复职事件让我们看到，创始人的个人IP早已不是锦上添花的装饰，而是企业核心竞争力的一部分。把这份资产用商标、版权和许可协议固定下来，让它既属于创始人，也能稳定地服务于企业——这是每一家有远见的企业都值得及早考虑的事。",
        "莞促知产扎根东莞松山湖，为企业提供商标注册、版权登记、知识产权布局与风险排查等一站式服务。如果您也在思考如何把创始人或品牌的价值转化为受法律保护的资产，欢迎与我们交流。",
    ],
    "news/n25.html": [
        "企业为什么需要一家知识产权公司？这个问题看似简单，答案却常常被误解。不少企业把知识产权服务理解为“帮我把证办下来”，于是比价格、比速度，证一到手，合作也就结束了。但知识产权真正的价值，从来不在那张证书本身，而在于它能不能成为企业竞争中的护城河、融资时的筹码、维权时的依据。从这个角度看，一家好的知识产权公司，应该是能陪企业把权利“用起来”的公司。",
        "如果我是莞促知产的负责人，我会从以下几个方面，把这件事做实。",
        "一、先听懂企业，再谈方案",
        "知识产权服务最容易犯的错，是上来就推产品。企业说要申请专利，有些机构不问技术背景就报方案，结果保护范围与业务对不上，授权了也用不上。",
        "我会要求团队接案先做诊断：企业处在什么发展阶段，核心技术是什么，主要市场在哪，眼下的保护重点和长期布局分别是什么。把这些问清楚了，再谈申请策略。对企业来说，多的这几次沟通，换来的是方案真正贴合业务；对机构来说，前期慢一点，后面少很多返工。",
        "二、把流程做透明，让每一步都看得见",
        "“交了钱就没人管了”，是很多企业找代理机构时的顾虑。申请材料交上去之后，受理了没有、审到哪一步了、还要补什么，客户往往一无所知。",
        "我会把流程节点做成明确的同步机制：材料清单一次讲清，避免反复补件；受理、审查、公告、授权等关键节点主动告知；遇到补正或审查意见，第一时间说明情况和应对办法。让客户随时知道事情办到哪一步，比任何承诺都更能建立信任。",
        "三、专业的事交给专业的人，对口服务",
        "专利、商标、版权、涉外、维权、科技项目申报，每一项都有自己的专业门槛和规则细节。一个顾问包打天下，看似方便，实际上容易在细节上出问题。",
        "我会按业务类型匹配对应团队：专利由熟悉技术的代理人处理，商标由熟悉审查实务的顾问跟进，涉外和维权这类复杂业务交给有专项经验的同事。同时坚持一对一顾问全程对接，客户认准一个人，不用在不同部门之间来回跑。",
        "四、不止于确权，更要想着运用和保护",
        "很多企业拿到证书就觉得事情结束了，但权利的价值恰恰在确权之后才开始。专利能不能用于高企认定、商标能不能做质押融资、遇到侵权该怎么维权，这些问题才是企业真正关心的。",
        "我会把服务链条往后延伸：在确权阶段就考虑企业未来的申报与运用需求，把高新技术企业认定、知识产权贯标、质押融资、侵权维权这些环节打通，让知识产权从“一张证书”变成“一项能产生效益的资产”。",
        "五、守住底线：保密与诚信",
        "知识产权服务接触的是企业最核心的技术和商业秘密。这份信任，是行业立身的根本。",
        "我会把保密作为硬要求：与客户签订规范的保密协议，内部严格限定资料接触范围，技术交底材料专人管理。同时坚持诚信执业，能做到的才承诺，做不到的如实说明，不夸大授权概率，不承诺不切实际的结果。短期看可能会“丢单”，长期看换来的是客户的放心和转介绍。",
        "六、长期陪伴，把后续事项管起来",
        "知识产权不是一锤子买卖。商标注册后有续展，专利授权后有年费，企业名称、地址变更要及时办理手续。这些后续事项一旦遗漏，权利就可能失效。",
        "我会为每一家客户建立服务档案，把续展、年费、变更这些时间节点纳入日常提醒，定期回访了解企业新的需求。企业成长到不同阶段，遇到的问题不一样，服务机构也应该跟着一起往前走。",
        "写在最后",
        "一家好的知识产权公司是什么样？规模大不大、价格低不低，都不是最关键的。关键是当企业在确权、维权、申报上遇到问题时，第一个想到的是“找他们，我放心”。",
        "莞促知产扎根东莞松山湖，作为莞促集团旗下专注知识产权与科技申报的机构，想做的正是这样一家公司——把专业做深，把服务做细，陪企业走得更远。",
    ],
    "news/n24.html": [
        "提到知识产权，很多企业最先想到的是申请一个专利，或者注册一个商标。但真正等到需要用的时候才发现：单独的一纸证书，往往解决不了问题。知识产权的价值，不在于零散地拥有几项权利，而在于把它们组织成一套与业务匹配的布局，并配上相应的风险管理。",
        "作为扎根东莞的知识产权服务机构，莞促知产想借这篇文章，用通俗的方式讲清楚两件事：企业到底该怎么做好知识产权布局，又该如何把风险管起来。",
        "一、先弄明白：什么是知识产权布局",
        "布局不是多申请。它指的是企业围绕自身的产品、技术和市场，有目的、有先后、有侧重地安排专利、商标、版权等权利的取得与维护，让它们相互配合，形成一张能覆盖核心业务的保护网。",
        "打个比方，单点申请像是买了一件雨衣，下雨时才想起来穿；而布局像是提前修好屋顶、装好排水系统。前者被动，后者主动。理解了这个区别，才能明白为什么布局要走在业务前面。",
        "二、布局要跟着业务走，而不是跟着清单走",
        "企业常见的误区，是照着别人的清单办：别人申请专利我也申请，别人注册商标我也注册。但每家企业的核心技术、主销产品、目标市场都不一样，合适的布局自然不同。",
        "正确的做法是从业务出发：核心技术在哪里，专利就重点布在哪里；品牌名字用在哪些产品和服务上，商标就覆盖哪些类别；产品卖到哪些地方，权利就延伸到哪些地域。让知识产权的版图和业务的版图对齐，布局才真正有用。",
        "三、把几类权利组合起来用",
        "专利、商标、版权各有各的用处，单靠一种往往不够。专利保护技术方案和产品外形，商标保护品牌和商誉，版权保护软件、设计图和创作成果。成熟的企业会把它们组合起来：用专利守住产品，用商标守住品牌，用版权守住内容，彼此互为补充。",
        "比如一款自主研发的产品，造型可以申请外观设计专利，核心技术可以考虑发明专利，配套软件可以做软件著作权登记，产品名和品牌名则通过商标保护。这样的组合，比单独申请一项权利要牢固得多。",
        "四、风险管理：先看清风险从哪里来",
        "布局解决的是保护自己，风险管理解决的则是别出事、出事能应对。企业的知识产权风险主要有几类：一是侵犯他人权利的风险，比如选品、宣传时无意用了别人的专利或图片；二是自己的权利被侵害，比如被仿冒、被抢注；三是内部管理风险，比如人员流动带来的技术泄密、合同里没有约定清楚权属。",
        "把这些风险点梳理出来，才知道该在哪里设防。风险管理不是等纠纷上门才启动，而是体现在日常的每个环节里。",
        "五、把风险管理嵌进日常经营",
        "有效的风险管理，靠的是制度和习惯。莞促知产通常会建议企业做好几件事：在产品上市、对外宣传之前做侵权排查，避免无意侵权；与员工、合作方签订规范的保密与权属约定，把技术成果的归属写清楚；建立商标、专利的监测机制，发现近似申请或侵权行为及时应对；妥善保存研发记录、设计底稿等证据，一旦发生纠纷拿得出材料。",
        "这些做法看起来琐碎，但正是它们决定了企业在关键时刻是被动挨打，还是从容应对。",
        "六、布局和管理都要动态调整",
        "企业的业务在变，知识产权也不能一成不变。新产品推出、新市场开拓、业务方向调整，都会带来新的布局需求；权利的续展、维持、放弃，也需要定期梳理。把知识产权当成一次性工作，往往几年后就和现实业务脱节了。",
        "比较稳妥的做法，是为知识产权建立台账，把各项权利的状态、期限、覆盖市场统一管理，并定期回顾。业务有变化时，同步评估布局是否需要补充或调整。",
        "写在最后",
        "知识产权布局和风险管理，本质上是一件事的两面：布局是把权利建设好，风险管理是让这些权利真正安全、能用。对成长中的企业来说，早一点建立意识、早一点动手规划，成本更低，效果也更好。",
        "莞促知产扎根东莞松山湖，为企业提供从专利、商标、版权申请，到布局规划、风险排查与维权应对的一站式知识产权服务。希望这篇科普，能帮您把企业的知识产权这件事想清楚、做扎实。",
    ],
    "news/n23.html": [
        "跨境电商有个和其他贸易方式很不一样的特点：上架快、铺货多、平台规则说了算。一个爆款做起来，可能很快冒出一批跟卖；一个投诉进来，链接说下就下，货款还可能被冻结。很多卖家吃过亏之后才明白——在这条赛道上，知识产权不是“有了更好”，而是“没有不行”。",
        "如果我是莞促知产的负责人，我会帮跨境电商企业把知识产权布局嵌进经营的每个环节，而不是等出事了再补救。具体会做下面这几件事。",
        "一、选品阶段先把侵权风险排掉",
        "很多卖家的选品逻辑是看销量、看利润，却很少先看权利。等货备好了、图片拍好了，才发现产品外观有专利、品牌名称已被注册，或者图上用了别人的作品，前面的投入全打了水漂。",
        "我会把侵权排查前置到选品环节：核对产品是否涉及他人的外观设计专利、发明或实用新型专利，确认拟用的品牌名、关键词是否与他人商标近似，检查产品图片、包装图案是否可能侵犯他人著作权。排查清楚再决定上不上，比上架后被投诉下架要划算得多。这一步看着慢，其实是在给后面的销售省麻烦。",
        "二、商标是品牌备案的钥匙，先注册再开卖",
        "跨境电商做品牌，绕不开平台的品牌备案。而备案的前提，是你在目标市场要有合法的商标权利。没有商标，就无法完成品牌备案，也难以享受平台的品牌保护工具，被跟卖时更是缺少有力的维权依据。",
        "我会建议企业把商标注册放在开店之前：根据主要销售市场确定注册国家和类别，核心市场优先、重点类别全覆盖；同时按平台要求准备规范的商标注册证明，确保能顺利完成备案。对已经开卖但还没商标的卖家，尽快补注册，越早拿到权利，越早掌握主动。",
        "三、产品本身要有专利护城河",
        "爆款最怕被仿。产品卖得好，仿品很快跟上，价格被压、评价被摊薄，前期打市场的投入替别人做了嫁衣。",
        "我会根据企业产品的特点来设计专利布局：造型、结构有独创性的，考虑申请外观设计专利和实用新型专利；核心技术有门槛的，考虑发明专利。对重点市场，还要结合当地规则做好海外专利布局。让专利真正成为拦住仿品的护城河，而不是抽屉里一张用不上的证书。",
        "四、图片、文案与店铺设计，版权也要管",
        "电商侵权里有一类特别容易被忽视：图片和文案。随手从网上找的产品图、参考文献里的技术描写、照搬别家的详情页设计，都可能埋下著作权侵权的隐患，一旦被投诉，同样会被下架甚至追责。",
        "我会提醒企业建立内容使用的规范：产品图片尽量自主拍摄，委托设计的作品约定清楚著作权归属，引用的文字、素材确认授权或属于合理使用范围。把版权管理做成日常习惯，避免因为一张图、一段文案毁掉一个链接。",
        "五、多平台多站点，权利覆盖要跟上",
        "不少卖家一开始只做一个平台、一个站点，做起来之后迅速铺开多个平台、多个国家。但商标和专利都是有地域范围的，在一个国家注册的权利，管不到另一个国家的市场。",
        "我会帮企业按业务扩张的节奏同步扩展权利：每进入一个新的国家或平台，先核对当地是否已有相应商标与专利保护，需要补的及时补上。让知识产权的版图和销售版图同步扩大，不留下一块“卖得出去却护不住”的市场。",
        "六、被跟卖、被投诉，要有现成的应对预案",
        "跨境电商的纠纷往往来得突然：被恶意跟卖、被竞争对手投诉侵权、链接被下架、资金被冻结。临时找人、临时准备材料，通常会错过最佳处理时机。",
        "我会帮企业提前备好应对机制：整理完整的权利证明和授权链条，熟悉各平台的投诉与申诉流程，准备好规范的反应材料。做到平时有准备、出事能快速响应，把每一次纠纷对经营的影响降到最低。",
        "七、把知识产权纳入日常运营",
        "知识产权布局不是做一次就结束了。商标要续展、专利要维持、新品的权利要跟着上、平台的规则也在不断变化。",
        "我会为电商企业建立知识产权台账，把各项权利的状态、期限、覆盖市场统一管理，定期跟进平台规则和目标市场的政策变化，在新品上架、开拓新站点之前提前给出布局建议。让知识产权成为运营的一部分，而不是出事时才翻出来的救火工具。",
        "写在最后",
        "跨境电商的竞争，表面看是选品、运营和价格的竞争，往后拼的是规则的掌控力。谁把知识产权布局做在前面，谁就少踩坑、走得稳。",
        "莞促知产扎根东莞松山湖，为企业提供从商标专利布局、平台备案支持到侵权维权的一站式知识产权服务。我们想做的，就是跨境电商路上那个懂平台、懂规则的知识产权伙伴——让企业安心铺货、放心出海。",
    ],
    "news/n22.html": [
        "东莞是制造业外向度很高的城市，越来越多企业把产品卖到海外、把品牌带到海外。但出海这条路，机遇之外还有一道容易被忽视的门槛——知识产权。商标在目标市场被抢注、产品在海关被扣押、收到海外侵权投诉，这些情况一旦发生，往往让企业措手不及，前期投入的市场成果也可能一夜清零。",
        "知识产权不是出海之后才要考虑的事，而应该在出发之前就布局好。如果我是莞促知产的负责人，我会从以下几个方面，帮企业把出海路上的知识产权这道关口守牢。",
        "一、出海之前，先做一次知识产权体检",
        "很多企业的习惯是先把货发出去、把渠道铺开，等做大了再补知识产权。这个顺序其实很危险：市场未动、权利先行，才是出海的正确打开方式。",
        "我会要求团队在企业出海前先做一次系统的知识产权体检：梳理企业现有的专利、商标、版权状况，核对权利的地域覆盖范围与目标市场是否匹配，排查是否存在权利空白或权属不清的问题。同时结合企业要进入的国家与产品方向，评估侵权风险，判断哪些技术需要先做自由实施分析。体检清楚了，后续布局才有依据，不至于花了钱却保护不到点子上。",
        "二、商标先行，把品牌名字先占住",
        "品牌出海最常见也最痛的坑，是商标被抢注。等到企业在海外市场做出名气，才发现商标早已被他人注册，轻则高价回购、重则被迫改名，多年积累毁于一旦。",
        "我会建议企业把商标布局前置：根据目标市场数量和预算，选择合适的注册路径——通过马德里体系做多国覆盖，或对重点市场逐一单独申请。核心类别要注册，关联类别和防御性类别也要一并考虑。同时提醒企业做好商标监测，一旦发现近似申请及时提出异议，把风险挡在萌芽阶段。",
        "三、专利跟着市场走，布局要算清楚账",
        "专利布局不是申请得越多越好，而是要和产品、市场节奏对得上。产品主销到哪里，专利就要覆盖到哪里；产品迭代到哪一代，保护就要跟到哪一代。",
        "我会帮助企业结合海外市场的销售规划确定专利策略：重点市场通过 PCT 途径或巴黎公约途径进入国家阶段，把核心技术、外观设计和实用新型按照各地规则分别布局。同时做好申请时机的把控，避免因公开过早或错过期限而丧失权利。让每一笔专利投入，都真正服务于企业的海外市场保护。",
        "四、提前备好纠纷应对机制",
        "出海企业遇到知识产权纠纷的概率远高于本土经营，可能是平台上的侵权投诉，也可能是海关的查验扣货，还可能是竞争对手的诉讼。临时抱佛脚，往往被动又昂贵。",
        "我会协助企业提前建立应对机制：办理知识产权海关备案，让权利在口岸就具备保护基础；整理好权利证明与授权链条，做到有备可查；针对电商平台的投诉与申诉，准备好规范的应对材料。一旦发生纠纷，专业团队能够快速响应，帮企业把损失控制在最小范围。",
        "五、把合规与运营一并做进去",
        "知识产权出海不只是申请两个字，还涉及目标市场的法律规则、数据合规、许可转让、关税与认证环节的知识产权要求。这些细节处理不好，同样会给企业带来麻烦。",
        "我会把服务延伸到确权之后：协助企业梳理不同市场的合规要求，做好专利商标的许可备案、权属变更与年费维持，帮助企业把海外知识产权作为资产进行管理和运营。让知识产权既能保护产品，也能在融资、合作、转让时创造价值。",
        "六、做长期陪伴的知识产权顾问",
        "企业的海外市场是逐步铺开的，知识产权布局也应该跟着节奏走。今天进入一个市场，明天多一条产品线，遇到的新问题会不断变化。",
        "我会为出海企业建立专门的知识产权档案，把各地权利的期限、范围、状态统一管理，定期跟进海外政策与规则变化，在企业进入新市场、推出新产品时提前给出布局建议。企业专注开拓海外业务，专业的知识产权后盾由我们来做。",
        "写在最后",
        "企业出海，拼的不只是产品和价格，更是规则和权利。谁把知识产权准备在前面，谁就能在海外的激烈竞争中少踩坑、走得稳。",
        "莞促知产扎根东莞松山湖，依托集团资源，为企业提供从专利申请、商标注册、PCT 国际布局到海外维权的一站式知识产权服务。我们想做的，就是企业出海路上那个值得信赖的知识产权伙伴——让企业放心走出去，把成果稳稳留下来。",
    ],
    "news/n21.html": [
        "2026年11月21日，第一届2026年“东莞市常平个体私营企业协会杯”篮球邀请赛在常平举行。本次赛事由东莞市常平个体私营企业协会主办，莞促集团有限公司赞助支持，以篮球为纽带，为本地企业与各界人士搭建交流互动的平台。莞促知产所在的莞促集团全程参与，与协会会员企业共赴这场活力之约。",
        "一、启动仪式与出席嘉宾",
        "赛事启动仪式上，常平镇赵宁发副镇长跳球开球，为比赛拉开序幕。东莞市市场监督管理局常平分局杜遵凯副局长，东莞市常平个体私营企业协会会长、莞促集团董事长谭喜，协会党支部书记李达豪、秘书长彭东正，协会副会长李海南出席活动。莞促集团有限公司员工到场助阵，集团党支部委员孙晓君出席。",
        "二、董事长谭喜：以体育为桥，凝聚企业力量",
        "作为东莞市常平个体私营企业协会会长，同时也是莞促集团董事长，谭喜在活动现场表示，篮球赛所体现的团队协作与拼搏精神，与企业经营发展中所倡导的携手共进高度契合。协会举办篮球邀请赛，为会员企业搭建了体育交流的平台，有助于增进彼此了解、凝聚发展合力。莞促集团赞助支持本次赛事，正是希望以实际行动支持地方企业文化建设，助力营造积极、健康、向上的营商氛围。他寄语参赛队伍赛出水平、赛出风格，把赛场上的拼搏精神转化为推动企业发展的动力。",
        "三、赛场风采与交流互动",
        "比赛过程中，各参赛队伍奋勇争先、配合默契，攻防转换间展现出良好的竞技状态与团队精神。莞促集团代表队与常平个私协等队伍同场竞技，在赛场上切磋球技、增进友谊。赛场内外，企业代表与员工朋友交流互动，气氛热烈，充分展现了常平企业家群体昂扬向上的精神风貌。",
        "四、莞促知产：与集团一同扎根常平、服务企业",
        "作为莞促集团旗下专注知识产权与科技申报服务的机构，莞促知产始终与集团一同扎根常平、服务本地企业。本次集团赞助支持协会杯篮球邀请赛，是莞促集团积极履行社会责任、参与地方经济文化建设的又一体现。莞促知产也将继续以专业的专利、商标、版权及高新技术企业认定服务，陪伴企业稳健成长，与企业共同迸发活力。",
    ],
    "news/n19.html": [
        "在东莞办理商标注册，按流程分步推进可以减少反复。本文梳理从注册前查询到最终领证的各个环节，以及每一步需要准备的材料，供企业在安排商标布局时参考。具体受理要求以国家知识产权局商标局的最新规定为准。",
        "一、注册前的查询准备",
        "提交申请前，建议先做近似查询：在与拟注册商标相同或近似的类别中，排查是否有在先注册或在先申请的相同或近似标志，同时留意字号、作品名称等可能构成在先权利的情形。查询还应结合企业当前业务与后续拓展方向确定类别与商品服务项目。相关判断方法可参考本站<a href=\"/service-trademark.html\">商标服务</a>栏目，或联系专业顾问协助分析。",
        "二、准备申请材料",
        "企业申请通常需准备营业执照等主体资格证明、清晰的商标图样、指定的类别与商品服务项目，以及委托代理时签署的委托书。以自然人名义申请的，需按现行规定提供相应的经营主体证明。材料中的名称、地址应与主体证明文件保持一致，避免因信息不一致产生补正。",
        "三、提交申请与受理",
        "材料齐备后可通过线上或线下渠道提交。商标局对申请文件进行形式审查，符合要求的发出受理通知；若存在填写不规范、材料缺失等情形，会要求限期补正。这一阶段的核心是把形式问题解决在前面，让申请顺利进入实质审查。",
        "四、实质审查与初步审定公告",
        "通过受理后，申请进入实质审查，审查员会判断标志是否具备显著性、是否违反禁用条款、是否与在先权利冲突。审查通过的，进入初步审定公告程序，公告期内利害关系人可依法提出异议。企业在此期间应留意公告动态，及时回应可能出现的异议。",
        "五、核准注册与领证",
        "公告期满无异议或异议不成立的，商标局核准注册并下发商标注册证。取得注册后，应按规定规范使用，并留存实际使用证据；后续如发生名称地址变更、转让或许可，应及时办理相应手续。注册并非一劳永逸，企业应将续展等后续事项纳入日常管理。",
    ]
    ,
    "news/n20.html": [
        "发明专利、实用新型专利与外观设计专利在授权路径上差别明显：发明需要经过实质审查，实用新型与外观设计主要经过初步审查。理解这些阶段差异，有助于企业结合技术特点与需求选择合适的申请类型。具体审查标准以国家知识产权局的现行规定为准。",
        "一、三类专利共同的起点",
        "三种专利都从申请提交开始，经形式审查后由专利局受理并给出申请号。申请文件的完整性与撰写质量，会直接影响后续审查的顺畅程度。技术交底充分、权利要求布局清楚的申请，往往更利于审查员理解技术方案。相关撰写要点可参考本站<a href=\"/service-patent.html\">专利服务</a>栏目。",
        "二、发明专利的授权路径",
        "发明专利申请经初步审查合格后进入公布阶段，申请人需在规定期限内提出实质审查请求。实质审查围绕新颖性、创造性与实用性展开，审查员可能发出审查意见通知书，申请人需按要求答复或修改。审查意见答复并通过后进入授权登记与公告。",
        "三、实用新型专利的授权路径",
        "实用新型专利申请主要经过初步审查，审查重点在于文件格式、明显缺陷与是否符合授权条件，一般不进行全面的实质审查。通过初步审查后即可办理授权登记。由于其保护的是产品的形状、构造，企业申报时应围绕具体产品结构准备材料。",
        "四、外观设计专利的授权路径",
        "外观设计专利申请同样以初步审查为主，审查重点是图片或照片是否清楚、是否符合表示要求，以及是否明显不具备新颖性。通过审查后进入授权公告。申请时应提交能够清楚显示设计要点的视图，必要时附简要说明。",
        "五、三类流程的关键差异",
        "是否经过实质审查，是三类流程最核心的区别：发明的权利稳定性建立在实质审查基础上；实用新型与外观设计授权较快，但后续维权时可能需要补充权利评价材料。企业可结合技术生命周期、保护紧迫程度与维权需求作出选择，必要时可同时布局多种类型。",
    ]
    ,
    "news/n01.html": [
        "为方便企业及时了解自有知识产权状况，广东莞促知识产权代理事务所（普通合伙）即日起开通商标、专利免费检索与初步评估服务，面向有需求的企业与创业者开放。",
        "一、服务内容",
        "商标检索：围绕拟申请商标进行近似查询与可注册性初步判断，提示潜在风险；专利检索：针对技术方案提供现有技术检索与初步分析，辅助判断申请方向；初步评估：结合企业业务类型与发展需求，给出保护方式的初步建议。",
        "二、参与方式",
        "有需要的企业可通过本所官方公布的电话、微信或邮箱，说明姓名、联系方式、业务类型与基本情况，我们将安排专业顾问与您对接。咨询过程严格保密，相关信息仅用于本次检索与评估。",
        "三、其他说明",
        "免费检索与初步评估不构成正式的法律意见或检索报告，具体申请方案以专业顾问结合完整材料出具的意见为准。本所保留对服务内容进行调整的权利。",
    ],
    "news/n02.html": [
        "2026 年 6 月 26 日，十四届全国人大常委会第二十三次会议审议通过新修订的《中华人民共和国商标法》，这是商标法施行四十多年来首次全面修订。新法由原来的 8 章 73 条增加为 9 章 87 条，对篇章结构和条款内容作了较大调整。",
        "一、拓宽商标可注册要素",
        "新法增设专章集中规定商标注册条件，积极适应移动互联网和数字化传播技术的发展，增加规定动态标志及其与相关要素的组合可以作为商标申请注册，回应新技术、新业态企业的需求。",
        "二、完善注册条件与使用规范",
        "新法明确通过互联网等信息网络实施的商标使用行为属于法律调整范围，同时进一步严格规范商标注册条件，对特定标志性要素、以颜色组合或声音等申请注册的情形作出规定。",
        "三、对企业的启示",
        "建议企业在品牌布局时关注新法变化，及时评估现有商标与拟申请标志的合规性，规范网络环境下的商标使用，必要时借助专业机构完善注册与保护方案。",
    ],
    "news/n03.html": [
        "新版《专利优先审查管理办法》自 2026 年 9 月 1 日起施行。新版办法立足高质量创新需求，对优先审查的适用条件、管控体系与办事流程作出系统修订。",
        "一、优化适用范围",
        "办法明确优先审查适用于未作出首次处理的发明专利实质审查申请、实用新型与外观设计专利申请，以及三类专利的复审、无效宣告案件；同时厘清制度边界，避免与专利预审等场景混淆。",
        "二、升级准入标准",
        "新版办法摒弃固定产业目录限制，重点聚焦新兴产业、未来产业与关键核心技术攻关领域的高质量专利申请，从“形式合规”转向“实质价值匹配”。",
        "三、强化质量与诚信约束",
        "办法首次明确四类一般不予优先审查的情形，压实专利代理机构服务责任，并对提交虚假材料、违背诚信原则的申请人及代理机构设置相应惩戒措施。",
    ],
    "news/n04.html": [
        "东莞市知识产权保护中心发布通知，正式启动专利申请预审服务备案主体预备案及专利代理机构预注册工作，为保护中心正式运行后的专利快速预审服务做好前置准备。",
        "一、申报领域与时间",
        "本次申报面向智能终端、新材料两大产业领域开放。符合条件的创新主体和专利代理机构可按通知要求自愿申报。具体申报时间与要求以东莞保护中心官方通知为准。",
        "二、预审服务的意义",
        "东莞保护中心获批建设国家级知识产权保护中心，待通过国家知识产权局验收后正式投入运行，将重点为本地优势产业提供专利申请快速预审、快速确权、快速维权及导航运用等全链条服务。",
        "三、对企业的建议",
        "属于相关产业领域的企业可关注备案通知，按要求准备材料并完成注册备案，以便保护中心正式启用后高效享受专利预审服务，缩短专利授权周期。",
    ],
    "news/n07.html": [
        "11 月 11 日下午，莞促集团一行走进投资企业东莞市昂图智能科技有限公司（ORTUR），从产品知识培训到设备实操，从展厅参观到座谈交流，近距离感受桌面级数字创意设备的技术积累。",
        "一、技术积累与产品体系",
        "公开资料显示，昂图智能成立于 2016 年，专注桌面级数字创意设备的研发、生产与销售，产品覆盖激光雕刻机、3D 打印机、CNC 雕刻机等品类，销往海内外市场。",
        "二、交流与合作",
        "双方围绕技术、产品与后续合作展开沟通，并就企业服务资源与智能制造产品之间的互补空间进行探讨，表达继续围绕产品应用、渠道与市场资源协同的意愿。",
        "三、集团视角",
        "莞促集团表示，此行进一步增强了持续关注智能制造赛道的信心，将继续以互学互鉴推进共同成长。作为集团旗下知识产权板块的承接机构，本所也将持续关注制造与智能制造企业的知识产权保护需求。",
    ],
    "news/n11.html": [
        "商标申请看似只是提交一个标志，真正决定成败的往往是申请前的判断。充分的检索准备，可以帮助企业避开明显的在先权利障碍，减少后续驳回与复审的时间成本。",
        "一、先做近似查询",
        "围绕拟申请的标志，在相同及关联类别中检索相同或近似的在先商标，同时关注驰名商标、字号、作品名称等可能构成在先权利的情形。检索时应把文字的字形、读音、含义以及图形的整体外观一并纳入比较。",
        "二、再确定类别与商品项目",
        "商标保护以核定使用的商品或服务为范围。企业应结合当前业务与未来拓展方向确定类别，并选择表述规范、覆盖范围适当的项目，避免类别过窄导致保护不到位。",
        "三、留存检索判断记录",
        "对检索结论、风险判断与最终申请方案形成书面记录，有助于后续遇到审查意见或异议时快速回溯决策依据。",
    ],
    "news/n12.html": [
        "企业计划到多个国家使用同一品牌或技术方案时，逐国分别提交申请往往成本较高、节奏难统一。PCT 途径提供了一次国际申请、多国后续进入的办理框架。",
        "一、国际阶段",
        "申请人可在中国国家知识产权局提交 PCT 国际申请，由受理局完成国际检索并出具国际检索报告，帮助申请人初步判断发明的新颖性与创造性。国际阶段不直接产生授权，但为后续决策提供参考。",
        "二、国家阶段",
        "申请人通常在优先权日起 30 个月内，决定进入哪些国家或地区，并按各局要求提交译文、缴纳费用，由各国专利局独立审查并决定是否授权。",
        "三、适用情形",
        "目标国家较多、需要争取更长决策时间的技术方案，通常更适合考虑 PCT 途径；若目标明确且数量较少，也可比较巴黎公约途径的时效与成本。",
    ],
    "news/n13.html": [
        "著作权自作品创作完成之日起自动产生，并不以登记为前提。但登记证书在维权、授权和商业合作中，往往能起到简化举证的作用。",
        "一、登记的实际价值",
        "在发生侵权争议时，登记证书可作为权利归属的初步证据；在企业融资、并购、版权交易或平台投诉场景中，权属证明也有助于提高沟通效率。",
        "二、常见登记对象",
        "软件代码、图文设计、宣传文案、摄影作品、短视频脚本与美术形象等，都可能构成受著作权保护的作品。企业应结合业务类型梳理可登记的作品清单。",
        "三、材料准备提示",
        "申请时需提交作品样本、权利归属说明等材料。委托创作、职务作品的权属应提前通过合同明确，避免登记时产生争议。",
    ],
    "news/n14.html": [
        "商标公告期内，利害关系人认为申请商标违反相关规定，可以提出异议；商标注册后，符合条件的主体也可依法请求宣告无效。两类程序都有严格的期限与证据要求。",
        "一、异议的提出与答辩",
        "初步审定公告的商标在三个月公告期内可被提出异议。被异议人应在规定期限内提交答辩材料，围绕在先权利、显著性与使用事实等要点进行回应。",
        "二、无效宣告的适用",
        "已注册商标存在违反禁用条款、以不正当手段取得注册等情形的，可依法请求宣告无效。涉及在先权利冲突的，还需注意五年等期限规定。",
        "三、证据准备思路",
        "无论是提出还是应对，都应围绕权利基础、使用证据与市场混淆可能性组织材料。及时监测公告、保留使用痕迹，是企业降低应对成本的基础。",
    ],
    "news/n15.html": [
        "专利申请获得授权后，并非“一劳永逸”。年费缴纳、权利状态跟踪与变更手续，直接关系到专利能否持续有效。",
        "一、年费缴纳期限",
        "发明专利、实用新型与外观设计专利在授权后均需按规定逐年缴纳年费。未按期缴纳的，可在宽限期内补缴并缴纳滞纳金；逾期仍未办理的，专利权将终止。",
        "二、权利恢复与状态核查",
        "因不可抗力或正当理由耽误期限的，可在规定期限内办理恢复权利手续。建议企业建立专利台账，定期核对法律状态、权利人信息与联系方式。",
        "三、放弃与维持的判断",
        "对技术已迭代或与业务关联度降低的专利，可结合成本与风险决定是否继续维持；对核心专利，则应避免因流程疏漏造成权利失效。",
    ],
    "news/n16.html": [
        "高新技术企业认定对知识产权有明确要求，企业准备的重点不只是“有没有证书”，还包括权属是否清晰、与主营业务是否匹配、能否支撑成果转化。",
        "一、关注权属与有效性",
        "用于申报的知识产权应与申报企业权属一致，且处于有效状态。通过受让取得的权利，应完成著录项目变更并保留完整证明材料。",
        "二、体现与主营业务的关联",
        "知识产权应能对企业主要产品或服务发挥核心支持作用。建议在材料中说明技术对应的产品、应用场景及产生的经济价值。",
        "三、重视成果转化材料",
        "研发立项、试验记录、产品上市与销售数据等，共同构成成果转化的证据链。具体指标与分值以当年认定管理工作指引为准。",
    ],
    "news/n17.html": [
        "《企业知识产权管理规范》提供了一套可落地的管理框架。贯标的意义在于把知识产权要求嵌入业务流程，而不是停留在文件层面。",
        "一、把管理要求嵌入业务",
        "在研发立项前开展专利检索，在采购环节明确技术成果归属，在销售与参展前核查商标与宣传用语，都是贯标强调的过程控制点。",
        "二、形成可追溯的记录",
        "体系运行依赖完整记录：检索报告、评审意见、合同知识产权条款、侵权监测台账等，既是内部管理依据，也是外部审核与纠纷应对的基础材料。",
        "三、持续改进",
        "贯标并非一次性项目。企业应通过内审与管理评审发现问题，结合业务变化调整流程，使知识产权管理真正服务于经营目标。",
    ],
    "news/n18.html": [
        "商业秘密不像专利那样公开换保护，其成立前提是信息不为公众所知悉、具有商业价值，并且权利人采取了相应保密措施。制度建设是其中关键一环。",
        "一、明确保密范围与措施",
        "企业应对技术配方、客户名单、经营数据等信息分级管理，通过制度文件、访问权限、标识标注与物理隔离等方式落实保密措施。",
        "二、管好人员与合同",
        "与员工、供应商及合作方签订保密条款，对涉密岗位做好入职与离职管理。人员流动频繁的岗位，尤其要及时回收权限并提示保密义务。",
        "三、留存侵权证据",
        "发现泄密迹象时，应及时固定证据，包括接触记录、文件流转痕迹与公开使用情况。必要时可通过行政投诉或民事诉讼途径主张权利。",
    ],
}

# 文章正文配图（流程图信息图）：紧跟首段插入，完整显示、不裁切
ARTICLE_IMAGES = {
    "news/n44.html": ("assets/img/covers/trademark-renewal-guide.jpg", "商标续展办理示意图：从权利核对、材料准备到提交审查与核准公告"),
    "news/n45.html": ("assets/img/covers/patent-enforcement-guide.jpg", "专利维权步骤示意图：从权利核查、侵权比对、证据固定到路径选择"),
    "news/n46.html": ("assets/img/covers/design-patent-guide.jpg", "外观专利申请图片准备示意图：成套视图、拍摄规范与简要说明"),
    "news/n41.html": ("assets/img/covers/trademark-enforcement-guide.jpg", "商标维权步骤示意图：从线索核查、证据固定、权利核对到维权路径选择"),
    "news/n42.html": ("assets/img/covers/software-copyright-guide.jpg", "软件著作权登记材料示意图：主体材料、源代码与文档三部分的准备要点"),
    "news/n43.html": ("assets/img/covers/overseas-trademark-guide.jpg", "海外商标注册路径示意图：单一国家申请、马德里体系与地区注册三种方式"),
    "news/n40.html": ("assets/img/covers/brand-boundary-guide.jpg", "商标专用权与历史叙事权边界示意图：客观讲述历史有空间，商业标识使用有红线"),
    "news/n19.html": ("assets/img/covers/seo-trademark-guide.jpg", "商标注册流程示意图：从注册前查询到核准领证的五个步骤"),
    "news/n20.html": ("assets/img/covers/seo-patent-timeline.jpg", "三种专利授权流程对比：发明、实用新型与外观设计的各阶段"),
}

# 活动纪实类文章：多张实拍图集，正文按序完整展示
ARTICLE_GALLERY = {
    "news/n21.html": [
        ("assets/img/news/game-opening.jpg", "2026年“东莞市常平个体私营企业协会杯”篮球邀请赛启动仪式现场，嘉宾与各参赛队伍合影"),
        ("assets/img/news/game-score.jpg", "赛场计分牌：莞促集团代表队对阵常平个私协代表队"),
        ("assets/img/news/game-teams.jpg", "参赛队伍赛后合影"),
        ("assets/img/news/group-photo1.jpg", "莞促集团有限公司员工出席活动"),
        ("assets/img/news/group-photo2.jpg", "莞促集团有限公司员工在活动现场合影"),
    ],
}

# 文章 FAQ：既渲染问答区块，也生成 FAQPage 结构化数据（利于搜索富摘要）
ARTICLE_FAQS = {
    "news/n44.html": [
        ("商标续展是重新申请一件新商标吗？", "不是。续展是延长原有注册商标专用权的期限，与原注册号、核定类别和项目对应，不需要重新走完整的注册申请流程。"),
        ("办理续展前要核对什么？", "重点核对注册人名称与地址是否和登记记录一致、核定类别项目是否覆盖现有业务、是否收到过异议或撤销通知，以及联系方式是否有效。"),
        ("企业名称变了，可以直接办续展吗？", "建议先办理商标名义变更，使登记记录与营业执照一致，再办续展，避免因信息不一致被要求补正。"),
        ("续展会因为材料问题被退回吗？", "会。常见原因是申请书信息与登记记录不一致、委托手续不完整、类别遗漏或通知收不到。提前按清单核对，多数情况可以避开。"),
        ("莞促知产在商标续展方面能提供什么帮助？", "莞促知产扎根东莞松山湖，可协助核对权利状态、准备续展材料，并为企业名下多件商标建立台账、管理续展节点。"),
    ],
    "news/n45.html": [
        ("发现专利被侵权，第一步做什么？", "先核查自己的专利是否有效、年费是否缴纳、权利要求是否稳定。权利底牌不清，后续投诉或诉讼容易被动。"),
        ("怎么判断对方产品是否落入专利保护范围？", "需要把被诉产品或方法与专利权利要求逐项比对，看是否覆盖全部技术特征；外观设计则比较整体视觉效果。应针对具体产品型号分析。"),
        ("专利维权一定要起诉吗？", "不一定。可以根据情况选择协商、电商平台投诉、请求管理专利工作的部门处理或提起侵权诉讼，几种方式也可组合使用。"),
        ("对方提出专利无效怎么办？", "这是常见抗辩方向。应提前评估专利稳定性、准备相应材料，并在专业指导下应对无效程序与侵权程序的衔接。"),
        ("莞促知产在专利维权方面能提供哪些帮助？", "莞促知产扎根东莞松山湖，可协助核查权利状态、开展侵权比对、整理证据清单、制定维权路径，并提供无效应对与行政诉讼衔接支持。"),
    ],
    "news/n46.html": [
        ("外观专利和发明、实用新型有什么区别？", "外观设计保护产品外形带来的视觉效果，发明和实用新型保护技术方案。想保护形状、图案、色彩的新设计，应申请外观专利。"),
        ("外观专利申请要提交哪些视图？", "通常需要提交能清楚显示设计要点的成套视图，一般包括正、背、左、右、顶、底等角度及立体图，具体以产品类型和设计要点为准。"),
        ("图片里能出现商标或文字吗？", "除非这些元素本身就是设计要点并已说明，否则不建议出现。无关的商标、文字、水印或标签会影响保护范围的清晰度。"),
        ("简要说明有什么作用？", "简要说明用于解释图片、指明设计要点，并说明是否要求保护色彩等事项。内容应与图片一致，避免使用宣传性语言。"),
        ("莞促知产如何帮助企业申请外观专利？", "莞促知产扎根东莞松山湖，可协助判断产品是否适合申请、梳理所需角度、规范图片与简要说明，并给出外观与发明、实用新型组合保护建议。"),
    ],
    "news/n41.html": [
        ("发现商标被仿冒，第一步应该做什么？", "先固定证据：完整保存侵权页面、链接、商品实物、票据与交易记录，必要时通过可信方式保全，避免对方下架或销毁后无据可查。"),
        ("商标维权一定要起诉吗？", "不一定。可以根据侵权规模和证据情况选择与对方协商、向平台投诉、向市场监督管理部门举报或提起侵权诉讼，几种方式也可以相互衔接。"),
        ("平台投诉和法院起诉可以同时进行吗？", "可以。平台投诉适合快速制止链接传播，行政程序形成的材料可为后续诉讼提供证据；建议提前统一事实陈述与证据口径。"),
        ("索赔金额怎么确定？", "应结合侵权情节、自身销售与许可情况、维权合理支出等材料提出主张，并保留相应凭证，避免空泛报价。"),
        ("莞促知产在商标维权方面能提供什么帮助？", "莞促知产扎根东莞松山湖，可协助核查权利状态、整理证据清单、分析侵权线索、制定维权路径，并提供商标监测与行政投诉等专业支持。"),
    ],
    "news/n42.html": [
        ("软件著作权登记是必须办理的吗？", "著作权自作品完成之日起产生，登记并非权利产生的前提。但登记证书是证明权利归属的重要凭证，在融资、项目申报、软件上架和维权举证时具有实际价值。"),
        ("登记需要准备哪些材料？", "一般需要源代码、软件说明书或设计文档、申请人身份材料与登记表；委托办理的还需委托书。各部分名称、版本号与主体信息应保持一致。"),
        ("源代码提交有什么要求？", "应前后连续、逻辑完整，能体现软件实际内容，避免只提交零散片段，也不要带入与申请主体无关的第三方信息。"),
        ("软件著作权和专利能同时申请吗？", "两者保护对象不同：著作权保护代码表达，专利保护符合授权条件的技术方案。企业可根据软件特点分别规划，互不影响。"),
        ("莞促知产能提供哪些软著方面的帮助？", "莞促知产扎根东莞松山湖，可协助判断登记必要性、梳理材料清单、规范源代码与文档表述，并从版权、专利、商标整体保护角度给出组合建议。"),
    ],
    "news/n43.html": [
        ("在国内注册了商标，海外能用吗？", "商标权具有地域性，国内注册不会自动在境外产生权利。企业要在目标国家或地区获得保护，通常需要按当地制度另行申请。"),
        ("海外商标有哪几种注册路径？", "常见路径包括单一国家申请、通过马德里体系办理国际注册，以及在部分区域办理地区性注册。选择时要结合目标市场数量与管理成本。"),
        ("应该先在哪些国家注册商标？", "建议按业务实际排序：先覆盖主要销售市场，再看生产、仓储、展会和电商站点所在地，随后考虑供应链与代理商区域，并为未来市场预留空间。"),
        ("只注册英文商标够不够？", "通常不够。当地消费者实际使用的称呼、拼写、音译与意译方式都应纳入规划，避免品牌进入市场后出现无法使用或被他人抢注的情况。"),
        ("莞促知产如何帮助企业做出海商标布局？", "莞促知产扎根东莞松山湖，可协助梳理目标市场优先级、比较注册路径、开展前期查询与材料准备，并做好国内与海外品牌保护的衔接。"),
    ],
    "news/n40.html": [
        ("创始王事件中的判决到底确认了什么？", "据公开信息，贵州省高级人民法院（2022）黔民终564号终审判决确认王立夫（字泽履）是荣和烧房创立人、茅台酒创始人之一，并认为有史料支撑的历史陈述不构成虚假宣传或不正当竞争。该判决并未改变相关注册商标的权属。"),
        ("讲家族历史会不会构成商标侵权？", "单纯基于史料的客观叙述与把历史称谓作为商标使用是两回事。是否构成侵权，要结合标识使用方式、商品类别、是否突出使用、是否容易导致混淆等因素，由主管部门或司法机关依法认定。"),
        ("历史称谓可以直接注册成商标吗？", "需要先做近似查询，判断是否与在先注册商标或在先权利冲突。历史上有据可查并不自动等于可以注册或使用，能否获准注册以商标主管部门审查结果为准。"),
        ("品牌宣传中的历史表述怎么把握？", "做到有出处、有分寸、不攀附：表述以公开史料为依据，避免绝对化和夸大，不借历史暗示与他人品牌存在授权或关联，并留存史料来源与发布记录。"),
        ("莞促知产能提供哪些商标方面的帮助？", "莞促知产扎根东莞松山湖，提供商标近似检索、注册申报、异议与无效宣告应对、品牌类别布局与侵权维权等服务，帮助企业把品牌确权与宣传表达纳入同一套规则。"),
    ],
    "news/n37.html": [
        ("东莞专利申请需要准备哪些材料？", "主要包括申请人身份信息、发明人信息、技术交底书、按专利类型准备的附图或图片；委托代理的还需签署代理委托书。具体以国知局现行要求为准。"),
        ("技术交底书要写到什么程度？", "应写清要解决的技术问题、采用的技术方案与有益效果，并配合附图或实验数据。交底越具体，代理人越能准确把握发明点，写出有保护力的申请文件。"),
        ("发明、实用新型和外观的材料一样吗？", "不一样。发明侧重技术方案与创造性说明，实用新型需体现结构特征的附图，外观设计需提交清晰的外观图片或照片并说明设计要点。"),
        ("申请人和发明人必须是同一个人吗？", "不必。申请人是专利权利人，发明人是对技术方案作出创造性贡献的实际人员，两者可以不同，申请时应分别如实列明。"),
        ("莞促知产在专利申请材料方面能提供什么帮助？", "莞促知产扎根东莞松山湖，提供专利检索、技术交底指导、申请文件撰写与审查意见答复等服务，帮助企业规范准备材料、提高申请质量。"),
    ],
    "news/n38.html": [
        ("东莞专利申请的预审有什么用？", "专利预审是知识产权保护中心为备案主体提供的前置审查服务，符合要求的东莞专利申请经预审后可缩短后续审查周期。预审服务通常不收费，最终授权仍由国家知识产权局依法审查决定。"),
        ("东莞企业怎么才能用上专利预审？", "东莞专利申请一般需要先在东莞知识产权保护中心完成备案，成为备案主体后，再通过预审系统提交申请。备案条件与服务领域以保护中心当期公布的规定为准。"),
        ("备案需要准备哪些材料？", "通常包括备案申请表、营业执照等材料，并在指定平台注册用户提交。填报的产业领域、主营业务等信息要真实完整，审核通过后还需按要求保持备案资格有效。"),
        ("不符合备案条件怎么办？", "如果企业不属于服务领域或技术方案与领域关联度低，可以走普通申请途径，先把技术交底和申请文件质量做扎实，不必勉强追求预审。"),
        ("莞促知产能为预审提供哪些帮助？", "莞促知产扎根东莞松山湖，可协助企业判断是否适合备案、准备备案材料，并在专利检索、技术交底撰写和预审文件准备等环节提供专业支持。"),
    ],
    "news/n39.html": [
        ("怎么判断一家知识产权代理机构是否正规？", "先核验资质：专利代理机构应有依法取得的执业许可，商标代理机构应符合备案要求。可通过国家主管部门公开渠道查询，避免遇到无资质的中介。"),
        ("选择代理机构要看哪些能力？", "重点看是否懂你的行业与技术、流程是否透明、服务是否覆盖确权之后的运用与维权、保密与诚信是否落实，以及是否具备本地化服务和长期陪伴能力。"),
        ("代理机构承诺“保证授权”可信吗？", "应谨慎对待。审查结果由主管部门依法决定，任何机构都不能保证授权。靠谱的机构会如实说明风险与成功率，而不是夸大承诺。"),
        ("为什么建议选熟悉本地的机构？", "熟悉本地产业和政策的机构，沟通成本更低、响应更快，也更了解东莞企业的业务场景与扶持政策，便于提供贴合实际的建议。"),
        ("莞促知产有哪些优势？", "莞促知产扎根东莞松山湖，是莞促集团旗下专注知识产权与科技申报的机构，七大业务板块覆盖确权、运用、保护、管理全链条，一对一顾问全程服务。"),
    ],
    "news/n34.html": [
        ("东莞商标注册需要哪些基本材料？", "主要包括申请人身份材料（公司营业执照、个体工商户执照或个人身份证等）、商标图样、确定的商品或服务类别与项目；委托代理办理的还需签署代理委托书。具体以商标局现行要求为准。"),
        ("以公司名义申请商标注册要准备什么？", "需提供营业执照复印件并加盖公章，同时准备商标图样、类别与项目清单、代理委托书（如委托办理）。公司名称、地址须与营业执照完全一致。"),
        ("商标图样有什么要求？", "图样应清晰、规范、边界完整。文字商标按标准字体提交，图形或图文组合商标要保证清晰度；指定颜色的提交彩色图样，不指定颜色的提交黑白图样。"),
        ("提交材料后被要求补正怎么办？", "应在规定期限内按补正通知要求补齐或修改材料。为避免补件返工，建议提交前逐项核对主体信息、图样、类别项目和联系方式。"),
        ("莞促知产在商标注册材料方面能提供哪些帮助？", "莞促知产扎根东莞，提供商标近似查询、材料核对、类别规划与注册申报等服务，帮助企业规范准备材料、减少补正返工。"),
    ],
    "news/n35.html": [
        ("东莞商标注册为什么要选类别？", "商标按商品和服务类别划分保护范围，注册只在核定使用的类别和项目上受保护。选对类别，商标保护才能覆盖企业实际经营的业务。"),
        ("类别应该选几个才合适？", "没有固定数量，应以当前主营业务为核心，沿业务链条补充关联类别，并为未来业务预留空间。既不能只选一个导致保护不足，也不宜盲目多注造成浪费。"),
        ("做电商需要关注哪些类别？", "除产品本身类别外，还应关注与线上销售、广告宣传、品牌管理相关的服务类别。具体建议结合经营范围，在专业检索基础上逐一排查。"),
        ("类别选定后还要做什么？", "类别确定后，应在目标类别中做近似查询，判断拟注册标志是否与他人已注册或在先申请的商标冲突。类别选择与近似查询应前后衔接。"),
        ("莞促知产如何帮助企业选类别？", "莞促知产扎根东莞，结合企业主营业务、业务链条和发展规划提供类别规划、近似查询与注册申报服务，帮助企业形成与业务匹配的商标保护。"),
    ],
    "news/n36.html": [
        ("个人和公司都可以申请商标注册吗？", "可以。按商标法规定，自然人、法人或者其他组织均可申请注册商标。选择个人还是公司名义，应结合经营主体、权属安排和长期规划决定。"),
        ("公司名义申请商标有什么好处？", "商标权归公司所有，与企业经营和品牌使用主体一致，权属清晰，便于品牌运营、授权、质押融资和尽职调查，适合有规范经营和长期规划的企业。"),
        ("商标在个人名下、公司在用会有风险吗？", "会有。商标权归个人而由公司实际使用的，应通过许可或转让把使用关系约定清楚，否则在企业股权变动、合作或融资时容易产生权属争议。"),
        ("个人名义注册的商标能转到公司吗？", "可以。可以通过转让或许可的方式处理，需签订书面协议、明确范围与期限，并按规定办理备案或变更登记手续。"),
        ("莞促知产能提供哪些商标权属方面的服务？", "莞促知产扎根东莞，提供商标申请、权属规划、转让与许可手续办理等服务，帮助企业让权利主体与实际使用主体保持一致。"),
    ],
    "news/n31.html": [
        ("《专利和商标审查“十五五”规划》对企业申请有什么直接影响？", "规划强调质量第一、提升审查质量，意味着申请会更看重技术交底是否充分、权利要求是否合理、商标标志是否具备显著性。企业应把申请做扎实，而非单纯追求数量。"),
        ("人工智能相关发明可以申请专利吗？", "规划提出研究人工智能辅助发明、人工智能生成发明及使用声明制度，相关规则仍在完善。企业有此类技术成果的，建议结合具体方案咨询专业机构，明确当前的申请路径与撰写要点。"),
        ("审查越来越智能，企业提交材料要注意什么？", "智能工具会提升检索与比对效率，企业应确保申请材料表述准确、逻辑清晰、前后一致，技术交底尽量完整，减少因形式或表述问题被要求补正。"),
        ("有出海计划的企业应关注规划中的哪些内容？", "规划提出支持创新主体、经营主体提升海外专利和商标布局水平。出海企业宜在产品进入目标市场前，通过相应国际途径完成商标与专利的先行布局。"),
        ("莞促知产如何帮助企业应对这些变化？", "莞促知产扎根东莞松山湖，持续跟踪审查政策变化，提供高质量申请撰写、新兴领域布局、海外知识产权规划与现有权利盘点等服务。"),
    ],
    "news/n32.html": [
        ("什么是知识产权海关备案，为什么要办？", "海关备案是权利人将商标、专利等权利向海关登记的保护措施。备案后，海关在口岸发现疑似侵权货物时，可更及时地采取扣留、调查等措施，是进出口环节的一道主动防线。"),
        ("哪些企业更适合优先办理海关备案？", "有驰名商标确认记录、地理标志集体商标或证明商标、光伏等重点产业的企业被政策鼓励积极备案。有进出口业务、品牌仿冒风险较高的外向型企业，也建议优先考虑。"),
        ("海关备案需要准备哪些材料？", "一般需要权利证明文件、权利人身份与联系方式、货物及包装图样、合法进出口企业情况等材料。具体清单以海关规定为准，委托专业机构可协助核对、规范填报。"),
        ("进出口环节发现侵权货物怎么办？", "可固定侵权线索并向海关反映，请求调查协助。意见明确了知识产权管理部门与海关之间的调查协助和业务支撑机制，涉及专利等专业性问题的，还可由专家提供意见。"),
        ("备案之后还需要维护吗？", "需要。权利发生变更、续展或失效时，应及时办理备案变更或注销，保持备案信息与权利状态一致，避免影响海关保护措施的适用。"),
    ],
    "news/n33.html": [
        ("什么是数据知识产权登记？", "数据知识产权登记是对依法依规获取、经过一定规则处理、具有实用价值的数据集合进行登记，确认数据处理者相应权益。登记证书可作为持有数据的初步证明，用于交易、融资和权益保护。"),
        ("数据知识产权登记的办理环节有哪些？", "一般包括登记申请、登记审查、登记公示、登记公告等环节。申请人需提交申请人情况、数据来源、处理规则等材料，上传样例数据并签署声明承诺书。具体以所在地区登记机构规定为准。"),
        ("登记证书有哪些实际用途？", "可用于数据流通交易中的权属证明、数据资产入表、质押融资，以及在权益争议中作为举证材料，帮助企业把数据资源转化为可计量、可运用的资产。"),
        ("所有数据都适合做数据知识产权登记吗？", "不一定。数据知识产权、专利、版权、商业秘密是不同制度。技术性创新方案可能更适合专利，独创性表达可考虑版权，不宜公开的核心数据和经营信息则适合商业秘密保护。应根据数据性质选择组合。"),
        ("企业办理登记前要准备什么？", "先梳理自有数据的类型与价值，确认来源合法、处理过程可追溯，并留存采集授权、清洗规则、加工记录等证据。涉及数据跨境的，还要同步关注合规要求。"),
    ],
    "news/n28.html": [
        ("商标被驳回后还有机会注册吗？", "有机会。商标驳回并不等于申请终结，申请人可在法定期限内提出驳回复审，围绕驳回理由陈述意见、补充证据；复审未获支持的，也可视情况调整标志重新申请或通过其他途径排除在先权利障碍。"),
        ("驳回复审和重新申请该怎么选？", "若驳回是因在先近似且自身标志有争取空间，复审更值得考虑；若属于绝对障碍、避让空间小，换名重新申请往往更高效。可结合品牌依赖度与成本综合判断。"),
        ("驳回复审需要准备哪些材料？", "主要围绕驳回理由准备：主张不近似的，从读音、字形、含义、整体印象说明差异；主张在先使用的，提供使用时间、范围和知名度证据；涉及在先权利的，可提交协商结果。"),
        ("驳回复审要在多长时间内提出？", "应在收到驳回通知之日起的法定期限内提出，具体期限以驳回通知书载明为准。建议收到通知后尽快着手，避免错过期限导致申请失效。"),
        ("莞促知产可以提供哪些商标救济服务？", "莞促知产扎根东莞松山湖，提供商标近似查询、驳回复审、异议答辩、无效宣告与侵权维权等服务，由专业顾问结合案件情况制定应对方案。"),
    ],
    "news/n29.html": [
        ("专利申请被驳回是不是就没救了？", "不是。驳回后通常还有救济途径：审查阶段可通过答复审查意见陈述观点、修改权利要求；收到驳回决定后可在法定期限内提出复审请求；复审不成的，还可依法寻求进一步救济。"),
        ("审查意见答复要注意什么？", "要针对每一条审查意见逐条回应，说清技术方案的区别与有益效果；确需修改的，修改不得超出原始申请文件公开的范围，避免引入新的技术内容。"),
        ("复审请求主要写什么？", "重点写明不服驳回的理由，围绕技术方案是否具备新颖性、创造性，以及审查程序是否存在问题展开，必要时配合修改权利要求和补充证据。"),
        ("驳回后一定要做复审吗？", "不一定。是否复审要结合专利对企业的重要程度、驳回理由和成本权衡。驳回往往也能暴露申请文件的问题，可借此调整技术方案，选择实用新型、拆分申请等更合适的路径。"),
        ("莞促知产在专利驳回方面能提供什么帮助？", "莞促知产扎根东莞松山湖，提供专利检索、申请文件撰写、审查意见答复、驳回复审与策略调整等专业服务，帮助企业在各阶段维护申请权益。"),
    ],
    "news/n30.html": [
        ("高企认定为什么要看知识产权？", "因为知识产权是企业自主创新能力的直接证据，能反映研发活动、成果形成与产品转化情况。认定审查更看重权利与研发活动、主营产品的对应关系，而不只是证书数量。"),
        ("用于高企认定的知识产权要满足什么条件？", "主要有三点：与主营产品或服务高度关联、权属清晰且与被认定主体一致、权利处于有效状态并按规定缴纳费用。权属不清或已失效的权利难以作为有效支撑。"),
        ("知识产权与主营产品不相关会有影响吗？", "会有影响。与主营产品无关的权利，即便真实有效，也难以说明企业的创新能力。建议围绕核心产品和技术，梳理从研发到专利再到产品的对应关系。"),
        ("临时突击申请知识产权来得及吗？", "通常难以体现持续性。高企认定看重长期创新积累，建议把知识产权规划嵌入日常研发，立项时同步考虑专利挖掘、成果形成后及时申请，申报时材料才齐备可信。"),
        ("莞促知产能为高企认定提供哪些服务？", "莞促知产扎根东莞松山湖，提供专利挖掘、申请布局、软件著作权登记、知识产权盘点与高企认定申报的一站式服务，帮助企业提前规划、规范准备材料。"),
    ],
    "news/n19.html": [
        ("东莞注册商标必须找代理机构吗？", "申请人可自行办理，也可委托依法设立的商标代理机构办理。对流程不熟悉的，委托专业机构可减少材料与程序上的疏漏。"),
        ("商标注册前为什么建议先做查询？", "查询可帮助判断拟注册标志是否存在在先相同或近似权利，降低因冲突被驳回的风险，是企业安排品牌布局的重要前置步骤。"),
        ("收到补正通知或审查意见怎么办？", "应在规定期限内按要求补正材料或作出答复。逾期未处理可能影响申请进程，建议及时与代理机构或商标局沟通。"),
        ("商标公告期被提出异议怎么办？", "被异议人可在规定期限内提交答辩材料，围绕在先权利、标志显著性与使用事实等要点回应，由专业代理人协助准备更稳妥。"),
        ("拿到商标注册证后还需要做什么？", "应规范使用并留存使用证据，名称地址变更、转让或许可需及时办理手续，同时关注续展期限，避免权利失效。"),
    ],
    "news/n20.html": [
        ("三种专利中哪种一定要经过实质审查？", "发明专利申请在初步审查合格后需由申请人提出实质审查请求，经过新颖性、创造性与实用性审查后才可能授权；实用新型与外观设计以初步审查为主。"),
        ("实用新型和外观专利授权后权利就一定稳定吗？", "两类专利授权时不进行全面实质审查，后续维权或发生争议时，通常需要提供专利权评价报告等材料佐证权利稳定性。"),
        ("三种专利可以同时申请吗？", "同一申请人同日就同样的发明创造既申请实用新型又申请发明专利，并作出声明的，可以按相关规定衔接办理，具体条件以现行专利法及其实施细则为准。"),
        ("专利申请的审查进度可以查询吗？", "可以。申请人可通过国家知识产权局提供的查询渠道了解申请状态；委托代理机构的，也可由顾问同步关键节点信息。"),
        ("技术交底材料要准备到什么程度？", "应尽量写清技术问题、技术方案与有益效果，并配合附图或实验数据，帮助代理人准确理解技术方案并撰写申请文件。"),
    ],
}

def build_articles():
    generic = [
        "知识产权是企业的核心无形资产。随着创新活动日益活跃，专利、商标、版权等权利的取得、维护与运用，越来越需要专业机构的支撑。",
        "一、准确把握制度要点",
        "无论是专利申请、商标注册，还是科技项目申报，都建立在明确的制度规则之上。企业应先理解规则本身，再结合自身技术背景、业务类型与发展目标作出选择。",
        "二、结合企业实际做好规划",
        "不同企业的技术方向、市场布局与保护重点各不相同。建议从长期经营的角度出发，对知识产权进行系统性规划，形成与业务匹配的布局。",
        "三、规范流程与材料准备",
        "规范的材料与流程是权利稳定的基础。企业应注意关键时间节点，按要求完整准备材料，并对商业秘密与核心技术信息做好保密管理。",
    ]
    def is_heading(seg):
        nums = ("一","二","三","四","五","六","七","八","九","十")
        return any(seg.startswith(x + "、") for x in nums) or seg in ("写在最后", "结语", "结语与展望")
    for n in NEWS:
        content = ARTICLE_BODIES.get(n["file"])
        if content:
            paras = ["<p>%s</p>" % n["desc"]]
            for seg in content:
                if is_heading(seg):
                    paras.append("<h3>%s</h3>" % seg)
                else:
                    paras.append("<p>%s</p>" % seg)
        else:
            paras = ["<p>%s</p>" % n["desc"]]
            for seg in generic:
                if is_heading(seg):
                    paras.append("<h3>%s</h3>" % seg)
                else:
                    paras.append("<p>%s</p>" % seg)
        # 正文配图：在引言段（第 2 段）后插入流程图，完整显示不裁切
        art_img = ARTICLE_IMAGES.get(n["file"])
        if art_img and len(paras) >= 2:
            img_src, img_cap = art_img
            paras.insert(2, '<figure class="article-figure"><img src="/%s" alt="%s"><figcaption>%s</figcaption></figure>' % (img_src, img_cap, img_cap))
        # 活动图集：正文中按序完整展示实拍照片
        gallery = ARTICLE_GALLERY.get(n["file"])
        if gallery:
            for gi, (g_src, g_cap) in enumerate(gallery):
                paras.insert(len(paras), '<figure class="article-figure"><img src="/%s" alt="%s"><figcaption>%s</figcaption></figure>' % (g_src, g_cap, g_cap))
        # 新闻纪实类不放业务引导语与知识说明
        is_news = n["file"] in ARTICLE_GALLERY
        if not is_news:
            # 内链到东莞地域落地页：把主关键词信号集中到转化页
            city_link = CITY_LINK_BY_ARTICLE.get(n["file"])
            if city_link:
                url, kw = city_link
                paras.append('<p>想进一步了解 <a href="/%s">%s</a> 的办理流程与本地服务，可查看本站对应服务页，或通过“联系我们”栏目由专业顾问结合您的情况提供说明。</p>' % (url, kw))
            else:
                paras.append("<p>如需了解本文涉及业务的具体办理方式，欢迎通过官网“联系我们”栏目与我们沟通，由专业顾问结合您的实际情况提供说明。</p>")
        # FAQ 区块：渲染问答，并配套 FAQPage 结构化数据
        faq = ARTICLE_FAQS.get(n["file"])
        if faq:
            paras.append("<h3>常见问题</h3>")
            for q, a in faq:
                paras.append('<div class="faq-item"><div class="faq-q"><span class="qmark">问</span><span>%s</span></div><div class="faq-a"><strong>答：</strong>%s</div></div>' % (q, a))
        if not is_news:
            paras.append("<p style=\"color:#5A6B85;font-size:13px\">说明：本文内容以国家主管部门最新规定与官方文件为准，仅供知识分享参考。</p>")
        bodycls = "article-body notice-body" if n["cat"]=="通知公告" else "article-body"
        body = '''<div class="container" style="padding:36px 0 80px">
  <article class="article-wrap">
    <h1 class="article-title">%s</h1>
    <div class="article-meta">%s ｜ %s ｜ 广东莞促知识产权代理事务所</div>
    <img class="article-cover" src="/%s" alt="%s">
    <div class="%s">%s</div>
    <div style="text-align:center;margin-top:30px"><a class="btn btn--outline" href="/news.html">返回资讯列表 →</a></div>
  </article>
</div>''' % (n["title"], n["cat"], n["date"], n["cover"], n["title"], bodycls, "".join(paras))
        ld = web_page_jsonld(n["title"], n["desc"], n["file"], "Article")
        if faq:
            ld = {
                "@context": "https://schema.org",
                "@graph": [
                    ld,
                    {"@type": "FAQPage", "mainEntity": [
                        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                        for q, a in faq
                    ]},
                ],
            }
        # 标题已含品牌词的文章不重复追加后缀，避免“莞促知产…｜莞促知产”
        seo_title = n["title"] if "莞促知产" in n["title"] else n["title"]+"｜莞促知产"
        write(n["file"], page(seo_title, n["desc"], n["cat"]+",知识产权,专利商标知识,莞促知产", n["file"], body, active="news", og_type="article", og_image=BASE+"/"+n["cover"], jsonld=ld))

# ============ 成功案例 ============
def build_cases():
    cases = [
        ("制造业企业发明专利布局", "为制造企业提供专利挖掘与布局服务，围绕核心技术形成专利组合，提升创新成果的保护强度。"),
        ("科技型企业高新技术企业认定", "辅导科技型企业完成高企认定申报，梳理自主知识产权与研发材料，规范申报流程。"),
        ("品牌商标异议与复审", "代理商标异议答辩与驳回复审，组织证据材料，维护客户品牌的注册权益。"),
        ("软件著作权批量登记", "为软件企业办理软件著作权批量登记，建立作品台账，便于后续管理与维权。"),
        ("跨境电商海外商标布局", "协助跨境电商企业通过马德里体系与单一国家途径完成海外商标注册。"),
        ("企业知识产权贯标辅导", "辅导企业建立知识产权管理体系，推进 GB/T 29490 贯标认证。"),
    ]
    cards = "".join('''<div class="item-card"><h4>%s</h4><p>%s</p></div>''' % p for p in cases)
    body = ph("成功案例", "以专业服务助力企业创新发展", "SUCCESS CASES") + '''
<div class="container" style="padding-top:36px;padding-bottom:80px">
  <div class="lead-box">以下案例为服务类型说明，均作匿名化处理，不涉及客户具体名称与敏感信息。实际服务内容以双方委托约定为准。</div>
  <div class="content-block"><h2>服务案例类型</h2><div class="item-list">%s</div></div>
</div>''' % cards
    write("cases.html", page(*seo("cases"), "cases.html", body, active="cases", jsonld=web_page_jsonld("成功案例", "服务案例类型说明", "cases.html", "CollectionPage")))

# ============ FAQ ============
def build_faq():
    items = "".join('''<div class="faq-item"><div class="faq-q"><span class="qmark">问</span><span>%s</span></div><div class="faq-a"><strong>答：</strong>%s</div></div>''' % p for p in FAQ)
    body = ph("常见问题", "关于知识产权服务的常见疑问", "FAQ") + '''
<div class="container" style="padding-top:36px;padding-bottom:80px">
  <div class="faq-list">%s</div>
  <div class="content-block" style="margin-top:28px;text-align:center">
    <p>还有其他问题？欢迎联系我们，由专业顾问为您解答。</p>
    <a class="btn btn--gold" href="/contact.html" style="margin-top:10px">联系我们 →</a>
  </div>
</div>''' % items
    write("faq.html", page(*seo("faq"), "faq.html", body, active="faq", jsonld=web_page_jsonld("常见问题", "知识产权服务常见问答", "faq.html", "FAQPage")))

# ============ 联系我们 ============
def build_contact():
    body = ph("联系我们", "期待与您建立联系", "CONTACT US") + '''
<div class="container" style="padding-top:36px;padding-bottom:80px">
  <div class="contact-grid">
    <div class="contact-info">
      <h3>联系方式</h3>
      <div class="info-grid">
        <div class="info-row"><div class="info-ico info-ico--2">联系</div><div><div class="info-label">联系人</div><div class="info-val">%s</div></div></div>
        <div class="info-row"><div class="info-ico info-ico--2">手机</div><div><div class="info-label">手机 / 微信</div><div class="info-val">%s</div></div></div>
        <div class="info-row"><div class="info-ico info-ico--2">热线</div><div><div class="info-label">服务热线 / 固话</div><div class="info-val">%s</div></div></div>
        <div class="info-row"><div class="info-ico info-ico--2">邮箱</div><div><div class="info-label">邮箱</div><div class="info-val">%s</div></div></div>
        <div class="info-row"><div class="info-ico info-ico--2">Q Q</div><div><div class="info-label">QQ</div><div class="info-val">%s</div></div></div>
        <div class="info-row"><div class="info-ico info-ico--2">时间</div><div><div class="info-label">工作时间</div><div class="info-val info-val--time">%s</div></div></div>
      </div>
      <div class="info-row info-row--full"><div class="info-ico info-ico--2">地址</div><div><div class="info-label">办公地址</div><div class="info-val">%s<span class="info-val--nowrap">（邮编 %s）</span></div></div></div>
    </div>
    <div>
      <div class="contact-qr" style="background:#fff;border:1px solid var(--line);border-radius:16px;padding:24px">
        <img src="/assets/img/qr-contact.png" alt="扫码咨询">
        <p>扫码添加微信咨询（微信号：%s）</p>
      </div>
      <div class="form-note" style="margin-top:20px">
        <h3>免费检索与初步评估</h3>
        <p>如需商标/专利检索或初步评估，请通过电话、微信或邮箱说明业务类型、企业情况与期望时间，我们将安排专业顾问与您对接。</p>
        <a class="btn btn--primary" href="tel:%s">立即致电 %s</a>
      </div>
    </div>
  </div>
</div>''' % (CONTACT["person"], CONTACT["mobile"], CONTACT["tel"], CONTACT["email"], CONTACT["qq"], CONTACT["worktime"], CONTACT["address_full"], CONTACT["postcode"], CONTACT["wechat"], CONTACT["mobile"], CONTACT["mobile"])
    write("contact.html", page(*seo("contact"), "contact.html", body, active="contact", jsonld=web_page_jsonld("联系我们", "联系方式与咨询方式", "contact.html", "ContactPage")))

# ============ 网站地图页 ============
def build_sitemap_html():
    groups = [
        ("首页", [("首页", "")]),
        ("关于莞促", [(l,h) for l,h in NAV[1]["children"]]),
        ("专业服务", [("服务总览", "services.html")]+[(l,h) for l,h in NAV[2]["children"]]),
        ("东莞本地服务", [(c["kw"], c["file"]) for c in CITY_PAGES]),
        ("服务与资讯", [("服务流程","process.html"),("新闻资讯","news.html"),("通知公告","notice.html"),("政策速递","policy.html"),("知产课堂","knowledge.html"),("成功案例","cases.html"),("常见问题","faq.html"),("联系我们","contact.html")]),
        ("资讯文章", [(n["title"], n["file"]) for n in NEWS]),
    ]
    cols = "".join('''<div class="sitemap-col"><h4>%s</h4>%s</div>''' % (g, "".join('<a href="/%s">%s</a>' % (h,l) for l,h in items)) for g,items in groups)
    body = ph("网站地图", "快速了解网站全部栏目", "SITEMAP") + '''
<div class="container" style="padding-top:36px;padding-bottom:80px">
  <div class="sitemap-grid">%s</div>
</div>''' % cols
    write("sitemap.html", page(*seo("sitemap"), "sitemap.html", body, active="", jsonld=web_page_jsonld("网站地图", "网站栏目导航", "sitemap.html")))

def main():
    build_index(); build_about(); build_group(); build_culture(); build_team(); build_honors()
    build_services()
    for s in SERVICES: build_service_detail(s)
    build_city_pages()
    build_process(); build_news(); build_articles(); build_cases(); build_faq(); build_contact(); build_sitemap_html()
    print("PAGES BUILT")

if __name__ == "__main__":
    main()
