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
VERSION = "v2"
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


def chars(text, cls=""):
    """Buchstaben einzeln (für 1–2 Hero-Wörter), Maske pro Wort."""
    out = []
    for w in text.split(" "):
        out.append('<span class="m">' + "".join('<span class="w ch %s">%s</span>' % (cls, c) for c in w) + '</span>')
    return " ".join(out)


def reel(rid):
    """Ziffernrolle 0–9 zweimal: Index 10+n = Ziffer n nach einer Extrarunde."""
    return '<span class="odo"><span class="reel" id="%s">%s</span></span>' % (rid, "".join("<span>%d</span>" % (i % 10) for i in range(20)))


RAIL = ["Wunschkunde", "Antrieb", "Handlung"]


def rail(sid, k):
    """Fortschrittsschiene 01–03: Schritte < k sind erledigt, Schritt k wird in dieser Szene aktiv."""
    parts = []
    for i in range(1, 4):
        if i > 1:
            if i < k:
                parts.append('<i class="rl"><b style="transform:scaleX(1)"></b></i>')
            else:
                parts.append('<i class="rl"><b%s></b></i>' % (' class="anim"' if i == k else ""))
        cls = "rn" + (" on" if i < k else "") + (" cur" if i == k else "")
        parts.append('<span class="%s">0%d %s</span>' % (cls, i, RAIL[i - 1]))
    return '<div class="rail" id="%s-rail">%s</div>' % (sid, "".join(parts))


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
             '<div class="txt"><div class="h1" id="s01-h">' + chars("SCHÖNES") + '<br>' + chars("VIDEO.") + '</div></div></div>')

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
             '<div class="mega" id="s04-h">' + chars("LIKES,") + '</div></div>')

cursors = "".join('<div class="clk c%d"><span class="ring"></span>%s</div>' % (i, icon("cursor")) for i in range(4))
SC["s05"] = ('<div class="bg"></div>',
             '<div class="center"><div class="field">' + cursors + '</div>'
             '<div class="mega" id="s05-h">' + chars("KLICKS,") + '</div></div>')

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
             '<div class="h1 xl" id="s11-h">' + words("VERKAUFS-") + '<br><span class="ul">' + chars("PSYCHOLOGIE.") +
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

SC["s12"] = ('<div class="bg grid"></div>' + rail("s12", 1), step("01", target, "WUNSCHKUNDE", "Wer ist es wirklich?", "s12"))
SC["s13"] = ('<div class="bg grid"></div>' + rail("s13", 2), step("02", orbit, "ANTRIEB", "Was treibt ihn an?", "s13"))
SC["s14"] = ('<div class="bg grid"></div>' + rail("s14", 3),
             step("03", btn, "HANDLUNG", "Was bringt ihn zum Handeln?", "s14"))

notes = "".join('<div class="note n%d">%s<div><b>Neue Anfrage</b><small>%s</small></div></div>' % (i, icon("bell", "sm"), t)
                for i, t in enumerate(["Kontaktformular · 08:12", "Anruf · 09:47", "WhatsApp · 11:03", "Kontaktformular · 14:26", "Anruf · 16:58"]))
SC["s15"] = ('<div class="bg glow"></div>',
             '<div class="duo"><div class="txt"><div class="kick" id="s15-k">Kundenbeispiel · Handwerksbetrieb</div>'
             '<div class="mega num-acc" id="s15-n">' + reel("s15-ra") + '<span class="dash">–</span>' + reel("s15-rb") + '</div>'
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
             '<div class="h1" id="s18-h">' + words("DEINE") + ' <span class="ul">' + chars("STRATEGIE.") +
             '<span class="line" id="s18-line"></span></span></div></div>')

SC["s19"] = ('<div class="bg glow"></div>',
             '<div class="duo">' + '<div class="adwrap">' + ad_card("s19-ad") +
             '<div class="notes over">' + "".join('<div class="note k%d">%s<div><b>Neue Anfrage</b><small>gerade eben</small></div></div>' % (i, icon("bell", "sm")) for i in range(3)) + '</div></div>'
             '<div class="txt"><div class="kick" id="s19-k">Jetzt</div>'
             '<div class="h1" id="s19-h">' + '<span class="hlw"><span class="hlb" id="s19-hlb"></span>' + words("KOSTENLOSE") + '</span><br>' + words("MARKETING-") + '<br>' + words("ANALYSE.", "acc") + '</div></div></div>')

SC["s20"] = ('<div class="bg"></div><div class="sparks">' + "".join('<span class="sp p%d"></span>' % i for i in range(8)) + '</div>',
             '<div class="center"><div class="kick" id="s20-k">In jedem Fall</div>'
             '<div class="h1" id="s20-h">' + words("KONKRETE") + '<br><span class="ul">' + chars("IDEEN.") +
             '<span class="line" id="s20-line"></span></span></div>'
             '<div class="body" id="s20-b">Für Dein Marketing.</div></div>')

