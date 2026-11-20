# -*- coding: utf-8 -*-
"""用 PIL 绘制两篇 SEO 文章配图（代码生成，无水印）。
seo-trademark-guide.jpg / seo-patent-timeline.jpg
设计原则：蓝色专业配色、充足留白、文字与边框保持安全距离、缩小后仍清晰。
"""
from PIL import Image, ImageDraw, ImageFont

FONT = "C:/Windows/Fonts/msyh.ttc"
FONT_B = "C:/Windows/Fonts/msyhbd.ttc"
OUT = "D:/项目管理文件夹/2026-11-19-15-27-25/site/assets/img/covers/"

INK = (16, 42, 92)
SUB = (86, 106, 140)
LINE = (206, 222, 246)
CARD = (255, 255, 255)
BLUE = (43, 108, 255)


def f(size, bold=False):
    return ImageFont.truetype(FONT_B if bold else FONT, size)


def grad(w, h, c1, c2):
    im = Image.new("RGB", (w, h), c1)
    d = ImageDraw.Draw(im)
    for y in range(h):
        t = y / max(h - 1, 1)
        d.line([(0, y), (w, y)], fill=tuple(int(c1[i] * (1 - t) + c2[i] * t) for i in range(3)))
    return im, d


def ctext(d, text, cx, y, size, fill, bold=False):
    fo = f(size, bold)
    d.text((cx - d.textlength(text, font=fo) / 2, y), text, font=fo, fill=fill)


def wrap(d, text, font, maxw):
    out, cur = [], ""
    for ch in text:
        if d.textlength(cur + ch, font=font) > maxw and cur:
            out.append(cur)
            cur = ch
        else:
            cur += ch
    if cur:
        out.append(cur)
    return out


# ===== 图1：商标注册五步流程 =====
def trademark():
    W, H = 1000, 560
    im, d = grad(W, H, (246, 251, 255), (230, 241, 255))

    # 顶部装饰细条
    d.rounded_rectangle((W / 2 - 32, 30, W / 2 + 32, 35), radius=3, fill=BLUE)
    ctext(d, "东莞商标注册完整流程", W / 2, 48, 38, INK, True)
    ctext(d, "从查询准备到核准领证，按步骤推进", W / 2, 104, 19, SUB)

    steps = [
        ("01", "注册前查询", "近似排查\n确定类别与项目", (43, 108, 255)),
        ("02", "准备材料", "主体证明\n商标图样 · 委托书", (88, 88, 232)),
        ("03", "提交与受理", "形式审查\n补正 · 受理通知", (128, 80, 224)),
        ("04", "实审与公告", "实质审查\n初步审定公告", (172, 84, 204)),
        ("05", "核准领证", "商标注册证\n规范使用与续展", (206, 92, 160)),
    ]
    x0, cw, gap = 56, 166, 22
    top, bot = 160, 400
    for i, (num, name, desc, col) in enumerate(steps):
        x = x0 + i * (cw + gap)
        d.rounded_rectangle((x, top, x + cw, bot), radius=16, fill=CARD, outline=LINE, width=2)
        # 序号徽章
        d.rounded_rectangle((x + 18, top + 18, x + 68, top + 60), radius=10, fill=col)
        nw = d.textlength(num, font=f(21, True))
        d.text((x + 43 - nw / 2, top + 24), num, font=f(21, True), fill=(255, 255, 255))
        d.text((x + 18, top + 76), name, font=f(20, True), fill=INK)
        d.line((x + 18, top + 112, x + cw - 18, top + 112), fill=(224, 234, 250), width=2)
        for k, line in enumerate(desc.split("\n")):
            d.text((x + 18, top + 130 + k * 32), line, font=f(16), fill=(74, 96, 132))
        if i < 4:
            ax = x + cw + 3
            d.line((ax, top + 120, ax + 13, top + 120), fill=(150, 172, 208), width=3)
            d.polygon([(ax + 13, top + 120), (ax + 6, top + 115), (ax + 6, top + 125)], fill=(150, 172, 208))

    # 底部提示：文字居中、留足边距
    d.rounded_rectangle((56, 432, 944, 528), radius=14, fill=CARD, outline=LINE, width=2)
    d.text((84, 452), "办理提示", font=f(18, True), fill=BLUE)
    tips = [
        "商标图样与主体信息一致，减少补正",
        "公告期内留意异议动态，及时答辩",
        "注册后留存使用证据，关注续展时间",
    ]
    for i, t in enumerate(tips):
        x = 84 + i * 288
        d.text((x, 488), "·", font=f(16, True), fill=BLUE)
        lines = wrap(d, t, f(15), 268)
        for k, line in enumerate(lines[:2]):
            d.text((x + 18, 486 + k * 22), line, font=f(15), fill=(70, 92, 128))
    im.save(OUT + "seo-trademark-guide.jpg", quality=94)


