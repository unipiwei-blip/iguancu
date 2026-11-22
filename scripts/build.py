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
    <p class="hero-lead">%s 是莞促集团旗下关联机构。我们拥有一批在专利申请、商标注册、高新认定、知识产权维权等方面资深的代理人团队，为企业提供一站式的知识产权与科技创新解决方案。</p>
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
''' % (LOC, BRAND, sector_top, sector_bottom, advs, news)
    write("index.html", page(
        *seo("index"), "", body, active="index", jsonld=org_jsonld()))

# ============ 关于莞促 ============
def build_about():
    body = ph("关于莞促", "了解我们的定位、团队与服务理念", "ABOUT US") + '''
<div class="container" style="padding-top:36px;padding-bottom:80px">
  <div class="content-block">
    <h2>事务所简介</h2>
    <div class="lead-box">广东莞促知识产权代理事务所（普通合伙）是莞促集团旗下关联的公司，在集团管理下实行连锁运营，下设 8 家分公司及 1 家自主产权科技孵化器。</div>
    <p>我们拥有一批在专利申请、商标注册、高新认定、知识产权维权等方面资深的强大专业代理人团队，为客户提供一站式的解决方案。</p>
    <p>所有知识产权案件当天申报，涉及相关问题在第一时间处理，提供一对一顾问服务，并具备完善的售后保障体系。严格遵守执业道德，忠诚执业信仰，公司建立有严格的保密体系，与客户之间所有业务均签订规范的保密协议。</p>
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
</div>'''
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
  <div class="content-block" style="margin-top:28px;text-align:center">
    <h2 style="border:none;padding:0">需要哪方面的帮助？</h2>
    <p>欢迎说明业务类型与企业情况，我们将匹配专业团队与您对接。</p>
    <a class="btn btn--gold" href="/contact.html" style="margin-top:10px">立即咨询 →</a>
  </div>
</div>''' % sectors
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
ARTICLE_BODIES = {
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
        write(n["file"], page(n["title"]+"｜莞促知产", n["desc"], n["cat"]+",知识产权,专利商标知识,莞促知产", n["file"], body, active="news", og_type="article", og_image=BASE+"/"+n["cover"], jsonld=ld))

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
    build_process(); build_news(); build_articles(); build_cases(); build_faq(); build_contact(); build_sitemap_html()
    print("PAGES BUILT")

if __name__ == "__main__":
    main()
