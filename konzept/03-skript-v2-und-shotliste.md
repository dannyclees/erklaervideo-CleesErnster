# Erklärvideo Clees & Ernster – Skript v2 (Aufnahme) & Shotliste v1

**Änderungen zu v1:** Analyse ist **kostenlos** · Kundenbeispiel als **Handwerksbetrieb** · **keine Website** im Video · Stil: **Trailer**, schnelle Schnitte (21 Shots in 40 s, im Hook alle 0,6–1,3 s).

## Skript zum Einsprechen (Danny)

> Ruhig, aber mit Druck sprechen, ca. 2,5 Wörter/s. `/` = kurze Pause, `//` = längere Pause.
> Trocken aufnehmen (ohne Musik/Hall), WAV oder MP3. Ich schneide die Animation danach exakt auf Deine Satzanfänge.

1. Ein schönes Video bringt Dir noch keinen einzigen Kunden. //
2. Likes, / Klicks, / Komplimente – / aber das Telefon bleibt still. //
3. Weil Menschen nicht kaufen, was sie sehen. / Sondern was sie fühlen. //
4. Darum starten wir mit Verkaufspsychologie: / Wer ist Dein Wunschkunde? / Was treibt ihn an? / Was bringt ihn zum Handeln? //
5. Ein Handwerksbetrieb bekommt zwei bis fünf Anfragen am Tag. / Andere wollen drei, vier im Monat – / oder in ihrer Region bekannter werden. / Die Strategie richtet sich nach Deinem Ziel. //
6. Lass Dein Marketing kostenlos von uns analysieren – / Du gehst in jedem Fall mit konkreten Ideen raus. / Clees & Ernster.

## Shotliste v2 (Timing = Schätzung, wird auf die Aufnahme angepasst)

| Shot | Zeit | VO | Bild | Sound-Hit |
|---|---|---|---|---|
| s01 | 0,0 | „Ein schönes Video …“ | Hochglanz-Anzeige + **SCHÖNES VIDEO.** (Frame 1 steht) | – |
| s02 | 1,3 | „… bringt Dir noch …“ | **= KUNDEN?** | Swish |
| s03 | 2,3 | „… keinen einzigen Kunden.“ | Anzeige friert ein (grau, Pause), „=“ wird rot zu **≠** durchgestrichen, Flash + Shake | Scratch / Hit |
| s04 | 3,6 | „Likes,“ | **LIKES,** + Herzen explodieren | Pop |
| s05 | 4,3 | „Klicks,“ | **KLICKS,** + Cursor klicken | Klicks |
| s06 | 4,95 | „Komplimente –“ | **KOMPLIMENTE –** + Kommentar-Blasen | Pops |
| s07 | 5,6 | „aber das Telefon bleibt still.“ | Stille: Telefon, Nulllinie, **Anfragen 0** | Musik weg, Stille |
| s08 | 7,2 | „Weil Menschen nicht kaufen,“ | **MENSCHEN KAUFEN NICHT,** | Whoosh (Wipe) |
| s09 | 8,5 | „was sie sehen.“ | Auge + **WAS SIE SEHEN.** wird rot durchgestrichen | Scratch |
| s10 | 10,0 | „Sondern was sie fühlen.“ | Zoom durch einen Tunnel, Herzschlag-Linie, **FÜHLEN.** blau unterstrichen | Whoosh + Herzschlag |
| s11 | 11,8 | „Darum starten wir mit Verkaufspsychologie:“ | Flash, **VERKAUFS-PSYCHOLOGIE.** auf Bauplan-Raster | Impact |
| s12 | 14,0 | „Wer ist Dein Wunschkunde?“ | 01 Zielkreis + Person, **WUNSCHKUNDE** | Klick |
| s13 | 15,6 | „Was treibt ihn an?“ | 02 vier Farbpunkte kreisen (die Farbtypen), **ANTRIEB** | Klick |
| s14 | 17,2 | „Was bringt ihn zum Handeln?“ | 03 Cursor klickt „Anfrage senden“ (wird grün), **HANDLUNG** | Klick + Ding |
| s15 | 19,0 | „Ein Handwerksbetrieb bekommt zwei bis fünf Anfragen am Tag.“ | Kundenbeispiel · Handwerksbetrieb, **2–5 ANFRAGEN PRO TAG**, Benachrichtigungen stapeln sich | Impact + Ding-Ding-Ding |
| s16 | 23,0 | „Andere wollen drei, vier im Monat –“ | **3–4 ANFRAGEN PRO MONAT**, Kalender mit 4 Treffern | Tick |
| s17 | 25,5 | „oder in ihrer Region bekannter werden.“ | **BEKANNTER IN DER REGION.**, Pin mit Wellen, Punkte leuchten auf | Sonar |
| s18 | 28,0 | „Die Strategie richtet sich nach Deinem Ziel.“ | Chips der 3 Ziele, **DEIN ZIEL. → DEINE STRATEGIE.** | Hit |
| s19 | 31,0 | „Lass Dein Marketing kostenlos von uns analysieren –“ | **Dieselbe Anzeige** wie am Anfang, jetzt mit Anfragen · **KOSTENLOSE MARKETING-ANALYSE.** | Ding-Ding |
| s20 | 33,9 | „Du gehst in jedem Fall mit konkreten Ideen raus.“ | **KONKRETE IDEEN.** + Funken | Sparkle |
| s21 | 37,0 | „Clees & Ernster.“ | Logo, **Erst die Strategie. Dann das Bild.**, Button **Kostenloses Strategiegespräch** | Final Hit |

