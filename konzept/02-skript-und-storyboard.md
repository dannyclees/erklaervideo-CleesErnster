# Erklärvideo Clees & Ernster – Phase 2: Skript v1 & Storyboard

**Bereich:** Komplett animiertes Erklärvideo, eigene Marke C&E
**Formate:** 16:9 Master (Website, 1920×1080) + 9:16-Fassung (Social-Profile, 1080×1920)
**Länge:** ca. 37–39 s
**Ton:** Danny spricht das Voiceover selbst ein. Das Video wird auf seine Aufnahme getimt.
**Ansprache:** Du-Form (C&E-Markenregel), Du/Dein/Dir großgeschrieben
**Ziel-Aktion:** unverbindliche Marketing-Analyse im Strategiegespräch

---

## Skript v1 (zum Einsprechen)

> Tempo: ruhig, aber bestimmt (etwa 2,5 Wörter/s). `/` = kurze Pause, `//` = längere Pause.

1. **Ein schönes Video bringt Dir noch keinen einzigen Kunden.** //
2. **Likes, Klicks, Komplimente – / aber das Telefon bleibt still.** //
3. **Weil Menschen nicht kaufen, was sie sehen. / Sondern was sie fühlen.** //
4. **Darum starten wir mit Verkaufspsychologie: / Wer ist Dein Wunschkunde? / Was treibt ihn an? / Was bringt ihn zum Handeln?** //
5. **Ein Kunde von uns bekommt zwei bis fünf Anfragen am Tag. / Andere wollen drei, vier im Monat – / oder in ihrer Region bekannter werden. / Die Strategie richtet sich nach Deinem Ziel.** //
6. **Lass Dein Marketing unverbindlich von uns analysieren – / Du gehst in jedem Fall mit konkreten Ideen raus. / Clees & Ernster.**

≈ 92 Wörter → ca. 37–39 s inkl. Pausen.

**Warum diese Reihenfolge (Farbtypen):**
- 🔴 Satz 1 = Pattern-Break, greift den Mythos an („gemeinsamer Feind“)
- 🟢 Satz 2 = Weg-von, Wiedererkennung („genau so geht’s mir“)
- 🔵 Satz 3–4 = das „Weil“ + Methode als Beweis (Struktur statt Versprechen)
- 🟡/🔴 Satz 5 = echtes Ergebnis + Hin-zu, gleichzeitig Einwand „bin ich zu klein dafür?“ entkräftet
- 🟢 Satz 6 = Risiko raus (unverbindlich, Mehrwert garantiert), Identität über den Namen

---

## Visuelle Leitidee: „Die Anzeige“ als Hauptfigur

Ein einziges Objekt trägt den ganzen Film: **eine hochglänzende Anzeigen-Karte** (stilisiertes Video/Post).
- Am Anfang ist sie schön, aber leer: Nichts passiert.
- Dann **tauchen wir hinter die Karte**. Dort liegt die Strategie als Bauplan aus Linien und Knoten.
- Der Bauplan steckt sich zurück in die Karte. **Dieselbe Anzeige** bringt jetzt Anfragen.

So steckt Idee B (gleiches Video, anderes Ergebnis) als Vorher/Nachher in der Zeit, statt als Split-Screen. Und die Kernaussage *„Es geht nicht um das Bild, sondern um das, was dahinter steckt“* wird wörtlich gezeigt.

## Bewegungscharakter

Schnell und direkt (C&E-Rot), aber präzise und aufgeräumt für Website-Besucher (Blau): harte Schnitte, kurze Auftritte, ruhiges Stehen beim Lesen, keine Effektshow.
**Signatur:** Die hellblaue Akzentlinie schnappt mit `expo.out` unter das Schlüsselwort jeder Szene (Wiedererkennung über alle C&E-Videos).

```js
var M = {
  tempo: 0.85,
  dur:  { xs: 0.12, s: 0.25, m: 0.45, l: 0.8 },
  ease: { enter: "power4.out", exit: "power3.in", accent: "expo.out", hold: "sine.inOut", pop: "back.out(1.2)" },
  stagger: 0.05
};
```

**Look:** Schwarz `#06080d` / Dunkelblau `#0b1f45` / Akzent-Hellblau `#4d8dff` *(Platzhalter, bis die echten Hex-Werte da sind)*. Fette Grotesk mit engem Tracking, ein durchgängiges Linien-Icon-System (gleicher Strich, runde Enden), feines Raster im Hintergrund als „Bauplan“-Ebene.

---

## Beat-Sheet / Storyboard

Zeiten = Schätzung nach Skript. Werden nach Dannys Aufnahme exakt auf die Satzanfänge gesetzt.

