"""Hero illustration for the home solar page: a contemporary house at dusk with an all black solar array,
battery storage, a heat pump and an EV charger, linked by animated energy lines. Drawn from scratch as SVG."""
import random

W, H = 1600, 1000
VIEW = (140, 150, 1460, 800)   # the framed crop used on the page
GROUND = 752

# Roof plane facing the viewer: eave (bottom) and ridge (top) corners
B0, B1 = (355, 470), (895, 470)
T0, T1 = (410, 325), (840, 325)


def roof_pt(u, v):
    bx, by = B0[0] + (B1[0] - B0[0]) * u, B0[1]
    tx, ty = T0[0] + (T1[0] - T0[0]) * u, T0[1]
    return bx + (tx - bx) * v, by + (ty - by) * v


def poly(points):
    return ' '.join('%.1f,%.1f' % p for p in points)


def panels():
    cols, rows = 9, 3
    ua, ub, va, vb, gu, gv = 0.06, 0.94, 0.09, 0.93, 0.0065, 0.035
    pw = (ub - ua - (cols - 1) * gu) / cols
    ph = (vb - va - (rows - 1) * gv) / rows
    out = []
    for j in range(rows):
        for i in range(cols):
            u0 = ua + i * (pw + gu)
            v0 = va + j * (ph + gv)
            u1, v1 = u0 + pw, v0 + ph
            out.append('<polygon class="pv" points="%s"/>' % poly([roof_pt(u0, v0), roof_pt(u1, v0), roof_pt(u1, v1), roof_pt(u0, v1)]))
            lines = []
            for k in range(1, 6):
                uu = u0 + pw * k / 6
                a, b = roof_pt(uu, v0), roof_pt(uu, v1)
                lines.append('M%.1f %.1fL%.1f %.1f' % (a + b))
            for k in (1, 2):
                vv = v0 + ph * k / 3
                a, b = roof_pt(u0, vv), roof_pt(u1, vv)
                lines.append('M%.1f %.1fL%.1f %.1f' % (a + b))
            out.append('<path class="cell" d="%s"/>' % ''.join(lines))
    area = [roof_pt(ua, va), roof_pt(ub, va), roof_pt(ub, vb), roof_pt(ua, vb)]
    return ''.join(out), poly(area)


def stars(seed=7, n=40):
    rnd = random.Random(seed)
    s = []
    for _ in range(n):
        x, y = rnd.uniform(150, W - 20), rnd.uniform(150, 430)
        r = rnd.choice([0.8, 1.0, 1.2, 1.5])
        o = rnd.uniform(0.2, 0.75)
        s.append('<circle cx="%.0f" cy="%.0f" r="%s" opacity="%.2f"/>' % (x, y, r, o))
    return ''.join(s)


def cladding(x0, x1, y0, y1, step=9):
    return ''.join('<line x1="%d" y1="%d" x2="%d" y2="%d"/>' % (x, y0, x, y1) for x in range(x0 + step, x1, step))


def lawn_stripes():
    out = []
    for i in range(-6, 16):
        x = 120 + i * 120
        out.append('<path d="M%d %d L%d %d L%d 1000 L%d 1000Z"/>' % (x, GROUND, x + 60, GROUND, x + 60 - 260, x - 260) if i % 2 == 0 else '')
    return ''.join(out)


def flow(d):
    return '<path class="flow-glow" d="%s"/><path class="flow-base" d="%s"/><path class="flow" d="%s"/>' % (d, d, d)


