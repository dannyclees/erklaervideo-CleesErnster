#!/usr/bin/env python3
"""Baut das C&E-Erklärvideo als HyperFrames-Komposition – 16:9 und 9:16 aus einer Quelle.

Aufruf:  python3 videos/ce-erklaervideo/src/build.py
Ergebnis: videos/ce-erklaervideo/CE_Erklaervideo_Strategie_<format>_40s_v1.html

Retiming nach Dannys Voiceover: nur SHOTS (Startzeiten) und SUBS anpassen,
dann neu bauen. Alle Animationen hängen relativ an T.<shot>.
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.dirname(HERE)
VERSION = "v1"
TOTAL = 40.0

# (id, start, VO-Zeile) – Dauer ergibt sich aus dem nächsten Start
SHOTS = [
    ("s01", 0.00, "Ein schönes Video …"),
    ("s02", 1.30, "… bringt Dir noch …"),
    ("s03", 2.30, "… keinen einzigen Kunden."),
    ("s04", 3.60, "Likes,"),
    ("s05", 4.30, "Klicks,"),
    ("s06", 4.95, "Komplimente –"),
    ("s07", 5.60, "aber das Telefon bleibt still."),
    ("s08", 7.20, "Weil Menschen nicht kaufen,"),
    ("s09", 8.50, "was sie sehen."),
    ("s10", 10.00, "Sondern was sie fühlen."),
    ("s11", 11.80, "Darum starten wir mit Verkaufspsychologie:"),
    ("s12", 14.00, "Wer ist Dein Wunschkunde?"),
    ("s13", 15.60, "Was treibt ihn an?"),
    ("s14", 17.20, "Was bringt ihn zum Handeln?"),
    ("s15", 19.00, "Ein Handwerksbetrieb bekommt zwei bis fünf Anfragen am Tag."),
    ("s16", 23.00, "Andere wollen drei, vier im Monat –"),
    ("s17", 25.50, "oder in ihrer Region bekannter werden."),
    ("s18", 28.00, "Die Strategie richtet sich nach Deinem Ziel."),
    ("s19", 31.00, "Lass Dein Marketing kostenlos von uns analysieren –"),
    ("s20", 33.90, "Du gehst in jedem Fall mit konkreten Ideen raus."),
    ("s21", 37.00, "Clees & Ernster."),
]

SUBS = [
    (0.0, 1.8, "Ein schönes Video bringt Dir"),
    (1.8, 3.6, "noch keinen einzigen Kunden."),
    (3.6, 5.6, "Likes, Klicks, Komplimente –"),
    (5.6, 7.2, "aber das Telefon bleibt still."),
    (7.2, 10.0, "Weil Menschen nicht kaufen, was sie sehen."),
    (10.0, 11.8, "Sondern was sie fühlen."),
    (11.8, 14.0, "Darum starten wir mit Verkaufspsychologie:"),
    (14.0, 15.6, "Wer ist Dein Wunschkunde?"),
    (15.6, 17.2, "Was treibt ihn an?"),
    (17.2, 19.0, "Was bringt ihn zum Handeln?"),
    (19.0, 21.0, "Ein Handwerksbetrieb bekommt"),
    (21.0, 23.0, "zwei bis fünf Anfragen am Tag."),
    (23.0, 25.5, "Andere wollen drei, vier im Monat –"),
    (25.5, 28.0, "oder in ihrer Region bekannter werden."),
    (28.0, 31.0, "Die Strategie richtet sich nach Deinem Ziel."),
    (31.0, 33.9, "Lass Dein Marketing kostenlos von uns analysieren –"),
    (33.9, 35.6, "Du gehst in jedem Fall"),
    (35.6, 37.4, "mit konkreten Ideen raus."),
]

FORMATS = {"16x9": (1920, 1080), "9x16": (1080, 1920)}


def words(text, cls=""):
    """Wörter einzeln maskiert – für Wort-Stagger aus einer Linie."""
    out = []
    for w in text.split(" "):
        out.append('<span class="m"><span class="w %s">%s</span></span>' % (cls, w))
    return " ".join(out)


# ── Icons (einheitlich: 8er-Strich, runde Enden, viewBox 0 0 120 120) ──────
ICON = {
    "heart": '<path d="M60 100 C20 72 10 52 18 36 C26 20 48 18 60 36 C72 18 94 20 102 36 C110 52 100 72 60 100 Z"/>',
    "cursor": '<path d="M30 18 L30 92 L50 74 L64 104 L78 98 L64 68 L92 68 Z"/>',
    "bubble": '<path d="M18 26 H102 V80 H52 L32 98 V80 H18 Z"/>',
    "phone": '<rect x="34" y="10" width="52" height="100" rx="12"/><path d="M52 96 H68"/>',
    "eye": '<path class="dr" d="M8 60 C28 28 92 28 112 60 C92 92 28 92 8 60 Z"/><circle class="dr" cx="60" cy="60" r="16"/>',
    "person": '<circle class="dr" cx="60" cy="42" r="18"/><path class="dr" d="M24 104 C28 78 44 68 60 68 C76 68 92 78 96 104"/>',
    "pin": '<path d="M60 108 C60 108 24 70 24 46 C24 26 40 12 60 12 C80 12 96 26 96 46 C96 70 60 108 60 108 Z"/><circle cx="60" cy="46" r="12"/>',
    "check": '<path class="dr" d="M26 62 L50 86 L96 36"/>',
    "play": '<path d="M46 34 L88 60 L46 86 Z" fill="currentColor" stroke="none"/>',
    "pause": '<path d="M46 34 V86 M74 34 V86"/>',
    "bell": '<path d="M60 14 C40 14 32 30 32 48 V72 L20 88 H100 L88 72 V48 C88 30 80 14 60 14 Z"/><path d="M50 98 C52 106 68 106 70 98"/>',
}


def icon(name, cls="", extra=""):
    return ('<svg class="ic %s" viewBox="0 0 120 120" fill="none" stroke="currentColor" '
            'stroke-width="8" stroke-linecap="round" stroke-linejoin="round" %s>%s</svg>'
            % (cls, extra, ICON[name]))


def ad_card(cid):
    return """
<div class="ad" id="%(id)s">
  <div class="ad-top" data-layout-ignore><span class="ad-logo"></span><span class="ad-name">Dein Betrieb</span><span class="ad-spons">Gesponsert</span></div>
  <div class="ad-media">
    <div class="ad-shine"></div>
    <div class="ad-play">%(play)s</div>
    <div class="ad-pause">%(pause)s</div>
  </div>
  <div class="ad-bar"><div class="ad-prog"></div></div>
  <div class="ad-row" data-layout-ignore>%(heart)s<span>Gefällt mir</span>%(bubble)s<span>Kommentieren</span></div>