| # | Zeit | VO | Text im Bild | Hero-Moment (und warum) | Sound | Übergang |
|---|---|---|---|---|---|---|
| 1 | 0,0–3,6 | „Ein schönes Video bringt Dir noch keinen einzigen Kunden.“ | **Schön ≠ Kunden** | Frame 1 steht: glänzende Anzeigen-Karte mit Play-Button, leichter Glanz-Sweep. Auf „keinen einzigen“ friert die Karte ein (Pause-Icon), das „=“ zwischen *Schön* und *Kunden* wird **durchgestrichen → ≠**. *Warum:* Der Mythos wird in einer Bewegung zerlegt. | Tick beim Einfrieren, Scratch beim Durchstreichen | harter Schnitt |
| 2 | 3,6–7,2 | „Likes, Klicks, Komplimente – aber das Telefon bleibt still.“ | **Anfragen: 0** | Um die Karte poppen Likes, Herzen und Klick-Cursor auf und steigen nach oben (viel Bewegung). Darunter steht ein Zähler **„Anfragen 0“** völlig still, das Telefon-Icon zeigt eine flache Linie. *Warum:* Der Kontrast „viel Lärm, null Ergebnis“ ist das Problem, ohne ein Wort zu lesen. | Pop-Pop-Pop, dann abrupte Stille | Kamera-Push in die Karte |
| 3 | 7,2–11,8 | „Weil Menschen nicht kaufen, was sie sehen. Sondern was sie fühlen.“ | **sehen → fühlen** | Kamera fährt **durch** die Karte hindurch (Motion Match): Die Oberfläche wird transparent, dahinter erscheint das dunkle Bauplan-Raster. Auge-Icon morpht in Herz/Impuls-Icon, Akzentlinie unter *fühlen*. *Warum:* Wir verlassen die Oberfläche und gehen dahin, wo gekauft wird. | Whoosh beim Durchfahren | Kontinuität (gleicher Raum) |
| 4 | 11,8–19,0 | „Darum starten wir mit Verkaufspsychologie: Wer ist Dein Wunschkunde? Was treibt ihn an? Was bringt ihn zum Handeln?“ | Kicker **Die Strategie** · **Wunschkunde → Antrieb → Handlung** | Drei Knoten zeichnen sich per Stroke-Draw genau auf das jeweilige Wort: Person-Icon, vier Farbpunkte (rot/gelb/grün/blau = Kaufmotive), Pfeil/Klick. Eine Linie verbindet sie zum Bauplan. *Warum:* Methode statt Versprechen ist der Beweis für Blau-Typen. | Kurzer Klick pro Knoten | Bauplan zoomt heraus |
| 5 | 19,0–30,5 | „Ein Kunde von uns bekommt zwei bis fünf Anfragen am Tag. Andere wollen drei, vier im Monat – oder in ihrer Region bekannter werden. Die Strategie richtet sich nach Deinem Ziel.“ | **2–5 Anfragen / Tag** (Label „Kundenbeispiel“) · **3–4 Anfragen / Monat** · **Bekannter in der Region** · Schluss: **Dein Ziel → Deine Strategie** | Ein Ziel-Regler (3 Rasterstufen) springt nacheinander auf die drei Ziele. Bei jedem Sprung **ordnet sich der Bauplan neu** (gleiche Knoten, andere Verbindung): Zahl zählt hoch bzw. Luxemburg-Umriss mit pulsierendem Pin. *Warum:* zeigt „jede Größe geht“ und dass die Strategie maßgeschneidert ist, ohne das Wort zu benutzen. | Rastklick pro Sprung, Count-up-Tick | Bauplan fliegt zurück in die Karte |
| 6a | 30,5–33,5 | „Lass Dein Marketing unverbindlich von uns analysieren –“ | **Dein Marketing. Analysiert.** | Der Bauplan schiebt sich in die Anzeigen-Karte zurück, **dieselbe Karte** wie in Szene 1. Jetzt vibriert das Telefon-Icon, Anfragen-Benachrichtigungen stapeln sich weich ein. *Warum:* Payoff von Szene 1 und 2, gleiche Anzeige, anderes Ergebnis. | Vibration, sanftes „Ding“ | Karte rückt zur Seite |
| 6b | 33,5–38,5 | „– Du gehst in jedem Fall mit konkreten Ideen raus. Clees & Ernster.“ | Logo **ce** · **Erst die Strategie. Dann das Bild.** · Button **Strategiegespräch vereinbaren** · *unverbindlich* | Logo setzt sich, Claim baut sich wortweise auf, Akzentlinie schnappt unter *Strategie*, Button erscheint mit leichtem Pulsieren. Letzter Frame = Peak (alles steht, Button leuchtet), keine Ausblende. | Akzent-Hit auf Logo, Klick auf Button | Ende |

---

## 9:16-Fassung (Social-Profile)

- Gleiche Szenen und gleiches Timing, **Layout neu gesetzt** (nicht nur beschnitten): Karte oben, Text darunter gestapelt.
- Safe Zone: Text und Button nicht in den oberen 250 px, unteren 620 px, links 90 px, rechts 140 px.
- **Untertitel eingebrannt** (max. 2 Zeilen, unten in der Safe Zone), weil im Feed meist ohne Ton geschaut wird.
- Bei Szene 4 stehen die drei Knoten untereinander statt nebeneinander.

---

## Produktionsablauf

1. ✅ Konzept und Skript v1 → **Freigabe durch Danny**
2. Danny nimmt das Voiceover auf (WAV/MP3, Raumklang trocken, ohne Musik)
3. Styleframes (Szene 1, 4, 6b) in 3 Richtungen: sicher / mittel / mutig
4. Animatic auf die echte Aufnahme getimt (einfache Bewegung, Timing fix)
5. Finale Animation + Polish, Render 16:9 + 9:16
6. Optional: Musik und Sounddesign (Hits laut Spalte „Sound“), selbst im Schnitt oder per HyperFrames/HeyGen

## Offene Punkte

- [ ] **Logo-Datei** (SVG/PNG) und **Hex-Werte** der C&E-Farben, bis dahin Platzhalter
- [ ] **Website/Domain** für den CTA-Screen
- [ ] **Kundenbeispiel „2–5 Anfragen/Tag“**: anonym als „Kundenbeispiel“ zeigen oder mit Branche (z. B. „Handwerksbetrieb, Luxemburg“)? Freigabe des Kunden nötig, falls genannt
- [ ] Ist die Analyse **kostenlos**? Dann darf „kostenlos“ in den Button, das wirkt stärker als „unverbindlich“
- [ ] **Musik/Sounddesign:** legst Du selbst Musik drunter, oder soll das Video vorab Sound-Hits mitbekommen?