SC["s21"] = ('<div class="bg glow"></div><div class="ghost" data-layout-ignore id="s21-g">STRATEGIE</div>',
             '<div class="center end"><div class="logo" id="s21-logo"><span class="lc">c</span><span class="le">e</span></div>'
             '<div class="brand" id="s21-brand">CLEES &amp; ERNSTER</div>'
             '<div class="claim" id="s21-claim">' + words("Erst die") + ' <span class="ul">' + words("Strategie.") +
             '<span class="line" id="s21-line"></span></span> ' + words("Dann das Bild.") + '</div>'
             '<div class="btn" id="s21-btn"><span class="shim"></span>Kostenloses Strategiegespräch <span class="arr">→</span></div></div>')


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
.wipe2{position:absolute;inset:0;z-index:6;background:var(--navy);opacity:0}
.wipe{position:absolute;inset:0;z-index:7;background:var(--acc);opacity:0}
.shock{position:absolute;left:50%;top:50%;width:300px;height:300px;margin:-150px;border-radius:50%;border:6px solid var(--acc);opacity:0;z-index:1}
.ch{display:inline-block}
.odo{display:inline-block;height:.9em;overflow:hidden;vertical-align:top}
.reel{display:flex;flex-direction:column}
.reel span{display:block;height:.9em;line-height:.9em}
.num-acc .dash{color:var(--ink)}
.rail{position:absolute;z-index:3;left:50%;top:var(--railt);transform:translateX(-50%);display:flex;align-items:center;gap:14px;white-space:nowrap}
.rn{padding:12px 24px;border-radius:999px;border:2px solid rgba(77,141,255,.35);font-weight:700;font-size:var(--chip);color:var(--muted);background:rgba(6,8,13,.6)}
.rn.on{background:rgba(77,141,255,.18);color:var(--ink);border-color:var(--acc)}
.rl{display:block;width:var(--rlw);height:4px;background:rgba(77,141,255,.2);border-radius:4px;overflow:hidden}
.rl b{display:block;height:100%;width:100%;background:var(--acc);transform-origin:left;transform:scaleX(0)}
.hlw{position:relative;display:inline-block;isolation:isolate}
.hlb{position:absolute;left:-.1em;right:-.1em;top:.04em;bottom:-.04em;background:var(--acc);transform-origin:left;transform:scaleX(0);z-index:-1;border-radius:.06em}
.btn{position:relative;overflow:hidden}
.shim{position:absolute;top:0;bottom:0;width:30%;left:-40%;background:linear-gradient(100deg,transparent,rgba(255,255,255,.5),transparent);transform:skewX(-20deg)}
.logo span{display:inline-block}
.flash{position:absolute;inset:0;z-index:8;background:#dfe9ff;opacity:0}
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
:root{--railt:96px;--rlw:70px;--brand:100px;--mega:250px;--h1:170px;--h1d:132px;--h1s:132px;--big:150px;--xl:150px;--h2:84px;--kick:32px;--body:40px;--bodyw:900px;--gap:110px;--adw:720px;
  --icsm:34px;--hrt:150px;--bub:42px;--phone:420px;--iconbox:320px;--mbtn:40px;--chip:30px;--chainb:90px;--notew:560px;--noteb:30px;--notes:28px;
  --calw:560px;--logo:200px;--claim:64px;--btn:44px}
.scene-content{padding:110px 150px}
"""

CSS_916 = r"""
:root{--railt:262px;--rlw:24px;--brand:76px;--mega:200px;--h1:118px;--h1d:104px;--h1s:96px;--big:84px;--xl:100px;--h2:72px;--kick:28px;--body:38px;--bodyw:820px;--gap:60px;--adw:760px;
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

JS = open(os.path.join(HERE, "js_v2.js"), encoding="utf-8").read()



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
        vis = ' style="opacity:0;"' if sid in ("s10", "s11") else ('' if i == 0 else ' style="visibility:hidden;"')
        scenes.append(
            '\n<!-- %s (%.2f–%.2fs) | VO: "%s" -->\n'
            '<div class="scene clip" id="%s" data-start="%s" data-duration="%s" data-track-index="0"%s>\n'
            '%s\n<div class="shock"></div>\n<div class="scene-content">%s</div>\n<div class="wipe2"></div><div class="wipe"></div><div class="flash"></div>\n</div>'
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
<script src="https://cdn.jsdelivr.net/npm/@hyperframes/shader-transitions/dist/index.global.js"></script>
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