</div>""" % {"id": cid, "play": icon("play"), "pause": icon("pause"),
             "heart": icon("heart", "sm"), "bubble": icon("bubble", "sm")}


# ── Szenen-Inhalt ───────────────────────────────────────────────────────────
SC = {}

SC["s01"] = ('<div class="bg glow"></div>',
             '<div class="duo">' + ad_card("s01-ad") +
             '<div class="txt"><div class="h1" id="s01-h">' + words("SCHÖNES") + '<br>' + words("VIDEO.") + '</div></div></div>')

SC["s02"] = ('<div class="bg glow"></div>',
             '<div class="duo">' + ad_card("s02-ad") +
             '<div class="txt"><div class="kick" id="s02-k">Und dann?</div>'
             '<div class="h1" id="s02-h">' + words("=&nbsp;KUNDEN?", "acc") + '</div></div></div>')

SC["s03"] = ('<div class="bg glow"></div>',
             '<div class="duo">' + ad_card("s03-ad") +
             '<div class="txt"><div class="h1" id="s03-h"><span class="nw">SCHÖN</span><br>'
             '<span class="nw"><span class="neq"><span class="eq">=</span><span class="strike" id="s03-strike"></span></span>'
             '&nbsp;KUNDEN.</span></div></div></div>')

hearts = "".join(icon("heart", "burst hrt h%d" % i) for i in range(10))
SC["s04"] = ('<div class="bg"></div>',
             '<div class="center"><div class="field">' + hearts + '</div>'
             '<div class="mega" id="s04-h">' + words("LIKES,") + '</div></div>')

cursors = "".join('<div class="clk c%d"><span class="ring"></span>%s</div>' % (i, icon("cursor")) for i in range(4))
SC["s05"] = ('<div class="bg"></div>',
             '<div class="center"><div class="field">' + cursors + '</div>'
             '<div class="mega" id="s05-h">' + words("KLICKS,") + '</div></div>')

bubbles = "".join('<div class="bub b%d">%s</div>' % (i, t) for i, t in enumerate(["Wow!", "Mega Video!", "Richtig schön!", "Top gemacht!"]))
SC["s06"] = ('<div class="bg"></div>',
             '<div class="center"><div class="field">' + bubbles + '</div>'
             '<div class="h1 big" id="s06-h">' + words("KOMPLIMENTE –") + '</div></div>')

SC["s07"] = ('<div class="bg dark"></div>',
             '<div class="duo quiet"><div class="phonebox">' + icon("phone", "phone") +
             '<svg class="flat" viewBox="0 0 600 120" fill="none" stroke="currentColor" stroke-width="6" stroke-linecap="round">'
             '<path id="s07-flat" d="M0 60 H600"/></svg></div>'
             '<div class="txt"><div class="kick muted" id="s07-k">Anfragen</div>'
             '<div class="zero" id="s07-n">0</div>'
             '<div class="body" id="s07-b">Das Telefon bleibt still.</div></div></div>')

SC["s08"] = ('<div class="bg"></div><div class="ghost" data-layout-ignore id="s08-g">KAUFEN KAUFEN KAUFEN</div>',
             '<div class="center"><div class="h1" id="s08-h">' + words("MENSCHEN") + '<br>' + words("KAUFEN NICHT,") + '</div></div>')

SC["s09"] = ('<div class="bg"></div>',
             '<div class="duo"><div class="iconbox">' + icon("eye", "eye big") + '</div>'
             '<div class="txt"><div class="h1" id="s09-h"><span class="strk">' + words("WAS SIE") + '<br>' + words("SEHEN.") +
             '<span class="strike thick" id="s09-strike"></span></span></div></div></div>')

SC["s10"] = ('<div class="bg glow2"></div><div class="tunnel">' +
             "".join('<span class="tr t%d"></span>' % i for i in range(5)) + '</div>'
             '<svg class="ecg" viewBox="0 0 1920 300" preserveAspectRatio="none" fill="none" stroke="currentColor" stroke-width="7" stroke-linecap="round" stroke-linejoin="round">'
             '<path id="s10-ecg" d="M0 150 H640 L700 150 L730 60 L770 250 L810 20 L850 210 L880 150 H1920"/></svg>',
             '<div class="center"><div class="kick" id="s10-k">Sondern</div>'
             '<div class="h1" id="s10-h">' + words("WAS SIE") + ' <span class="ul">' + words("FÜHLEN.") +
             '<span class="line" id="s10-line"></span></span></div></div>')

SC["s11"] = ('<div class="bg grid"></div><div class="ghost" data-layout-ignore id="s11-g">PSYCHOLOGIE</div>',
             '<div class="center"><div class="kick" id="s11-k">Darum starten wir mit</div>'
             '<div class="h1 xl" id="s11-h">' + words("VERKAUFS-") + '<br><span class="ul">' + words("PSYCHOLOGIE.") +
             '<span class="line" id="s11-line"></span></span></div></div>')


def step(n, ic_html, word, sub, sid):
    return ('<div class="duo step"><div class="iconbox">%s</div>'
            '<div class="txt"><div class="num" id="%s-n">%s</div>'
            '<div class="h1" id="%s-h">%s</div><div class="body" id="%s-b">%s</div></div></div>'
            % (ic_html, sid, n, sid, words(word), sid, sub))


target = ('<div class="target"><span class="tg r1"></span><span class="tg r2"></span><span class="tg r3"></span>'
          + icon("person", "person") + '</div>')
orbit = ('<div class="orbit"><span class="core"></span>' +
         "".join('<span class="dot d%d"></span>' % i for i in range(4)) + '</div>')
btn = ('<div class="cta-mini"><div class="mbtn" id="s14-btn">Anfrage senden</div>'
       '<div class="mcur" id="s14-cur">' + icon("cursor") + '</div><span class="ring" id="s14-ring"></span></div>')

SC["s12"] = ('<div class="bg grid"></div>', step("01", target, "WUNSCHKUNDE", "Wer ist es wirklich?", "s12"))
SC["s13"] = ('<div class="bg grid"></div>', step("02", orbit, "ANTRIEB", "Was treibt ihn an?", "s13"))
SC["s14"] = ('<div class="bg grid"></div>',
             step("03", btn, "HANDLUNG", "Was bringt ihn zum Handeln?", "s14") +
             '<div class="chain" id="s14-chain"><span>Wunschkunde</span><i></i><span>Antrieb</span><i></i><span class="on">Handlung</span></div>')

notes = "".join('<div class="note n%d">%s<div><b>Neue Anfrage</b><small>%s</small></div></div>' % (i, icon("bell", "sm"), t)
                for i, t in enumerate(["Kontaktformular · 08:12", "Anruf · 09:47", "WhatsApp · 11:03", "Kontaktformular · 14:26", "Anruf · 16:58"]))
SC["s15"] = ('<div class="bg glow"></div>',
             '<div class="duo"><div class="txt"><div class="kick" id="s15-k">Kundenbeispiel · Handwerksbetrieb</div>'
             '<div class="mega num-acc" id="s15-n"><span id="s15-a">0</span>–<span id="s15-b">0</span></div>'
             '<div class="h2" id="s15-h">' + words("ANFRAGEN PRO TAG") + '</div></div>'
             '<div class="notes">' + notes + '</div></div>')

cal = "".join('<span class="cd%s"></span>' % (" hit h%d" % [3, 11, 19, 26].index(i) if i in (3, 11, 19, 26) else "") for i in range(30))
SC["s16"] = ('<div class="bg"></div>',
             '<div class="duo"><div class="txt"><div class="kick" id="s16-k">Andere wollen</div>'
             '<div class="mega" id="s16-n">3–4</div>'
             '<div class="h2" id="s16-h">' + words("ANFRAGEN PRO MONAT") + '</div></div>'
             '<div class="cal" id="s16-cal"><div class="calh">Oktober</div><div class="calg">' + cal + '</div></div></div>')

# Punktfeld „Region“ – feste Positionen (deterministisch), kein Zufall
pts = []
for gy in range(7):
    for gx in range(11):
        x = 40 + gx * 52 + (26 if gy % 2 else 0)
        y = 40 + gy * 52
        d = ((x - 300) ** 2 + (y - 196) ** 2) ** 0.5
        pts.append('<span class="pt" style="left:%dpx;top:%dpx" data-d="%d"></span>' % (x, y, d))
SC["s17"] = ('<div class="bg"></div>',
             '<div class="duo"><div class="txt"><div class="kick" id="s17-k">Oder</div>'
             '<div class="h1" id="s17-h">' + words("BEKANNTER") + '<br>' + words("IN DER REGION.") + '</div></div>'
             '<div class="map" id="s17-map">' + "".join(pts) +
             '<span class="wave w1"></span><span class="wave w2"></span><span class="wave w3"></span>'
             '<div class="mpin">' + icon("pin") + '</div></div></div>')

SC["s18"] = ('<div class="bg grid"></div><div class="ghost" data-layout-ignore id="s18-g">STRATEGIE</div>',
             '<div class="center"><div class="chips"><span class="chip">2–5 / Tag</span><span class="chip">3–4 / Monat</span><span class="chip">Region</span></div>'
             '<div class="h2 muted" id="s18-a">' + words("DEIN ZIEL.") + '</div>'
             '<div class="h1" id="s18-h">' + words("DEINE") + ' <span class="ul">' + words("STRATEGIE.") +
             '<span class="line" id="s18-line"></span></span></div></div>')

SC["s19"] = ('<div class="bg glow"></div>',
             '<div class="duo">' + '<div class="adwrap">' + ad_card("s19-ad") +
             '<div class="notes over">' + "".join('<div class="note k%d">%s<div><b>Neue Anfrage</b><small>gerade eben</small></div></div>' % (i, icon("bell", "sm")) for i in range(3)) + '</div></div>'
             '<div class="txt"><div class="kick" id="s19-k">Jetzt</div>'
             '<div class="h1" id="s19-h">' + words("KOSTENLOSE") + '<br>' + words("MARKETING-") + '<br>' + words("ANALYSE.", "acc") + '</div></div></div>')

SC["s20"] = ('<div class="bg"></div><div class="sparks">' + "".join('<span class="sp p%d"></span>' % i for i in range(8)) + '</div>',
             '<div class="center"><div class="kick" id="s20-k">In jedem Fall</div>'
             '<div class="h1" id="s20-h">' + words("KONKRETE") + '<br><span class="ul">' + words("IDEEN.") +
             '<span class="line" id="s20-line"></span></span></div>'
             '<div class="body" id="s20-b">Für Dein Marketing.</div></div>')

SC["s21"] = ('<div class="bg glow"></div><div class="ghost" data-layout-ignore id="s21-g">STRATEGIE</div>',
             '<div class="center end"><div class="logo" id="s21-logo"><span class="lc">c</span><span class="le">e</span></div>'
             '<div class="brand" id="s21-brand">CLEES &amp; ERNSTER</div>'
             '<div class="claim" id="s21-claim">' + words("Erst die") + ' <span class="ul">' + words("Strategie.") +
             '<span class="line" id="s21-line"></span></span> ' + words("Dann das Bild.") + '</div>'
             '<div class="btn" id="s21-btn">Kostenloses Strategiegespräch <span class="arr">→</span></div></div>')


CSS = r"""
:root{
  --bg:#06080d; --navy:#0b1f45; --acc:#4d8dff; --acc2:#8fb6ff; --ink:#f2f5fa;
  --muted:rgba(242,245,250,.58); --line:rgba(77,141,255,.16);
  --red:#ff5a5f; --yel:#ffc93d; --grn:#3ddc84; --blu:#4d8dff;
  --font:"Archivo","Helvetica Neue",Arial,sans-serif;
}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:__W__px;height:__H__px;overflow:hidden;background:var(--bg);color:var(--ink);font-family:var(--font)}
.scene{position:absolute;inset:0;width:__W__px;height:__H__px;overflow:hidden;background:var(--bg)}
.scene-content{position:absolute;inset:0;z-index:2;display:flex;align-items:center;justify-content:center}
.bg{position:absolute;inset:-4%;z-index:0}
.bg.glow{background:radial-gradient(60% 70% at 70% 40%,rgba(11,31,69,.95),transparent 70%),radial-gradient(40% 50% at 15% 85%,rgba(77,141,255,.14),transparent 70%)}
.bg.glow2{background:radial-gradient(50% 60% at 50% 50%,rgba(77,141,255,.22),transparent 70%)}
.bg.dark{background:radial-gradient(60% 60% at 30% 50%,rgba(11,31,69,.45),transparent 70%)}
.bg.grid{background-image:linear-gradient(var(--line) 2px,transparent 2px),linear-gradient(90deg,var(--line) 2px,transparent 2px),radial-gradient(60% 60% at 50% 50%,rgba(11,31,69,.9),transparent 75%);background-size:96px 96px,96px 96px,100% 100%}
.fx{position:absolute;inset:0;z-index:30;pointer-events:none;
  background:radial-gradient(ellipse at center,transparent 55%,rgba(0,0,0,.45) 100%),
  radial-gradient(rgba(255,255,255,.05) 1px,transparent 1.4px) 0 0/5px 5px,
  radial-gradient(rgba(255,255,255,.035) 1px,transparent 1.4px) 2px 3px/7px 7px}