def home_energy_svg(labels=True, pid='he', cls='home-art', crop=True):
    p = pid
    pv, area = panels()
    vb = '%d %d %d %d' % VIEW if crop else '0 0 %d %d' % (W, H)
    lab = ''
    if labels:
        def label(x, y, text, lx, ly):
            w = len(text) * 13 + 50
            bx = x - w / 2
            return ('<g class="hl"><path class="lead" d="M%.0f %.0fL%.0f %.0f"/><circle class="ldot" cx="%.0f" cy="%.0f" r="4.5"/>'
                    '<rect class="lpill" x="%.0f" y="%.0f" width="%.0f" height="40" rx="20"/>'
                    '<circle class="lmark" cx="%.0f" cy="%.0f" r="5"/>'
                    '<text class="ltext" x="%.0f" y="%.0f">%s</text></g>') % (
                x, y + 20, lx, ly, lx, ly, bx, y, w, bx + 22, y + 20, bx + 36, y + 26.5, text)
        lab = (label(625, 232, 'ALL BLACK SOLAR ARRAY', 625, 340)
               + label(300, 534, 'BATTERY STORAGE', 317, 662)
               + label(244, 600, 'HEAT PUMP', 228, 696)
               + label(1300, 508, 'SMART EV CHARGING', 1269, 662))
    reflections = ('<g filter="url(#%s-soft)" opacity="0.75">' % p + ''.join(
        '<rect x="%d" y="800" width="%d" height="42" fill="url(#%s-refl)"/>' % (x0 + 6, x1 - x0 - 12, p)
        for x0, x1 in [(880, 959), (968, 1045), (1054, 1131), (1140, 1220)]) + '</g>'
        '<g stroke="#0a1c20" stroke-width="2" opacity="0.7"><line x1="856" y1="811" x2="1268" y2="811"/>'
        '<line x1="856" y1="823" x2="1268" y2="823"/><line x1="856" y1="835" x2="1268" y2="835"/></g>')
    return f'''<svg class="{cls}" viewBox="{vb}" role="img" aria-label="Illustration of a contemporary home at dusk with an all black solar array, battery storage, a heat pump and an electric car charging, all linked as one energy system" xmlns="http://www.w3.org/2000/svg">
<defs>
  <linearGradient id="{p}-sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#040605"/><stop offset="0.42" stop-color="#0a110d"/><stop offset="0.66" stop-color="#17221a"/><stop offset="0.76" stop-color="#2d3526"/><stop offset="1" stop-color="#1a2219"/>
  </linearGradient>
  <radialGradient id="{p}-dusk" cx="0.7" cy="0.7" r="0.55"><stop offset="0" stop-color="#e3a75a" stop-opacity="0.45"/><stop offset="0.45" stop-color="#b8834a" stop-opacity="0.15"/><stop offset="1" stop-color="#b8834a" stop-opacity="0"/></radialGradient>
  <radialGradient id="{p}-sage" cx="0.25" cy="0.2" r="0.5"><stop offset="0" stop-color="#9eca84" stop-opacity="0.13"/><stop offset="1" stop-color="#9eca84" stop-opacity="0"/></radialGradient>
  <linearGradient id="{p}-lawn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0f1c12"/><stop offset="1" stop-color="#050906"/></linearGradient>
  <linearGradient id="{p}-wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#222a24"/><stop offset="1" stop-color="#151a17"/></linearGradient>
  <linearGradient id="{p}-timber" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4d3a27"/><stop offset="1" stop-color="#2e2318"/></linearGradient>
  <linearGradient id="{p}-roof" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#0c100e"/><stop offset="1" stop-color="#1c2320"/></linearGradient>
  <linearGradient id="{p}-pv" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#141c26"/><stop offset="1" stop-color="#070b10"/></linearGradient>
  <linearGradient id="{p}-sheen" x1="0" y1="0" x2="1" y2="1"><stop offset="0.12" stop-color="#ffffff" stop-opacity="0"/><stop offset="0.46" stop-color="#d6e6ff" stop-opacity="0.12"/><stop offset="0.56" stop-color="#ffffff" stop-opacity="0.02"/><stop offset="0.9" stop-color="#e3a75a" stop-opacity="0.16"/></linearGradient>
  <linearGradient id="{p}-warm" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffd596"/><stop offset="0.55" stop-color="#e9a95c"/><stop offset="1" stop-color="#b9763a"/></linearGradient>
  <linearGradient id="{p}-warm2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f3c886"/><stop offset="1" stop-color="#a8682f"/></linearGradient>
  <linearGradient id="{p}-pool" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#173b42"/><stop offset="1" stop-color="#081619"/></linearGradient>
  <linearGradient id="{p}-refl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f0b46a" stop-opacity="0.5"/><stop offset="1" stop-color="#f0b46a" stop-opacity="0"/></linearGradient>
  <linearGradient id="{p}-car" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2f393f"/><stop offset="0.45" stop-color="#161c20"/><stop offset="1" stop-color="#0a0e10"/></linearGradient>
  <linearGradient id="{p}-unit" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#dfe4e1"/><stop offset="1" stop-color="#aab3ad"/></linearGradient>
  <radialGradient id="{p}-vig" cx="0.5" cy="0.45" r="0.75"><stop offset="0.6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.55"/></radialGradient>
  <filter id="{p}-glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="14"/></filter>
  <filter id="{p}-soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4"/></filter>
</defs>
<style>
  .{cls} .pv {{ fill: url(#{p}-pv); stroke: #020406; stroke-width: 1.6; }}
  .{cls} .cell {{ fill: none; stroke: #1b2633; stroke-width: 0.8; opacity: 0.8; }}
  .{cls} .slat line {{ stroke: #241b12; stroke-width: 2; }}
  .{cls} .flow {{ fill: none; stroke: #c4e8ab; stroke-width: 3; stroke-linecap: round; stroke-dasharray: 2 16; animation: {p}-flow 1.6s linear infinite; }}
  .{cls} .flow-base {{ fill: none; stroke: #9eca84; stroke-width: 3; stroke-linecap: round; opacity: 0.3; }}
  .{cls} .flow-glow {{ fill: none; stroke: #9eca84; stroke-width: 10; stroke-linecap: round; opacity: 0.25; filter: url(#{p}-soft); }}
  .{cls} .lead {{ stroke: rgba(158, 202, 132, 0.6); stroke-width: 1.5; stroke-dasharray: 3 5; }}
  .{cls} .ldot, .{cls} .lmark {{ fill: #9eca84; }}
  .{cls} .lpill {{ fill: rgba(6, 8, 6, 0.84); stroke: rgba(255, 255, 255, 0.22); stroke-width: 1.2; }}
  .{cls} .ltext {{ fill: #ffffff; font: 700 17px/1 "Manrope Local", "Manrope", Arial, sans-serif; letter-spacing: 1.6px; }}
  .{cls} .twinkle {{ animation: {p}-tw 4s ease-in-out infinite alternate; }}
  @keyframes {p}-flow {{ to {{ stroke-dashoffset: -36; }} }}
  @keyframes {p}-tw {{ from {{ opacity: 0.4; }} to {{ opacity: 1; }} }}
  @media (prefers-reduced-motion: reduce) {{ .{cls} .flow, .{cls} .twinkle {{ animation: none; }} }}
</style>
<rect width="{W}" height="{H}" fill="url(#{p}-sky)"/>
<rect width="{W}" height="{H}" fill="url(#{p}-dusk)"/>
<rect width="{W}" height="{H}" fill="url(#{p}-sage)"/>
<g fill="#f4efe2" class="twinkle">{stars()}</g>
<g transform="translate(1440 236)"><circle r="28" fill="#f1e7cf" opacity="0.92"/><circle cx="12" cy="-8" r="27" fill="#070b08"/></g>
<path d="M0 660 C160 610 300 640 430 622 C600 598 700 640 860 612 C1010 586 1150 628 1300 600 C1420 580 1520 606 1600 596 V1000 H0Z" fill="#0f1913"/>
<path d="M0 700 C200 672 340 694 520 680 C720 664 900 690 1080 674 C1260 658 1420 684 1600 670 V1000 H0Z" fill="#0b140e"/>
<g fill="#070d09">
  <ellipse cx="330" cy="470" rx="34" ry="200"/><rect x="326" y="600" width="8" height="160"/>
  <ellipse cx="1290" cy="500" rx="30" ry="170"/><rect x="1286" y="610" width="8" height="150"/>
  <ellipse cx="1350" cy="540" rx="24" ry="130"/>
</g>
<g fill="#060b07">
  <circle cx="150" cy="560" r="78"/><circle cx="208" cy="500" r="70"/><circle cx="160" cy="455" r="60"/><circle cx="190" cy="612" r="58"/><rect x="164" y="600" width="12" height="160"/>
  <circle cx="1548" cy="560" r="72"/><circle cx="1500" cy="606" r="56"/><circle cx="1590" cy="500" r="62"/><rect x="1538" y="600" width="11" height="160"/>
</g>
<ellipse cx="170" cy="752" rx="70" ry="16" fill="#ffd27f" opacity="0.12" filter="url(#{p}-soft)"/>
<ellipse cx="1544" cy="752" rx="60" ry="14" fill="#ffd27f" opacity="0.1" filter="url(#{p}-soft)"/>
<rect y="{GROUND}" width="{W}" height="{H - GROUND}" fill="url(#{p}-lawn)"/>
<g fill="#ffffff" opacity="0.018">{lawn_stripes()}</g>
<ellipse cx="760" cy="792" rx="560" ry="52" fill="#e3a75a" opacity="0.12" filter="url(#{p}-glow)"/>
<path d="M1176 {GROUND} H1600 V1000 H1330 Z" fill="#0c1012"/>
<path d="M1176 {GROUND} L1330 1000" stroke="#1a2023" stroke-width="2"/>
<rect x="250" y="{GROUND}" width="1010" height="16" fill="#1a201c"/>
<rect x="250" y="{GROUND}" width="1010" height="2" fill="#2e3730"/>
<!-- reflection pool -->
<rect x="852" y="796" width="420" height="50" rx="3" fill="url(#{p}-pool)"/>
{reflections}
<rect x="852" y="796" width="420" height="50" rx="3" fill="none" stroke="#2c3531" stroke-width="3"/>
<rect x="852" y="796" width="420" height="2" fill="#4a5a52" opacity="0.6"/>
<!-- heat pump -->
<g>
  <rect x="198" y="690" width="76" height="60" rx="5" fill="url(#{p}-unit)"/>
  <circle cx="226" cy="720" r="20" fill="#949d98"/><circle cx="226" cy="720" r="15" fill="#626c67"/>
  <path d="M211 720H241M226 705V735M215.4 709.4L236.6 730.6M236.6 709.4L215.4 730.6" stroke="#48514d" stroke-width="2"/>
  <g stroke="#949d98" stroke-width="2"><line x1="252" y1="704" x2="268" y2="704"/><line x1="252" y1="712" x2="268" y2="712"/><line x1="252" y1="720" x2="268" y2="720"/><line x1="252" y1="728" x2="268" y2="728"/><line x1="252" y1="736" x2="268" y2="736"/></g>
  <rect x="204" y="748" width="10" height="5" fill="#2b302d"/><rect x="258" y="748" width="10" height="5" fill="#2b302d"/>
</g>
<!-- plant room with battery and inverter -->
<rect x="285" y="640" width="98" height="{GROUND - 640}" fill="url(#{p}-wall)"/>
<rect x="278" y="628" width="112" height="13" fill="#0b0f0d"/><rect x="278" y="628" width="112" height="2" fill="#2e3731"/>
<rect x="300" y="664" width="34" height="84" rx="4" fill="url(#{p}-unit)"/>
<rect x="306" y="672" width="22" height="3" rx="1.5" fill="#9eca84"/>
<rect x="342" y="664" width="30" height="40" rx="3" fill="url(#{p}-unit)"/>
<rect x="348" y="672" width="18" height="10" rx="1" fill="#1d2622"/><rect x="350" y="676" width="9" height="2" fill="#9eca84"/>
<!-- main house -->
<rect x="380" y="470" width="490" height="{GROUND - 470}" fill="url(#{p}-wall)"/>
<rect x="680" y="470" width="190" height="{GROUND - 470}" fill="url(#{p}-timber)"/>
<g class="slat">{cladding(680, 870, 480, GROUND)}</g>
<polygon points="{poly([B0, B1, T1, T0])}" fill="url(#{p}-roof)"/>
<path d="M{B0[0]} {B0[1]}L{T0[0]} {T0[1]}M{B1[0]} {B1[1]}L{T1[0]} {T1[1]}" stroke="#2f3833" stroke-width="2.5"/>
{pv}
<polygon points="{area}" fill="url(#{p}-sheen)"/>
<path d="M{T0[0] - 4} {T0[1]}H{T1[0] + 4}" stroke="#3c4741" stroke-width="5" stroke-linecap="round"/>
<rect x="345" y="468" width="560" height="14" fill="#0a0d0b"/><rect x="345" y="468" width="560" height="2" fill="#36403a"/>
<g fill="#fff0cf"><circle cx="420" cy="486" r="2.4"/><circle cx="520" cy="486" r="2.4"/><circle cx="620" cy="486" r="2.4"/><circle cx="720" cy="486" r="2.4"/><circle cx="820" cy="486" r="2.4"/></g>
<g fill="#ffd27f" opacity="0.3" filter="url(#{p}-soft)"><ellipse cx="420" cy="500" rx="10" ry="16"/><ellipse cx="520" cy="500" rx="10" ry="16"/><ellipse cx="620" cy="500" rx="10" ry="16"/><ellipse cx="720" cy="500" rx="10" ry="16"/><ellipse cx="820" cy="500" rx="10" ry="16"/></g>
<!-- glazing, main house -->
<rect x="402" y="598" width="290" height="10" fill="#0b0e0c"/>
<rect x="412" y="612" width="262" height="{GROUND - 612}" fill="url(#{p}-warm)"/>
<rect x="412" y="612" width="262" height="{GROUND - 612}" fill="#ffc77a" opacity="0.35" filter="url(#{p}-glow)"/>
<g fill="#0c0f0d"><rect x="406" y="608" width="274" height="6"/><rect x="406" y="608" width="6" height="{GROUND - 608}"/><rect x="674" y="608" width="6" height="{GROUND - 608}"/><rect x="497" y="612" width="5" height="{GROUND - 612}"/><rect x="584" y="612" width="5" height="{GROUND - 612}"/></g>
<g fill="#6b4523" opacity="0.55"><rect x="430" y="712" width="52" height="30" rx="6"/><rect x="600" y="700" width="14" height="42" rx="3"/><circle cx="607" cy="694" r="16"/></g>
<rect x="440" y="500" width="104" height="80" fill="url(#{p}-warm2)"/><rect x="566" y="500" width="104" height="80" fill="url(#{p}-warm2)"/>
<g fill="#0c0f0d"><rect x="436" y="496" width="112" height="5"/><rect x="562" y="496" width="112" height="5"/><rect x="490" y="500" width="4" height="80"/><rect x="616" y="500" width="4" height="80"/></g>
<polygon points="412,612 470,612 412,700" fill="#ffffff" opacity="0.07"/><polygon points="520,612 560,612 450,752 412,752" fill="#ffffff" opacity="0.05"/>
<rect x="752" y="500" width="40" height="214" fill="url(#{p}-warm)"/><rect x="752" y="500" width="40" height="214" fill="#ffc77a" opacity="0.3" filter="url(#{p}-glow)"/>
<rect x="748" y="496" width="48" height="5" fill="#0c0f0d"/>
<!-- glass wing -->
<rect x="865" y="575" width="370" height="{GROUND - 575}" fill="#121714"/>
<rect x="878" y="590" width="344" height="{GROUND - 590}" fill="url(#{p}-warm)"/>
<rect x="878" y="590" width="344" height="{GROUND - 590}" fill="#ffc77a" opacity="0.32" filter="url(#{p}-glow)"/>
<g fill="#5a3b1e" opacity="0.6"><rect x="990" y="704" width="150" height="34" rx="10"/><rect x="984" y="690" width="26" height="48" rx="8"/><rect x="1120" y="690" width="26" height="48" rx="8"/></g>
<polygon points="878,590 950,590 878,690" fill="#ffffff" opacity="0.07"/><polygon points="1060,590 1110,590 990,752 940,752" fill="#ffffff" opacity="0.05"/>
<line x1="1010" y1="590" x2="1010" y2="640" stroke="#3a2a18" stroke-width="2"/><circle cx="1010" cy="646" r="9" fill="#fff1d0"/>
<g fill="#0c0f0d"><rect x="878" y="586" width="344" height="5"/><rect x="961" y="590" width="5" height="{GROUND - 590}"/><rect x="1047" y="590" width="5" height="{GROUND - 590}"/><rect x="1133" y="590" width="5" height="{GROUND - 590}"/></g>
<rect x="852" y="561" width="396" height="16" fill="#0b0e0c"/><rect x="852" y="561" width="396" height="2" fill="#36403a"/>
<!-- hedge and path lights -->
<rect x="250" y="768" width="560" height="22" rx="11" fill="#08110a"/>
<g fill="#ffe2a8"><circle cx="300" cy="768" r="3"/><circle cx="420" cy="768" r="3"/><circle cx="540" cy="768" r="3"/><circle cx="660" cy="768" r="3"/><circle cx="780" cy="768" r="3"/></g>
<g fill="#ffd27f" opacity="0.4" filter="url(#{p}-soft)"><circle cx="300" cy="768" r="10"/><circle cx="420" cy="768" r="10"/><circle cx="540" cy="768" r="10"/><circle cx="660" cy="768" r="10"/><circle cx="780" cy="768" r="10"/></g>
<!-- EV charger -->
<rect x="1266" y="672" width="6" height="{GROUND - 672}" fill="#2a312d"/>
<rect x="1256" y="664" width="26" height="46" rx="5" fill="url(#{p}-unit)"/>
<circle cx="1269" cy="681" r="6" fill="none" stroke="#9eca84" stroke-width="2.5"/>
<!-- car -->
<ellipse cx="1446" cy="768" rx="170" ry="10" fill="#000" opacity="0.5" filter="url(#{p}-soft)"/>
<path d="M1300 744 L1300 724 C1301 712 1312 706 1330 702 L1376 694 C1400 676 1428 664 1466 663 C1506 662 1534 674 1556 690 C1576 694 1590 704 1592 718 L1592 744 Z" fill="url(#{p}-car)"/>
<path d="M1386 694 C1408 678 1432 670 1464 669 C1496 668 1520 678 1538 692 Z" fill="#090d10"/>
<path d="M1394 692 C1410 680 1428 674 1446 672 L1430 692 Z" fill="#8aa2b3" opacity="0.16"/>
<line x1="1458" y1="671" x2="1458" y2="692" stroke="#1d2428" stroke-width="3"/>
<path d="M1314 708 C1380 700 1470 699 1588 708" stroke="#56656d" stroke-width="1.6" fill="none" opacity="0.8"/>
<path d="M1458 696 V736" stroke="#0a0e10" stroke-width="1.5" opacity="0.8"/>
<path d="M1302 716 L1330 711" stroke="#fff4dc" stroke-width="3" stroke-linecap="round"/>
<ellipse cx="1298" cy="716" rx="30" ry="9" fill="#fff1d0" opacity="0.22" filter="url(#{p}-soft)"/>
<path d="M1576 712 L1591 715" stroke="#d4453a" stroke-width="3" stroke-linecap="round"/>
<circle cx="1350" cy="744" r="28" fill="#06090a"/><circle cx="1538" cy="744" r="28" fill="#06090a"/>
<g><circle cx="1350" cy="744" r="23" fill="#0c0f10"/><circle cx="1350" cy="744" r="14" fill="#39434a"/><circle cx="1350" cy="744" r="4" fill="#0c0f10"/>
   <circle cx="1538" cy="744" r="23" fill="#0c0f10"/><circle cx="1538" cy="744" r="14" fill="#39434a"/><circle cx="1538" cy="744" r="4" fill="#0c0f10"/></g>
<!-- energy flowing through the system -->
{flow('M372 484V640H358V664')}
{flow('M372 690H412')}
{flow('M300 742H274')}
{flow('M383 760H1262Q1269 760 1269 752V712')}
{flow('M1278 700C1290 712 1298 718 1312 714')}
<rect width="{W}" height="{H}" fill="url(#{p}-vig)"/>
{lab}
</svg>'''


if __name__ == '__main__':
    import sys
    open(sys.argv[1], 'w').write(home_energy_svg(crop=len(sys.argv) < 3))