# ===== 图2：三种专利流程对比 =====
def patent():
    W, H = 1000, 620
    im, d = grad(W, H, (246, 251, 255), (232, 244, 255))

    d.rounded_rectangle((W / 2 - 32, 28, W / 2 + 32, 33), radius=3, fill=BLUE)
    ctext(d, "三种专利授权流程对比", W / 2, 46, 38, INK, True)
    ctext(d, "发明需实质审查，实用新型与外观设计以初步审查为主", W / 2, 100, 19, SUB)

    lanes = [
        ("发明专利", (43, 108, 255), ["提交申请", "初步审查", "公布", "提出实审请求", "实质审查", "授权登记"]),
        ("实用新型", (122, 80, 240), ["提交申请", "初步审查", "授权登记", "", "", ""]),
        ("外观设计", (200, 84, 158), ["提交申请", "初步审查", "授权登记", "", "", ""]),
    ]
    lx, lw = 56, 148
    sx, sw, sg = 232, 106, 12
    top = 158
    rh = 108
    gap = 20
    for ri, (name, col, stages) in enumerate(lanes):
        y = top + ri * (rh + gap)
        d.rounded_rectangle((lx, y, lx + lw, y + rh), radius=14, fill=col)
        ctext(d, name, lx + lw / 2, y + rh / 2 - 14, 21, (255, 255, 255), True)
        for si, st in enumerate(stages):
            x = sx + si * (sw + sg)
            if not st:
                d.rounded_rectangle((x, y + 16, x + sw, y + rh - 16), radius=11,
                                    fill=(244, 249, 255), outline=(228, 236, 248), width=1)
                ctext(d, "—", x + sw / 2, y + rh / 2 - 14, 20, (176, 192, 214))
            else:
                key = "实审" in st or "请求" in st
                fill = col if key else CARD
                tc = (255, 255, 255) if key else (36, 58, 96)
                d.rounded_rectangle((x, y + 16, x + sw, y + rh - 16), radius=11,
                                    fill=fill, outline=col, width=2)
                ctext(d, st, x + sw / 2, y + rh / 2 - 11, 15 if key else 16, tc, key)
            if si < 5 and stages[si + 1] and st:
                ax = x + sw + 1
                d.line((ax, y + rh / 2, ax + 8, y + rh / 2), fill=(158, 180, 212), width=2)
                d.polygon([(ax + 8, y + rh / 2), (ax + 3, y + rh / 2 - 4), (ax + 3, y + rh / 2 + 4)],
                          fill=(158, 180, 212))

    # 底部说明：居中、留足边距
    d.rounded_rectangle((56, 552, 944, 600), radius=11, fill=CARD, outline=LINE, width=1)
    ctext(d, "高亮环节为该类型专利特有的关键流程，具体以国家知识产权局现行规定为准",
          W / 2, 566, 16, (84, 104, 138))
    im.save(OUT + "seo-patent-timeline.jpg", quality=94)


trademark()
patent()
print("done")