.wipe{position:absolute;inset:0;z-index:6;background:var(--acc);opacity:0}
.flash{position:absolute;inset:0;z-index:7;background:#dfe9ff;opacity:0}
.ghost{position:absolute;z-index:1;top:50%;left:0;white-space:nowrap;font-weight:900;font-size:calc(var(--mega)*1.6);line-height:1;
  letter-spacing:-.03em;color:rgba(77,141,255,.07);transform:translateY(-50%)}

.m{display:inline-block;overflow:hidden;vertical-align:bottom;padding:0 .02em .06em;margin-bottom:-.06em}
.w{display:inline-block}
.acc{color:var(--acc)}
.mega{font-weight:900;font-size:var(--mega);line-height:.9;letter-spacing:-.04em;font-variant-numeric:tabular-nums}
.h1{font-weight:900;font-size:var(--h1);line-height:.95;letter-spacing:-.035em}
.h1.big{font-size:var(--big)}
.h1.xl{font-size:var(--xl)}
.h2{font-weight:900;font-size:var(--h2);line-height:1;letter-spacing:-.02em}
.kick{font-weight:700;font-size:var(--kick);letter-spacing:.2em;text-transform:uppercase;color:var(--acc);margin-bottom:22px}
.kick.muted,.muted{color:var(--muted)}
.body{font-weight:500;font-size:var(--body);line-height:1.3;color:var(--muted);margin-top:26px;max-width:var(--bodyw)}
.num{font-weight:900;font-size:var(--kick);letter-spacing:.2em;color:var(--acc);margin-bottom:14px}
.ul{position:relative;display:inline-block}
.ul .line{position:absolute;left:0;right:0;bottom:-.02em;height:.09em;min-height:8px;background:var(--acc);transform-origin:left;transform:scaleX(0);border-radius:6px}
.strike{position:absolute;left:-4%;right:-4%;top:50%;height:.11em;background:var(--acc);transform-origin:left;transform:scaleX(0);border-radius:8px}
.strike.thick{height:.1em;top:55%;background:var(--red)}
.strk{position:relative;display:inline-block}
.neq{position:relative;display:inline-block}
.neq .strike{transform-origin:50% 50%;transform:rotate(-58deg) scaleX(0);left:-25%;right:-25%;margin-top:-.055em;background:var(--red)}
.nw{white-space:nowrap}
.duo .h1{font-size:var(--h1d);white-space:nowrap}
.step .h1{font-size:var(--h1s)}
.duo .h2{white-space:nowrap}
.ic{width:100%;height:100%;display:block}
.ic.sm{width:var(--icsm);height:var(--icsm);flex:none}

.center{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;position:relative}
.duo{display:flex;align-items:center;gap:var(--gap)}
.txt{display:flex;flex-direction:column;align-items:flex-start}

/* Anzeigen-Karte */
.ad{width:var(--adw);border-radius:28px;background:#0d1320;border:2px solid rgba(255,255,255,.08);box-shadow:0 40px 120px rgba(0,0,0,.55),0 0 0 1px rgba(77,141,255,.08);overflow:hidden;flex:none}
.ad-top{display:flex;align-items:center;gap:14px;padding:20px 24px;font-size:24px;font-weight:700}
.ad-logo{width:40px;height:40px;border-radius:50%;background:linear-gradient(135deg,var(--acc),#a96bff)}
.ad-spons{margin-left:auto;font-weight:500;color:var(--muted);font-size:22px}
.ad-media{position:relative;aspect-ratio:16/10;overflow:hidden;background:radial-gradient(45% 60% at 18% 20%,rgba(255,201,61,.7),transparent 70%),radial-gradient(45% 55% at 90% 90%,rgba(255,90,140,.65),transparent 70%),radial-gradient(30% 40% at 55% 55%,rgba(77,220,255,.45),transparent 70%),linear-gradient(135deg,#132a5e,#2a59c9 55%,#6a4dff)}
.ad-blob{position:absolute;border-radius:50%;filter:blur(30px)}
.ad-blob.b1{width:60%;height:80%;left:-10%;top:-20%;background:rgba(255,201,61,.55)}
.ad-blob.b2{width:55%;height:70%;right:-15%;bottom:-25%;background:rgba(255,90,140,.5)}
.ad-blob.b3{width:40%;height:50%;left:35%;top:30%;background:rgba(77,220,255,.35)}
.ad-shine{position:absolute;top:-20%;bottom:-20%;width:30%;left:-40%;background:linear-gradient(100deg,transparent,rgba(255,255,255,.35),transparent);transform:skewX(-18deg)}
.ad-play,.ad-pause{position:absolute;left:50%;top:50%;width:120px;height:120px;margin:-60px 0 0 -60px;border-radius:50%;background:rgba(255,255,255,.18);border:3px solid rgba(255,255,255,.7);color:#fff;padding:14px}
.ad-pause{opacity:0}
.ad-bar{height:8px;background:rgba(255,255,255,.1)}
.ad-prog{height:100%;width:100%;background:var(--acc);transform-origin:left;transform:scaleX(.08)}
.ad-row{display:flex;align-items:center;gap:12px;padding:18px 24px;font-size:22px;font-weight:600;color:var(--muted)}
.ad-row span{margin-right:22px}

/* Likes / Klicks / Kommentare */
.field{position:absolute;left:50%;top:50%;width:0;height:0;z-index:0}
.burst{position:absolute;width:var(--hrt);height:var(--hrt);margin:calc(var(--hrt)/-2);color:var(--red);fill:var(--red)}
.clk{position:absolute;width:var(--hrt);height:var(--hrt);margin:calc(var(--hrt)/-2);color:var(--ink)}
.clk .ic{fill:var(--bg)}
.clk .ring{position:absolute;left:-30%;top:-30%;width:70%;height:70%;border-radius:50%;border:5px solid var(--acc);opacity:0}
.bub{position:absolute;white-space:nowrap;padding:22px 34px;border-radius:30px 30px 30px 6px;background:#16203a;border:2px solid rgba(77,141,255,.35);font-size:var(--bub);font-weight:700;transform:translate(-50%,-50%)}

/* Stille */
.quiet .phonebox{position:relative;width:var(--phone);height:var(--phone);color:var(--muted)}
.phone{width:60%;height:60%;margin:0 auto}
.flat{position:absolute;left:-10%;width:120%;bottom:0;height:30%;color:rgba(77,141,255,.55)}
.zero{font-weight:900;font-size:var(--mega);line-height:.9;color:var(--muted);letter-spacing:-.04em}

/* Auge */
.iconbox{width:var(--iconbox);height:var(--iconbox);flex:none;color:var(--acc);position:relative;display:flex;align-items:center;justify-content:center}
.eye .dr,.person .dr,.check .dr{stroke-dasharray:400;stroke-dashoffset:400}

/* Tunnel + EKG */
.tunnel{position:absolute;inset:0;z-index:1}
.tr{position:absolute;left:50%;top:50%;width:400px;height:400px;margin:-200px;border-radius:50%;border:3px solid rgba(77,141,255,.35)}
.ecg{position:absolute;left:0;width:100%;top:50%;height:300px;margin-top:-150px;z-index:1;color:rgba(77,141,255,.45)}
#s10-ecg{stroke-dasharray:2400;stroke-dashoffset:2400}

/* Schritte */
.target{position:relative;width:100%;height:100%}
.tg{position:absolute;inset:0;margin:auto;border-radius:50%;border:5px solid rgba(77,141,255,.5)}
.tg.r1{width:100%;height:100%}.tg.r2{width:70%;height:70%}.tg.r3{width:40%;height:40%;border-color:var(--acc)}
.target .person{position:absolute;inset:22%;width:56%;height:56%;color:var(--ink)}
.orbit{position:relative;width:100%;height:100%}
.orbit .core{position:absolute;left:50%;top:50%;width:26%;height:26%;margin:-13%;border-radius:50%;background:var(--ink);box-shadow:0 0 60px rgba(77,141,255,.6)}
.orbit .dot{position:absolute;left:50%;top:50%;width:20%;height:20%;margin:-10%;border-radius:50%}
.dot.d0{background:var(--red)}.dot.d1{background:var(--yel)}.dot.d2{background:var(--grn)}.dot.d3{background:var(--blu)}
.cta-mini{position:relative;width:100%;height:100%;display:flex;align-items:center;justify-content:center}
.mbtn{padding:28px 44px;border-radius:999px;background:var(--acc);color:#fff;font-weight:800;font-size:var(--mbtn);white-space:nowrap}
.mcur{position:absolute;width:30%;height:30%;right:4%;bottom:6%;color:var(--ink)}
.mcur .ic{fill:var(--bg)}
.cta-mini .ring{position:absolute;width:30%;height:30%;right:18%;bottom:22%;border-radius:50%;border:5px solid var(--ink);opacity:0}
.chain{position:absolute;z-index:3;left:50%;bottom:var(--chainb);transform:translateX(-50%);display:flex;align-items:center;gap:18px;font-weight:700;font-size:var(--chip);color:var(--muted);white-space:nowrap}
.chain span{padding:12px 24px;border:2px solid rgba(77,141,255,.35);border-radius:999px}
.chain span.on{background:var(--acc);color:#fff;border-color:var(--acc)}
.chain i{display:block;width:60px;height:4px;background:var(--acc);border-radius:4px}

/* Zahlen + Benachrichtigungen */
.num-acc{color:var(--ink)}
.num-acc span{color:var(--acc)}
.notes{display:flex;flex-direction:column;gap:18px;width:var(--notew);flex:none}
.note{display:flex;align-items:center;gap:20px;padding:22px 26px;border-radius:22px;background:rgba(22,32,58,.92);border:2px solid rgba(77,141,255,.3);box-shadow:0 20px 50px rgba(0,0,0,.4);color:var(--acc)}
.note b{display:block;color:var(--ink);font-size:var(--noteb);font-weight:800}
.note small{display:block;color:var(--muted);font-size:var(--notes);font-weight:500;margin-top:4px}
.adwrap{position:relative}
.notes.over{position:absolute;right:-60px;top:40px;width:calc(var(--notew)*.92)}

/* Kalender */
.cal{width:var(--calw);padding:30px;border-radius:28px;background:#0d1320;border:2px solid rgba(255,255,255,.08);flex:none}
.calh{font-weight:800;font-size:var(--noteb);margin-bottom:20px;color:var(--muted);letter-spacing:.1em;text-transform:uppercase}
.calg{display:grid;grid-template-columns:repeat(6,1fr);gap:12px}
.calg span{aspect-ratio:1;border-radius:12px;background:rgba(255,255,255,.06)}
.calg span.hit{background:rgba(255,255,255,.06);position:relative}
.calg span.hit::after{content:"";position:absolute;inset:18%;border-radius:50%;background:var(--acc);transform:scale(var(--k,0))}

/* Karte Region */
.map{position:relative;width:640px;height:400px;flex:none}
.pt{position:absolute;width:12px;height:12px;margin:-6px;border-radius:50%;background:rgba(242,245,250,.18)}
.wave{position:absolute;left:300px;top:196px;width:20px;height:20px;margin:-10px;border-radius:50%;border:4px solid var(--acc);opacity:0}
.mpin{position:absolute;left:300px;top:196px;width:110px;height:110px;margin:-104px 0 0 -55px;color:var(--acc)}
.mpin .ic{fill:rgba(77,141,255,.2)}

/* Ziel → Strategie */
.chips{display:flex;gap:20px;margin-bottom:36px;flex-wrap:wrap;justify-content:center}
.chip{padding:14px 28px;border-radius:999px;border:2px solid rgba(77,141,255,.45);font-weight:700;font-size:var(--chip);color:var(--acc2)}
#s18-a{margin-bottom:14px}

/* Funken */
.sparks{position:absolute;left:50%;top:44%;z-index:1}
.sp{position:absolute;width:6px;height:120px;margin:-60px -3px;background:linear-gradient(var(--acc),transparent);border-radius:6px;transform-origin:50% 100%}

/* Ende */
.end{gap:0}
.logo{width:var(--logo);height:var(--logo);border-radius:28%;background:#0d1320;border:2px solid rgba(77,141,255,.4);display:flex;align-items:center;justify-content:center;font-weight:900;font-size:calc(var(--logo)*.5);letter-spacing:-.06em;margin-bottom:30px}
.lc{color:#fff}.le{color:var(--acc)}
.brand{font-weight:900;font-size:var(--brand);letter-spacing:.04em;margin-bottom:22px}
.claim{font-weight:700;font-size:var(--claim);color:var(--ink);margin-bottom:46px}
.claim .line{height:.12em}
.btn{display:inline-flex;align-items:center;gap:18px;padding:30px 52px;border-radius:999px;background:var(--acc);color:#fff;font-weight:800;font-size:var(--btn);box-shadow:0 20px 60px rgba(77,141,255,.45)}

/* Untertitel (nur 9:16) */
.subs{position:absolute;inset:0;z-index:20;pointer-events:none}
.sub{position:absolute;left:90px;right:140px;bottom:640px;text-align:center;opacity:0;visibility:hidden}
.sub span{display:inline-block;padding:14px 26px;border-radius:16px;background:rgba(6,8,13,.82);font-weight:700;font-size:40px;line-height:1.25;color:var(--ink)}
"""

CSS_169 = r"""
:root{--brand:100px;--mega:250px;--h1:170px;--h1d:132px;--h1s:132px;--big:150px;--xl:150px;--h2:84px;--kick:32px;--body:40px;--bodyw:900px;--gap:110px;--adw:720px;
  --icsm:34px;--hrt:150px;--bub:42px;--phone:420px;--iconbox:320px;--mbtn:40px;--chip:30px;--chainb:90px;--notew:560px;--noteb:30px;--notes:28px;
  --calw:560px;--logo:200px;--claim:64px;--btn:44px}
.scene-content{padding:110px 150px}
"""

CSS_916 = r"""
:root{--brand:76px;--mega:200px;--h1:118px;--h1d:104px;--h1s:96px;--big:84px;--xl:100px;--h2:72px;--kick:28px;--body:38px;--bodyw:820px;--gap:60px;--adw:760px;
  --icsm:30px;--hrt:120px;--bub:38px;--phone:300px;--iconbox:300px;--mbtn:36px;--chip:28px;--chainb:690px;--notew:760px;--noteb:30px;--notes:28px;
  --calw:600px;--logo:150px;--claim:46px;--btn:36px}
.scene-content{padding:250px 140px 800px 90px}
.duo{flex-direction:column;gap:var(--gap)}
.txt{align-items:center;text-align:center}
.duo.quiet{gap:30px}
.step .iconbox{width:260px;height:260px}
.notes{gap:14px}
.notes .note:nth-child(n+4){display:none}
.note{padding:16px 22px}
.notes.over{right:-30px;top:30px;width:600px}
.map{transform:scale(.95)}
.chain{gap:10px}.chain i{width:30px}
.claim{text-align:center;max-width:850px}
.chain{display:none}
#s19-ad{width:560px}
.notes.over{width:520px}
.cal{width:440px;padding:22px}
.calg{gap:9px}
.btn{padding:26px 40px}
"""

JS = r"""
window.__timelines = window.__timelines || {};
var tl = gsap.timeline({ paused: true });
var T = __T__, END = __END__, V = __VERT__;
var M = {
  tempo: 0.85,
  dur:  { xs: 0.12, s: 0.25, m: 0.45, l: 0.8 },
  ease: { enter: "power4.out", exit: "power3.in", accent: "expo.out", hold: "sine.inOut", pop: "back.out(1.2)" },
  stagger: 0.05
};
function d(k) { return M.dur[k] * M.tempo; }
function q(s) { return document.querySelector(s); }

// Szenen-Sichtbarkeit (harte Schnitte)
Object.keys(T).forEach(function (id) {
  if (id !== "s01") tl.set("#" + id, { autoAlpha: 1 }, T[id]);
  if (END[id] < __TOTAL__) tl.set("#" + id, { autoAlpha: 0 }, END[id]);
});

// ── Bausteine ──
function slam(sel, t, st) { tl.from(sel + " .w", { yPercent: 115, duration: d("m"), ease: M.ease.enter, stagger: st || M.stagger }, t); }
function punch(sel, t, from) { tl.fromTo(sel, { scale: from || 1.5, autoAlpha: 0 }, { scale: 1, autoAlpha: 1, duration: d("s") + 0.05, ease: M.ease.accent }, t); }
function kick(sel, t) { tl.from(sel, { x: -40, autoAlpha: 0, duration: d("m"), ease: M.ease.accent }, t); }
function line(sel, t) { tl.to(sel, { scaleX: 1, duration: d("m"), ease: M.ease.accent }, t); }
function push(id, s) { tl.fromTo("#" + id + " .scene-content", { scale: 1 }, { scale: s || 1.04, duration: END[id] - T[id], ease: "none" }, T[id]); }
function wipe(id, dir) { var w = "#" + id + " .wipe"; tl.set(w, { xPercent: 0, opacity: 1 }, T[id]); tl.to(w, { xPercent: dir < 0 ? -101 : 101, duration: 0.3, ease: "power3.in" }, T[id]); }
function flash(id, t) { var f = "#" + id + " .flash"; tl.set(f, { opacity: 0.75 }, t); tl.to(f, { opacity: 0, duration: 0.3, ease: "power2.out" }, t); }
function shake(id, t, a) {
  var c = "#" + id + " .scene-content", k = a || 1;
  [[-14, 8], [12, -6], [-8, 5], [5, -3], [0, 0]].forEach(function (p, i) {
    tl.to(c, { x: p[0] * k, y: p[1] * k, duration: 0.035, ease: "none" }, t + i * 0.035);
  });
}
function ghost(id, dx) { tl.fromTo("#" + id + " .ghost", { x: 0 }, { x: dx, duration: END[id] - T[id], ease: "none" }, T[id]); }
function shine(card, t) { tl.fromTo(card + " .ad-shine", { left: "-40%" }, { left: "130%", duration: 0.9, ease: "power2.inOut" }, t); }

// ── S01–S03 Hook: Schön ≠ Kunden ──
(function () {
  var t = T.s01;
  shine("#s01-ad", t + 0.1);
  tl.fromTo("#s01-ad .ad-play", { scale: 1 }, { scale: 1.08, duration: 0.6, yoyo: true, repeat: 1, ease: M.ease.hold }, t);
  tl.fromTo("#s01-ad .ad-prog", { scaleX: 0.08 }, { scaleX: 0.3, duration: 1.3, ease: "none" }, t);
  tl.fromTo("#s01-ad", { rotation: -1.5, y: 10 }, { rotation: 0, y: 0, duration: 1.3, ease: "power2.out" }, t);
  push("s01", 1.03);

  t = T.s02;
  tl.fromTo("#s02-ad .ad-prog", { scaleX: 0.3 }, { scaleX: 0.55, duration: 1.0, ease: "none" }, t);
  kick("#s02-k", t + 0.02);
  slam("#s02-h", t + 0.08);
  shine("#s02-ad", t + 0.2);
  push("s02", 1.03);

  t = T.s03;
  tl.set("#s03-ad .ad-prog", { scaleX: 0.55 }, t);
  tl.to("#s03-ad .ad-play", { autoAlpha: 0, duration: 0.05 }, t + 0.35);
  tl.to("#s03-ad .ad-pause", { opacity: 1, duration: 0.05 }, t + 0.35);
  tl.to("#s03-ad .ad-media", { filter: "grayscale(1) brightness(.55)", duration: 0.25, ease: "power2.out" }, t + 0.35);
  tl.fromTo("#s03-strike", { scaleX: 0, rotation: -58 }, { scaleX: 1, rotation: -58, duration: d("s"), ease: M.ease.accent }, t + 0.4);
  flash("s03", t + 0.4);
  shake("s03", t + 0.42, 1.2);
  tl.fromTo("#s03-ad", { scale: 1 }, { scale: 0.96, duration: 0.9, ease: "power2.out" }, t + 0.4);
})();

// ── S04–S06 Lärm: Likes, Klicks, Komplimente ──
(function () {
  var t = T.s04, H = [[-560, -260], [520, -220], [-380, 260], [430, 280], [-720, 30], [700, 40], [-150, -330], [180, 330], [-250, -120], [270, 120]];
  if (V) H = H.map(function (p) { return [p[0] * 0.55, p[1] * 1.5]; });
  wipe("s04", 1);
  punch("#s04-h", t + 0.05, 1.6);
  H.forEach(function (p, i) {
    var el = "#s04 .h" + i, tt = t + 0.08 + i * 0.03;
    tl.fromTo(el, { x: 0, y: 0, scale: 0.2, rotation: 0, autoAlpha: 1 },
      { x: p[0], y: p[1] - 60, scale: 0.5 + (i % 3) * 0.25, rotation: (i % 2 ? 14 : -14), duration: 0.55, ease: "expo.out" }, tt);
  });
  shake("s04", t + 0.08, 0.7);

  t = T.s05;
  var C = [[-560, -200], [540, -160], [-420, 230], [460, 250]];
  if (V) C = [[-280, -440], [280, -360], [-260, 380], [270, 440]];
  C.forEach(function (p, i) {
    var el = "#s05 .c" + i, tt = t + 0.04 + i * 0.09;
    tl.fromTo(el, { x: p[0] * 1.4, y: p[1] * 1.4, autoAlpha: 0 }, { x: p[0], y: p[1], autoAlpha: 1, duration: 0.22, ease: "power3.out" }, tt);
    tl.to(el + " .ic", { scale: 0.82, duration: 0.06, yoyo: true, repeat: 1 }, tt + 0.22);
    tl.fromTo(el + " .ring", { scale: 0.2, opacity: 1 }, { scale: 2.2, opacity: 0, duration: 0.35, ease: "power2.out" }, tt + 0.24);
  });
  punch("#s05-h", t + 0.02, 0.6);

  t = T.s06;
  var B = [[-560, -230], [480, -250], [-500, 240], [520, 220]];
  if (V) B = [[-140, -430], [150, -320], [-120, 360], [120, 460]];
  B.forEach(function (p, i) {
    tl.fromTo("#s06 .b" + i, { x: p[0], y: p[1] + 30, scale: 0.4, autoAlpha: 0 }, { x: p[0], y: p[1], scale: 1, autoAlpha: 1, duration: 0.25, ease: M.ease.pop }, t + 0.05 + i * 0.08);
  });
  slam("#s06-h", t + 0.02, 0.04);
  push("s06", 1.05);
})();

// ── S07 Stille ──
(function () {
  var t = T.s07;
  tl.fromTo("#s07-flat", { strokeDasharray: 600, strokeDashoffset: 600 }, { strokeDashoffset: 0, duration: 1.2, ease: "none" }, t + 0.1);
  kick("#s07-k", t + 0.15);
  tl.fromTo("#s07-n", { yPercent: -40, autoAlpha: 0 }, { yPercent: 0, autoAlpha: 1, duration: 0.35, ease: "bounce.out" }, t + 0.25);
  tl.from("#s07-b", { y: 20, autoAlpha: 0, duration: 0.4, ease: "power2.out" }, t + 0.55);
  push("s07", 1.025);
})();

// ── S08–S10 Das Weil: sehen → fühlen ──
(function () {
  var t = T.s08;
  wipe("s08", -1);
  slam("#s08-h", t + 0.08, 0.07);
  ghost("s08", -400);
  push("s08", 1.05);

  t = T.s09;
  tl.to("#s09 .eye .dr", { strokeDashoffset: 0, duration: 0.6, ease: "power2.out", stagger: 0.12 }, t + 0.05);
  slam("#s09-h", t + 0.1);
  tl.to("#s09-strike", { scaleX: 1, duration: d("s"), ease: M.ease.accent }, t + 1.0);
  tl.to("#s09-h .w", { color: "rgba(242,245,250,.4)", duration: 0.2 }, t + 1.05);
  tl.to("#s09 .eye", { color: "rgba(242,245,250,.35)", duration: 0.2 }, t + 1.05);
  shake("s09", t + 1.02, 0.6);
  push("s09", 1.03);

  t = T.s10;
  for (var i = 0; i < 5; i++) {
    tl.fromTo("#s10 .t" + i, { scale: 0.2 + i * 0.5, autoAlpha: 0.9 }, { scale: 4 + i * 1.2, autoAlpha: 0, duration: 1.2, ease: "power2.out" }, t + i * 0.05);
  }
  tl.fromTo("#s10 .scene-content", { scale: 1.6 }, { scale: 1, duration: 0.5, ease: M.ease.accent }, t);
  tl.to("#s10-ecg", { strokeDashoffset: 0, duration: 1.1, ease: "power1.inOut" }, t + 0.1);
  kick("#s10-k", t + 0.15);
  slam("#s10-h", t + 0.2);
  line("#s10-line", t + 0.95);
  tl.to("#s10 .ul .w", { color: "#4d8dff", duration: 0.2 }, t + 0.95);
})();

// ── S11 Verkaufspsychologie ──
(function () {
  var t = T.s11;
  flash("s11", t);
  kick("#s11-k", t + 0.05);
  slam("#s11-h", t + 0.15, 0.08);
  shake("s11", t + 0.5, 0.8);
  line("#s11-line", t + 0.9);
  ghost("s11", -500);
  tl.fromTo("#s11 .bg", { backgroundPosition: "0px 0px" }, { backgroundPosition: "0px -96px", duration: END.s11 - t, ease: "none" }, t);
  push("s11", 1.05);
})();

// ── S12–S14 Die drei Schritte ──
(function () {
  var t = T.s12;
  wipe("s12", 1);
  [".r1", ".r2", ".r3"].forEach(function (r, i) { tl.from("#s12 " + r, { scale: 0, duration: 0.45, ease: M.ease.accent }, t + 0.05 + i * 0.07); });
  tl.to("#s12 .person .dr", { strokeDashoffset: 0, duration: 0.55, ease: "power2.out", stagger: 0.1 }, t + 0.25);
  tl.to("#s12 .r3", { scale: 1.12, duration: 0.25, yoyo: true, repeat: 1, ease: M.ease.hold }, t + 0.8);
  kick("#s12-n", t + 0.05); slam("#s12-h", t + 0.1);
  tl.from("#s12-b", { y: 18, autoAlpha: 0, duration: 0.35, ease: "power2.out" }, t + 0.45);
  push("s12", 1.04);

  t = T.s13;
  var R = V ? 110 : 150;
  for (var i = 0; i < 4; i++) {
    var a0 = i * Math.PI / 2;
    (function (i, a0) {
      var o = { a: 0 };
      var el = q("#s13 .d" + i);
      tl.fromTo(o, { a: 0 }, { a: Math.PI * 1.5, duration: END.s13 - t, ease: "power2.out",
        onUpdate: function () { var r = R * Math.min(1, 0.3 + o.a * 1.2); el.style.transform = "translate(" + (Math.cos(a0 + o.a) * r) + "px," + (Math.sin(a0 + o.a) * r) + "px)"; } }, t);
    })(i, a0);
  }
  tl.from("#s13 .core", { scale: 0, duration: 0.4, ease: M.ease.pop }, t + 0.05);
  kick("#s13-n", t + 0.05); slam("#s13-h", t + 0.1);
  tl.from("#s13-b", { y: 18, autoAlpha: 0, duration: 0.35, ease: "power2.out" }, t + 0.45);
  push("s13", 1.04);

  t = T.s14;
  tl.from("#s14-btn", { scale: 0.6, autoAlpha: 0, duration: 0.35, ease: M.ease.pop }, t + 0.05);
  tl.from("#s14-cur", { x: 160, y: 140, duration: 0.45, ease: "power3.out" }, t + 0.2);
  tl.to("#s14-btn", { scale: 0.92, duration: 0.07, yoyo: true, repeat: 1 }, t + 0.66);
  tl.fromTo("#s14-ring", { scale: 0.2, opacity: 1 }, { scale: 2.4, opacity: 0, duration: 0.45, ease: "power2.out" }, t + 0.68);
  tl.to("#s14-btn", { backgroundColor: "#3ddc84", duration: 0.15 }, t + 0.7);
  kick("#s14-n", t + 0.05); slam("#s14-h", t + 0.1);
  tl.from("#s14-b", { y: 18, autoAlpha: 0, duration: 0.35, ease: "power2.out" }, t + 0.45);
  tl.from("#s14-chain > *", { autoAlpha: 0, y: 20, duration: 0.3, ease: "power3.out", stagger: 0.07 }, t + 0.95);
  push("s14", 1.04);
})();

// ── S15–S18 Jede Größe ──
(function () {
  var t = T.s15;
  flash("s15", t);
  kick("#s15-k", t + 0.05);
  tl.from("#s15-n", { scale: 1.4, autoAlpha: 0, duration: 0.35, ease: M.ease.accent }, t + 0.1);
  var a = { v: 0 }, b = { v: 0 };
  tl.to(a, { v: 2, duration: 0.6, ease: "power2.out", onUpdate: function () { q("#s15-a").textContent = Math.round(a.v); } }, t + 0.15);
  tl.to(b, { v: 5, duration: 0.9, ease: "power2.out", onUpdate: function () { q("#s15-b").textContent = Math.round(b.v); } }, t + 0.35);
  slam("#s15-h", t + 0.4);
  var n = V ? 3 : 5;
  for (var i = 0; i < n; i++) {
    tl.from("#s15 .n" + i, { x: V ? 0 : 120, y: V ? -40 : 0, autoAlpha: 0, duration: 0.3, ease: "power4.out" }, t + 0.6 + i * 0.5);
    tl.to("#s15 .n" + i + " .ic", { rotation: 18, duration: 0.06, yoyo: true, repeat: 3 }, t + 0.7 + i * 0.5);
  }
  push("s15", 1.03);

  t = T.s16;
  wipe("s16", -1);
  kick("#s16-k", t + 0.05);
  punch("#s16-n", t + 0.1, 1.5);
  slam("#s16-h", t + 0.3);
  tl.from("#s16-cal", { y: 60, autoAlpha: 0, duration: 0.4, ease: "power4.out" }, t + 0.15);
  [0, 1, 2, 3].forEach(function (i) { tl.fromTo("#s16 .h" + i, { "--k": 0 }, { "--k": 1, duration: 0.3, ease: M.ease.pop }, t + 0.6 + i * 0.32); });
  push("s16", 1.03);

  t = T.s17;
  kick("#s17-k", t + 0.05);
  slam("#s17-h", t + 0.1, 0.06);
  tl.from("#s17 .mpin", { y: -120, autoAlpha: 0, duration: 0.4, ease: "bounce.out" }, t + 0.15);
  [".w1", ".w2", ".w3"].forEach(function (w, i) {
    tl.fromTo("#s17 " + w, { scale: 1, opacity: 0.9 }, { scale: 34, opacity: 0, duration: 1.4, ease: "power1.out" }, t + 0.5 + i * 0.45);
  });
  document.querySelectorAll("#s17 .pt").forEach(function (p) {
    var dd = parseFloat(p.getAttribute("data-d"));
    tl.to(p, { backgroundColor: "#4d8dff", scale: 1.3, duration: 0.25, ease: "power2.out" }, t + 0.5 + dd / 330);
  });
  push("s17", 1.03);

  t = T.s18;
  tl.from("#s18 .chip", { y: 30, autoAlpha: 0, duration: 0.3, ease: "power3.out", stagger: 0.08 }, t + 0.05);
  slam("#s18-a", t + 0.15);
  slam("#s18-h", t + 1.0, 0.07);
  line("#s18-line", t + 1.6);
  tl.to("#s18 .chip", { borderColor: "#4d8dff", color: "#f2f5fa", duration: 0.2, stagger: 0.06 }, t + 1.6);
  shake("s18", t + 1.62, 0.5);
  ghost("s18", -420);
  push("s18", 1.04);
})();

// ── S19 Payoff: dieselbe Anzeige – jetzt mit Anfragen ──
(function () {
  var t = T.s19;
  wipe("s19", 1);
  tl.from("#s19-ad", { scale: 0.9, rotation: -2, duration: 0.5, ease: M.ease.accent }, t + 0.05);
  tl.fromTo("#s19-ad .ad-prog", { scaleX: 0.55 }, { scaleX: 1, duration: 2.6, ease: "none" }, t);
  shine("#s19-ad", t + 0.2);
  [0, 1, 2].forEach(function (i) {
    tl.from("#s19 .k" + i, { x: 80, scale: 0.8, autoAlpha: 0, duration: 0.3, ease: M.ease.pop }, t + 0.45 + i * 0.4);
    tl.to("#s19 .k" + i + " .ic", { rotation: 18, duration: 0.06, yoyo: true, repeat: 3 }, t + 0.55 + i * 0.4);
  });
  kick("#s19-k", t + 0.1);
  slam("#s19-h", t + 0.2, 0.07);
  push("s19", 1.03);
})();

// ── S20 Konkrete Ideen ──
(function () {
  var t = T.s20;
  for (var i = 0; i < 8; i++) {
    tl.set("#s20 .p" + i, { rotation: i * 45 }, t);
    tl.fromTo("#s20 .p" + i, { scaleY: 0, y: 0, opacity: 1 }, { scaleY: 1, y: -(V ? 260 : 300), opacity: 0, duration: 0.7, ease: "power3.out" }, t + 0.9);
  }
  kick("#s20-k", t + 0.05);
  slam("#s20-h", t + 0.12, 0.08);
  line("#s20-line", t + 0.8);
  tl.to("#s20 .ul .w", { color: "#4d8dff", duration: 0.2 }, t + 0.8);
  tl.from("#s20-b", { y: 20, autoAlpha: 0, duration: 0.4, ease: "power2.out" }, t + 1.1);
  push("s20", 1.04);
})();

// ── S21 Ende: letzter Frame = Peak ──
(function () {
  var t = T.s21;
  flash("s21", t);
  tl.from("#s21-logo", { scale: 0, rotation: -20, duration: 0.5, ease: "back.out(1.6)" }, t + 0.05);
  tl.from("#s21-brand", { y: 30, autoAlpha: 0, duration: 0.45, ease: M.ease.accent }, t + 0.3);
  slam("#s21-claim", t + 0.6, 0.06);
  line("#s21-line", t + 1.2);
  tl.from("#s21-btn", { y: 40, scale: 0.8, autoAlpha: 0, duration: 0.45, ease: "back.out(1.5)" }, t + 0.8);
  tl.to("#s21-btn", { scale: 1.05, duration: 0.35, yoyo: true, repeat: 1, ease: M.ease.hold }, t + 1.7);
  tl.fromTo("#s21-btn .arr", { x: 0 }, { x: 10, duration: 0.3, yoyo: true, repeat: 3, ease: M.ease.hold }, t + 1.8);
  ghost("s21", -260);
})();

// ── Untertitel (9:16) ──
document.querySelectorAll(".sub").forEach(function (el) {
  var a = parseFloat(el.getAttribute("data-a")), b = parseFloat(el.getAttribute("data-b"));
  tl.set(el, { autoAlpha: 1 }, a);
  if (b < __TOTAL__) tl.set(el, { autoAlpha: 0 }, b);
});

window.__timelines["main"] = tl;
"""


def build(fmt):
    W, H = FORMATS[fmt]
    vert = fmt == "9x16"
    font = open(os.path.join(HERE, "font-archivo.css"), encoding="utf-8").read()
    starts = {s[0]: s[1] for s in SHOTS}
    ends = {}
    for i, s in enumerate(SHOTS):
        ends[s[0]] = SHOTS[i + 1][1] if i + 1 < len(SHOTS) else TOTAL

    scenes = []
    for i, (sid, start, vo) in enumerate(SHOTS):
        dur = round(ends[sid] - start, 3)
        deco, content = SC[sid]
        vis = '' if i == 0 else ' style="visibility:hidden;"'
        scenes.append(
            '\n<!-- %s (%.2f–%.2fs) | VO: "%s" -->\n'
            '<div class="scene clip" id="%s" data-start="%s" data-duration="%s" data-track-index="0"%s>\n'
            '%s\n<div class="scene-content">%s</div>\n<div class="wipe"></div><div class="flash"></div>\n</div>'
            % (sid, start, ends[sid], vo, sid, start, dur, vis, deco, content))

    subs = '\n<div class="fx clip" id="fx" data-start="0" data-duration="%s" data-track-index="2"></div>' % TOTAL
    if vert:
        subs += ('\n<div class="subs clip" id="subs" data-start="0" data-duration="%s" data-track-index="1">%s</div>'
                % (TOTAL, "".join('<div class="sub" data-a="%s" data-b="%s"><span>%s</span></div>' % (a, b, t) for a, b, t in SUBS)))

    css = CSS + (CSS_916 if vert else CSS_169)
    css = css.replace("__W__", str(W)).replace("__H__", str(H))
    js = (JS.replace("__T__", json.dumps(starts)).replace("__END__", json.dumps(ends))
          .replace("__VERT__", "true" if vert else "false").replace("__TOTAL__", str(TOTAL)))

    html = """<!doctype html>
<!--
  Clees & Ernster – Erklärvideo „Erst die Strategie. Dann das Bild.“
  Format %(fmt)s · %(total)ss · %(ver)s · generiert von src/build.py (nicht von Hand editieren)
  Timing = Schätzung nach Skript (ca. 2,5 Wörter/s). Nach Dannys VO-Aufnahme in build.py retimen.
  Farben/Logo = Platzhalter, bis echte Markenwerte vorliegen.
-->
<html lang="de" style="overflow:hidden; margin:0">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=%(W)s, height=%(H)s" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@hyperframes/core/dist/hyperframe.runtime.iife.js"></script>
<style>
%(font)s
%(css)s
</style>
</head>
<body class="f%(fmt)s">
<div id="main" data-composition-id="main" data-width="%(W)s" data-height="%(H)s" data-start="0" data-duration="%(total)s">
%(scenes)s
%(subs)s
</div>
<script>
%(js)s
</script>
</body>
</html>
""" % {"fmt": fmt, "total": TOTAL, "ver": VERSION, "W": W, "H": H, "font": font, "css": css,
       "scenes": "".join(scenes), "subs": subs, "js": js}
    out = os.path.join(OUTDIR, "CE_Erklaervideo_Strategie_%s_40s_%s.html" % (fmt, VERSION))
    open(out, "w", encoding="utf-8").write(html)
    print(out)


if __name__ == "__main__":
    for f in FORMATS:
        build(f)