## Dateien

- `videos/ce-erklaervideo/CE_Erklaervideo_Strategie_16x9_40s_v2.mp4` – Website
- `videos/ce-erklaervideo/CE_Erklaervideo_Strategie_9x16_40s_v2.mp4` – Social-Profile (mit eingebrannten Untertiteln)
- `videos/ce-erklaervideo/src/build.py` – Quelle für beide Formate (Timing in `SHOTS`/`SUBS`)

## Platzhalter (noch offen)

- Logo „ce“ ist nachgebaut → echte Logo-Datei (SVG) einsetzen
- Farben `#06080d` / `#0b1f45` / `#4d8dff` → echte Hex-Werte
- Benachrichtigungen („Neue Anfrage · 08:12“ usw.) sind Illustration, keine echten Daten

## Motion-Upgrade v2 („noch geiler“)

| Was | Wo | Warum |
|---|---|---|
| **Tempo 0.8** (alle Bewegungen ~20 % schneller) | überall | Trailer-Energie |
| **3D-Kamerafahrt** der Anzeige, dreht über drei Schnitte weiter und „friert“ beim ≠ mit einem Ruck ein | s01–s03, Rückkehr in s19 | Motion Match: Schnitte werden unsichtbar, die Anzeige ist die Hauptfigur |
| **Shader-Zoom** (cinematic-zoom), einmal | s10 → s11 | der größte Energiesprung: von „fühlen“ in die Verkaufspsychologie |
| **Buchstaben einzeln** schlagen ein (mit Rotation/Pop) | SCHÖNES VIDEO, LIKES, KLICKS, PSYCHOLOGIE, STRATEGIE, IDEEN | Hero-Wörter bekommen Gewicht |
| **Schockwellen-Ring** beim Aufprall | ≠, Likes, Menschen, Psychologie, Handlung, 2–5, Strategie, Ideen, Logo | macht den Treffer sichtbar, Ankerpunkt für Sound-Hits |
| **RGB-Split** (4 Frames) | ≠ KUNDEN, SEHEN, PSYCHOLOGIE, STRATEGIE | Glitch-Akzent auf den Wendepunkten |
| **Smear-Frames** (kurz gestreckt + Snap) | Wort-Auftritte | ersetzt Motion Blur |
| **Doppel-Wipe** (Akzent + Navy) | Szenenwechsel s04, s08, s12, s16, s19 | Trailer-Schnitte |
| **Zählwerk** 2–5: Ziffernrollen drehen und rasten ein | s15 | macht die echte Zahl zum Moment |
| **Fortschrittsschiene** 01 → 02 → 03 läuft über die Schnitte weiter | s12–s14 | Struktur für Blau-Typen, Kontinuität |
| **Highlight-Balken** hinter KOSTENLOSE | s19 | das Angebot sticht heraus (Von-Restorff) |
| **Logo-Lock** (c und e fahren zusammen, Ring, Shake) + Shimmer über den Button | s21 | letzter Frame = Peak |
