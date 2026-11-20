# -*- coding: utf-8 -*-
"""用 PIL 绘制两篇 SEO 文章配图（代码生成，无水印）。
seo-trademark-guide.jpg / seo-patent-timeline.jpg
"""
from PIL import Image, ImageDraw, ImageFont

FONT = "C:/Windows/Fonts/msyh.ttc"
FONT_B = "C:/Windows/Fonts/msyhbd.ttc"
OUT = "D:/项目管理文件夹/2026-11-19-15-27-25/site/assets/img/covers/"

def f(size, bold=False):
    return ImageFont.truetype(FONT_B if bold else FONT, size)

def grad(w, h, c1, c2):
    im = Image.new("RGB", (w, h), c1)
    d = ImageDraw.Draw(im)
    for y in range(h):
        t = y / max(h - 1, 1)
        d.line([(0, y), (w, y)], fill=tuple(int(c1[i]*(1-t)+c2[i]*t) for i in range(3)))
    return im, d

def ctext(d, text, cx, y, size, fill, bold=False):
    fo = f(size, bold)
    d.text((cx - d.textlength(text, font=fo)/2, y), text, font=fo, fill=fill)

def wrap(d, text, font, maxw):
    out, cur = [], ""
    for ch in text:
        if d.textlength(cur + ch, font=font) > maxw and cur:
            out.append(cur); cur = ch
        else:
            cur += ch
    if cur: out.append(cur)
    return out

# ===== 图1：商标注册五步流程 =====
def trademark():
    W, H = 1000, 620
    im, d = grad(W, H, (245,250,255), (232,242,255))
    ctext(d, "东莞商标注册完整流程", W/2, 40, 36, (14,42,92), True)
    ctext(d, "从查询准备到核准领证，按步骤推进", W/2, 92, 18, (96,116,148))
    steps = [
        ("01", "注册前查询", "近似排查\n确定类别与项目", (43,108,255)),
        ("02", "准备材料", "主体证明\n商标图样 · 委托书", (90,80,230)),
        ("03", "提交与受理", "形式审查\n补正 · 受理通知", (130,75,225)),
        ("04", "实审与公告", "实质审查\n初步审定公告", (175,80,200)),
        ("05", "核准领证", "商标注册证\n规范使用与续展", (210,90,160)),
    ]
    x0, cw, gap = 55, 168, 22
    for i, (num, name, desc, col) in enumerate(steps):
        x = x0 + i*(cw+gap)
        d.rounded_rectangle((x, 150, x+cw, 430), radius=16, fill=(255,255,255), outline=(212,224,246), width=2)
        d.rounded_rectangle((x+14, 166, x+62, 206), radius=10, fill=col)
        nw = d.textlength(num, font=f(20, True))
        d.text((x+38-nw/2, 173), num, font=f(20, True), fill=(255,255,255))
        d.text((x+16, 224), name, font=f(19, True), fill=(14,42,92))
        d.line((x+16, 258, x+cw-16, 258), fill=(220,230,246), width=2)
        for k, line in enumerate(desc.split("\n")):
            d.text((x+16, 278+k*32), line, font=f(15), fill=(78,98,132))
        if i < 4:
            ax = x+cw+4
            d.line((ax, 290, ax+14, 290), fill=(150,170,205), width=3)
            d.polygon([(ax+14,290),(ax+7,285),(ax+7,295)], fill=(150,170,205))
    d.rounded_rectangle((55, 470, 945, 575), radius=14, fill=(255,255,255), outline=(212,224,246), width=2)
    d.text((78, 488), "提示", font=f(18, True), fill=(43,108,255))
    tips = ["商标图样与主体信息需保持一致，减少补正", "公告期内留意异议动态，及时答辩", "注册后留存使用证据，关注续展时间"]
    for i, t in enumerate(tips):
        x = 80 + i*295
        d.text((x, 524), "·", font=f(15), fill=(43,108,255))
        lines = wrap(d, t, f(14), 280)
        for k, line in enumerate(lines[:2]):
            d.text((x+16, 522+k*22), line, font=f(14), fill=(70,90,125))
    im.save(OUT+"seo-trademark-guide.jpg", quality=92)

# ===== 图2：三种专利流程对比 =====
def patent():
    W, H = 1000, 640
    im, d = grad(W, H, (245,250,255), (235,246,255))
    ctext(d, "三种专利授权流程对比", W/2, 40, 36, (14,42,92), True)
    ctext(d, "发明需实质审查，实用新型与外观设计以初步审查为主", W/2, 92, 18, (96,116,148))
    lanes = [
        ("发明专利", (43,108,255), ["提交申请","初步审查","公布","提出实审请求","实质审查","授权登记"]),
        ("实用新型", (122,75,255), ["提交申请","初步审查","授权登记","—","—","—"]),
        ("外观设计", (200,80,160), ["提交申请","初步审查","授权登记","—","—","—"]),
    ]
    lx, lw = 55, 150
    sx = 230; sw = 108; sg = 10
    for ri, (name, col, stages) in enumerate(lanes):
        y = 150 + ri*145
        d.rounded_rectangle((lx, y, lx+lw, y+108), radius=14, fill=col)
        ctext(d, name, lx+lw/2, y+40, 20, (255,255,255), True)
        for si, st in enumerate(stages):
            x = sx + si*(sw+sg)
            if st == "—":
                d.rounded_rectangle((x, y+20, x+sw, y+88), radius=12, fill=(244,248,255), outline=(226,234,247), width=1)
                ctext(d, "—", x+sw/2, y+48, 20, (180,195,215))
            else:
                is_实 = "实审" in st or "请求" in st
                fill = col if is_实 else (255,255,255)
                tc = (255,255,255) if is_实 else (40,60,95)
                d.rounded_rectangle((x, y+20, x+sw, y+88), radius=12, fill=fill, outline=col, width=2)
                ctext(d, st, x+sw/2, y+44, 15, tc, is_实)
            if si < 5 and stages[si+1] != "—" and st != "—":
                ax = x+sw+1
                d.line((ax, y+54, ax+8, y+54), fill=(160,180,210), width=2)
                d.polygon([(ax+8,y+54),(ax+3,y+50),(ax+3,y+58)], fill=(160,180,210))
    d.rounded_rectangle((55, 590, 945, 622), radius=10, fill=(255,255,255), outline=(212,224,246), width=1)
    ctext(d, "高亮环节为该类型专利特有的关键流程 · 具体以国家知识产权局现行规定为准", W/2, 598, 14, (92,112,145))
    im.save(OUT+"seo-patent-timeline.jpg", quality=92)

trademark(); patent()
print("done")
