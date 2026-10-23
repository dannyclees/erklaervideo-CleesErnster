window.__timelines = window.__timelines || {};
var tl = gsap.timeline({ paused: true });
var T = __T__, END = __END__, V = __VERT__, TOTAL = __TOTAL__;
// C&E-Bewegungssystem, v2: Tempo 0.8 = Trailer-Energie
var M = {
  tempo: 0.8,
  dur:  { xs: 0.12, s: 0.25, m: 0.45, l: 0.8 },
  ease: { enter: "power4.out", exit: "power3.in", accent: "expo.out", hold: "sine.inOut", pop: "back.out(1.2)" },
  stagger: 0.05
};
var ACC = "#4d8dff", RED = "#ff5a5f", INK = "#f2f5fa";
function d(k) { return M.dur[k] * M.tempo; }
function q(s) { return document.querySelector(s); }

// Szenen-Sichtbarkeit (harte Schnitte). s10/s11 sind Shader-Anker → keine Toggles
var ANCHORS = ["s10", "s11"];
Object.keys(T).forEach(function (id) {
  if (ANCHORS.indexOf(id) >= 0) return;
  if (id !== "s01") tl.set("#" + id, { autoAlpha: 1 }, T[id]);
  if (END[id] < TOTAL) tl.set("#" + id, { autoAlpha: 0 }, END[id]);
});
tl.set("#s10", { opacity: 1 }, T.s10);

// ── Bausteine ──
function slam(sel, t, st, dir) { tl.from(sel, { yPercent: dir || 115, duration: d("m"), ease: M.ease.enter, stagger: st || M.stagger }, t); }
function pop(sel, t, st) { tl.from(sel, { yPercent: 120, scale: 1.5, duration: 0.36, ease: M.ease.accent, stagger: st || 0.03 }, t); }
function punch(sel, t, from) { tl.fromTo(sel, { scale: from || 1.5, autoAlpha: 0 }, { scale: 1, autoAlpha: 1, duration: d("s") + 0.05, ease: M.ease.accent }, t); }
function kick(sel, t) { tl.from(sel, { x: -40, autoAlpha: 0, duration: d("m"), ease: M.ease.accent }, t); }
function line(sel, t) { tl.to(sel, { scaleX: 1, duration: d("m"), ease: M.ease.accent }, t); }
function push(id, s) { tl.fromTo("#" + id + " .scene-content", { scale: 1 }, { scale: s || 1.04, duration: END[id] - T[id], ease: "none" }, T[id]); }
// Doppel-Wipe: Akzent-Panel räumt zuerst, Navy-Panel folgt 2 Frames später
function wipe(id, dir) {
  var a = "#" + id + " .wipe", b = "#" + id + " .wipe2", x = dir < 0 ? -101 : 101;
  tl.set([a, b], { xPercent: 0, opacity: 1 }, T[id]);
  tl.to(a, { xPercent: x, duration: 0.18, ease: "power3.in" }, T[id]);
  tl.to(b, { xPercent: x, duration: 0.2, ease: "power3.in" }, T[id] + 0.05);
}
function flash(id, t) { var f = "#" + id + " .flash"; tl.set(f, { opacity: 0.75 }, t); tl.to(f, { opacity: 0, duration: 0.3, ease: "power2.out" }, t); }
function shake(id, t, a) {
  var c = "#" + id + " .scene-content", k = a || 1;
  [[-14, 8], [12, -6], [-8, 5], [5, -3], [0, 0]].forEach(function (p, i) {
    tl.to(c, { x: p[0] * k, y: p[1] * k, duration: 0.035, ease: "none" }, t + i * 0.035);
  });
}
// Schockwelle: Ring schießt aus der Bildmitte – macht den Aufprall sichtbar
function shock(id, t, c) { var s = "#" + id + " .shock"; tl.set(s, { scale: 0.15, opacity: 0.9, borderColor: c || ACC }, t); tl.to(s, { scale: 7, opacity: 0, duration: 0.6, ease: "expo.out" }, t); }
// Smear-Frames: kurz gestreckt + geschert, dann Snap – ersetzt Motion Blur
function smear(sel, t, dir) { var k = dir || 1; tl.set(sel, { scaleX: 1.3, skewX: -14 * k }, t); tl.to(sel, { scaleX: 1, skewX: 0, duration: 0.14, ease: "power3.out" }, t); }
// RGB-Split für 4 Frames auf Hero-Typo (nie auf Lesetext im Hold)
function rgb(sel, t) {
  tl.set(sel, { textShadow: "9px 0 rgba(255,60,90,.85), -9px 0 rgba(60,170,255,.85)" }, t);
  tl.set(sel, { textShadow: "-5px 0 rgba(255,60,90,.7), 5px 0 rgba(60,170,255,.7)" }, t + 0.067);
  tl.set(sel, { textShadow: "0px 0px rgba(0,0,0,0)" }, t + 0.134);
}
function ghost(id, dx) { tl.fromTo("#" + id + " .ghost", { x: 0 }, { x: dx, duration: END[id] - T[id], ease: "none" }, T[id]); }
function shine(card, t) { tl.fromTo(card + " .ad-shine", { xPercent: 0 }, { xPercent: 570, duration: 0.9, ease: "power2.inOut" }, t); }
function tap(sel, t, s) { tl.set(sel, { scale: s || 1.05 }, t); tl.to(sel, { scale: 1, duration: 0.12, ease: "power2.out" }, t); }

// ── S01–S03 Hook: Schön ≠ Kunden. Die Karte dreht sich über alle drei Schnitte weiter (Motion Match) ──
(function () {
  var t = T.s01;
  tl.fromTo("#s01-ad", { rotationY: 26, rotationX: 6, z: -160, transformPerspective: 1400 },
    { rotationY: 10, rotationX: 2, z: 0, duration: END.s01 - t, ease: "power2.out" }, t);
  shine("#s01-ad", t + 0.1);
  tl.fromTo("#s01-ad .ad-play", { scale: 1 }, { scale: 1.08, duration: 0.5, yoyo: true, repeat: 1, ease: M.ease.hold }, t);
  tl.fromTo("#s01-ad .ad-prog", { scaleX: 0.08 }, { scaleX: 0.3, duration: END.s01 - t, ease: "none" }, t);
  tl.to("#s01-h .ch", { color: ACC, duration: 0.1, stagger: 0.03, yoyo: true, repeat: 1 }, t + 0.2);
  tl.fromTo("#s01-h", { scale: 1.06 }, { scale: 1, duration: END.s01 - t, ease: "power2.out" }, t);

  t = T.s02;
  tl.fromTo("#s02-ad", { rotationY: 10, rotationX: 2, transformPerspective: 1400 }, { rotationY: 4, rotationX: 0, duration: END.s02 - t, ease: "none" }, t);
  tl.fromTo("#s02-ad .ad-prog", { scaleX: 0.3 }, { scaleX: 0.55, duration: END.s02 - t, ease: "none" }, t);
  kick("#s02-k", t + 0.02);
  slam("#s02-h .w", t + 0.05, 0.05);
  smear("#s02-h .m", t + 0.05);
  shine("#s02-ad", t + 0.25);
  push("s02", 1.03);

  t = T.s03;
  tl.set("#s03-ad", { rotationY: 4, transformPerspective: 1400 }, t);
  tl.set("#s03-ad .ad-prog", { scaleX: 0.55 }, t);
  tl.to("#s03-ad", { rotationY: 0, scale: 0.93, duration: 0.3, ease: M.ease.accent }, t + 0.35);
  tl.to("#s03-ad .ad-play", { autoAlpha: 0, duration: 0.05 }, t + 0.35);
  tl.to("#s03-ad .ad-pause", { opacity: 1, duration: 0.05 }, t + 0.35);
  tl.to("#s03-ad .ad-media", { filter: "grayscale(1) brightness(.55)", duration: 0.2, ease: "power2.out" }, t + 0.35);
  tl.fromTo("#s03-strike", { scaleX: 0, rotation: -58 }, { scaleX: 1, rotation: -58, duration: d("s"), ease: M.ease.accent }, t + 0.4);
  flash("s03", t + 0.4);
  rgb("#s03-h", t + 0.4);
  shock("s03", t + 0.4, RED);
  shake("s03", t + 0.42, 1.3);
})();

// ── S04–S06 Lärm: jedes Wort ein Aufprall, Richtung wechselt ──
(function () {
  var t = T.s04, H = [[-560, -260], [520, -220], [-380, 260], [430, 280], [-720, 30], [700, 40], [-150, -330], [180, 330], [-250, -120], [270, 120]];
  if (V) H = H.map(function (p) { return [p[0] * 0.55, p[1] * 1.5]; });
  wipe("s04", 1);
  tl.from("#s04-h .ch", { yPercent: 120, rotation: function (i) { return [-14, 9, -7, 11, -9, 6][i % 6]; }, duration: 0.3, ease: M.ease.accent, stagger: 0.03 }, t + 0.06);
  tl.fromTo("#s04-h", { scale: 1.25 }, { scale: 1, duration: END.s04 - t, ease: "power2.out" }, t);
  shock("s04", t + 0.12, RED);
  H.forEach(function (p, i) {
    tl.fromTo("#s04 .h" + i, { x: 0, y: 0, scale: 0.2, rotation: 0, autoAlpha: 1 },
      { x: p[0], y: p[1] - 60, scale: 0.5 + (i % 3) * 0.25, rotation: (i % 2 ? 14 : -14), duration: 0.55, ease: "expo.out" }, t + 0.1 + i * 0.025);
  });
  shake("s04", t + 0.12, 0.8);

  t = T.s05;
  tl.from("#s05-h .ch", { yPercent: -120, duration: 0.28, ease: M.ease.accent, stagger: 0.025 }, t + 0.02);
  smear("#s05-h .m", t + 0.02, -1);
  var C = [[-560, -200], [540, -160], [-420, 230], [460, 250]];
  if (V) C = [[-280, -440], [280, -360], [-260, 380], [270, 440]];
  C.forEach(function (p, i) {
    var el = "#s05 .c" + i, tt = t + 0.04 + i * 0.09;
    tl.fromTo(el, { x: p[0] * 1.4, y: p[1] * 1.4, autoAlpha: 0 }, { x: p[0], y: p[1], autoAlpha: 1, duration: 0.2, ease: "power3.out" }, tt);
    tl.to(el + " .ic", { scale: 0.82, duration: 0.06, yoyo: true, repeat: 1 }, tt + 0.2);
    tl.set(el + " .ring", { scale: 0.2, opacity: 1 }, tt + 0.22);
    tl.to(el + " .ring", { scale: 2.2, opacity: 0, duration: 0.35, ease: "power2.out" }, tt + 0.22);
    if (i > 0) tap("#s05-h", tt + 0.22, 1.04);
  });

  t = T.s06;
  var B = [[-560, -230], [480, -250], [-500, 240], [520, 220]];
  if (V) B = [[-140, -430], [150, -320], [-120, 360], [120, 460]];
  B.forEach(function (p, i) {
    tl.fromTo("#s06 .b" + i, { x: p[0], y: p[1] + 30, scale: 0.4, autoAlpha: 0 }, { x: p[0], y: p[1] - 12, scale: 1, autoAlpha: 1, duration: 0.3, ease: M.ease.pop }, t + 0.04 + i * 0.07);
  });
  slam("#s06-h .w", t + 0.02, 0.04);
  smear("#s06-h .m", t + 0.02);
  push("s06", 1.06);
})();

// ── S07 Stille: alles steht, nur die Nulllinie läuft – Kontrast zum Lärm davor ──
(function () {
  var t = T.s07;
  tl.fromTo("#s07-flat", { strokeDasharray: 600, strokeDashoffset: 600 }, { strokeDashoffset: 0, duration: 1.3, ease: "none" }, t + 0.1);
  kick("#s07-k", t + 0.15);
  tl.fromTo("#s07-n", { yPercent: -40, autoAlpha: 0 }, { yPercent: 0, autoAlpha: 1, duration: 0.4, ease: "bounce.out" }, t + 0.25);
  tl.from("#s07-b", { y: 20, autoAlpha: 0, duration: 0.4, ease: "power2.out" }, t + 0.55);
  push("s07", 1.07);
})();

// ── S08–S10 Das Weil: sehen → fühlen ──
(function () {
  var t = T.s08;
  wipe("s08", -1);
  tl.from("#s08-h .w", { yPercent: function (i) { return i === 0 ? -115 : 115; }, duration: d("m"), ease: M.ease.enter, stagger: 0.07 }, t + 0.06);
  shock("s08", t + 0.3);
  ghost("s08", -700);
  push("s08", 1.05);

  t = T.s09;
  tl.to("#s09 .eye .dr", { strokeDashoffset: 0, duration: 0.5, ease: "power2.out", stagger: 0.1 }, t + 0.05);
  tl.to("#s09 .eye", { scaleY: 0.08, duration: 0.07, yoyo: true, repeat: 1, ease: "power2.in", transformOrigin: "50% 50%" }, t + 0.65);
  slam("#s09-h .w", t + 0.08);
  tl.to("#s09-strike", { scaleX: 1, duration: d("s"), ease: M.ease.accent }, t + 1.0);
  rgb("#s09-h", t + 1.0);
  tl.to("#s09-h .w", { color: "rgba(242,245,250,.4)", duration: 0.2 }, t + 1.05);
  tl.to("#s09 .eye", { color: "rgba(242,245,250,.35)", duration: 0.2 }, t + 1.05);
  shake("s09", t + 1.02, 0.7);
  push("s09", 1.03);

  t = T.s10;
  for (var i = 0; i < 5; i++) {
    tl.fromTo("#s10 .t" + i, { scale: 0.2 + i * 0.5, autoAlpha: 0.9 }, { scale: 4 + i * 1.2, autoAlpha: 0, duration: 1.2, ease: "power2.out" }, t + i * 0.05);
  }
  tl.fromTo("#s10 .scene-content", { scale: 1.6 }, { scale: 1, duration: 0.5, ease: M.ease.accent }, t);
  tl.to("#s10-ecg", { strokeDashoffset: 0, duration: 1.1, ease: "power1.inOut" }, t + 0.1);
  kick("#s10-k", t + 0.15);
  slam("#s10-h .w", t + 0.2);
  line("#s10-line", t + 0.95);
  tl.to("#s10 .ul .w", { color: ACC, duration: 0.2 }, t + 0.95);
  tl.to("#s10-h", { scale: 1.06, duration: 0.6, ease: "power2.in" }, t + 1.15);
})();

// ── S11 Verkaufspsychologie: kommt über den Shader-Zoom, Buchstaben schlagen einzeln ein ──
(function () {
  var t = T.s11;
  kick("#s11-k", t + 0.1);
  slam("#s11-h > .m .w", t + 0.15, 0.06);
  pop("#s11-h .ul .ch", t + 0.32, 0.028);
  shock("s11", t + 0.6);
  shake("s11", t + 0.62, 0.9);
  rgb("#s11-h .ul", t + 0.62);
  line("#s11-line", t + 1.0);
  ghost("s11", -600);
  tl.fromTo("#s11 .bg", { backgroundPosition: "0px 0px" }, { backgroundPosition: "0px -192px", duration: END.s11 - t, ease: "none" }, t);
  push("s11", 1.05);
})();

// ── S12–S14 Die drei Schritte: Fortschrittsschiene läuft über die Schnitte weiter ──
(function () {
  function railStep(id, k, t) {
    if (k === 1) tl.from("#" + id + "-rail", { y: -30, autoAlpha: 0, duration: 0.35, ease: M.ease.enter }, t + 0.05);
    else tl.to("#" + id + "-rail .anim", { scaleX: 1, duration: 0.4, ease: M.ease.accent }, t + 0.08);
    tl.to("#" + id + "-rail .cur", { backgroundColor: ACC, borderColor: ACC, color: "#fff", duration: 0.15 }, t + 0.35);
    tl.fromTo("#" + id + "-rail .cur", { scale: 1.25 }, { scale: 1, duration: 0.3, ease: M.ease.pop, immediateRender: false }, t + 0.35);
  }
  var t = T.s12;
  wipe("s12", 1);
  railStep("s12", 1, t);
  [".r1", ".r2", ".r3"].forEach(function (r, i) { tl.from("#s12 " + r, { scale: 0, duration: 0.45, ease: M.ease.accent }, t + 0.1 + i * 0.07); });
  tl.to("#s12 .person .dr", { strokeDashoffset: 0, duration: 0.5, ease: "power2.out", stagger: 0.1 }, t + 0.25);
  tl.to("#s12 .r3", { scale: 1.12, duration: 0.25, yoyo: true, repeat: 1, ease: M.ease.hold }, t + 0.8);
  kick("#s12-n", t + 0.1); slam("#s12-h .w", t + 0.12); smear("#s12-h .m", t + 0.12);
  tl.from("#s12-b", { y: 18, autoAlpha: 0, duration: 0.35, ease: "power2.out" }, t + 0.45);
  push("s12", 1.04);

  t = T.s13;
  railStep("s13", 2, t);
  var R = V ? 110 : 150;
  for (var i = 0; i < 4; i++) {
    (function (i, a0) {
      var o = { a: 0 }, el = q("#s13 .d" + i);
      tl.fromTo(o, { a: 0 }, { a: Math.PI * 1.6, duration: END.s13 - t, ease: "power2.out",
        onUpdate: function () { var r = R * Math.min(1, 0.3 + o.a * 1.2); el.style.transform = "translate(" + (Math.cos(a0 + o.a) * r) + "px," + (Math.sin(a0 + o.a) * r) + "px)"; } }, t);
    })(i, i * Math.PI / 2);
  }
  tl.from("#s13 .core", { scale: 0, duration: 0.4, ease: M.ease.pop }, t + 0.05);
  kick("#s13-n", t + 0.05); slam("#s13-h .w", t + 0.1); smear("#s13-h .m", t + 0.1, -1);
  tl.from("#s13-b", { y: 18, autoAlpha: 0, duration: 0.35, ease: "power2.out" }, t + 0.45);
  push("s13", 1.04);

  t = T.s14;
  railStep("s14", 3, t);
  tl.from("#s14-btn", { scale: 0.6, autoAlpha: 0, duration: 0.35, ease: M.ease.pop }, t + 0.05);
  tl.from("#s14-cur", { x: 160, y: 140, duration: 0.45, ease: "power3.out" }, t + 0.2);
  tl.to("#s14-btn", { scale: 0.9, duration: 0.07, yoyo: true, repeat: 1 }, t + 0.66);
  tl.set("#s14-ring", { scale: 0.2, opacity: 1 }, t + 0.68);
  tl.to("#s14-ring", { scale: 2.4, opacity: 0, duration: 0.45, ease: "power2.out" }, t + 0.68);
  tl.to("#s14-btn", { backgroundColor: "#3ddc84", duration: 0.15 }, t + 0.7);
  shock("s14", t + 0.7, "#3ddc84");
  kick("#s14-n", t + 0.05); slam("#s14-h .w", t + 0.1); smear("#s14-h .m", t + 0.1);
  tl.from("#s14-b", { y: 18, autoAlpha: 0, duration: 0.35, ease: "power2.out" }, t + 0.45);
  push("s14", 1.04);
})();

// ── S15–S18 Jede Größe ──
(function () {
  var t = T.s15;
  flash("s15", t);
  kick("#s15-k", t + 0.05);
  tl.from("#s15-n", { scale: 1.4, autoAlpha: 0, duration: 0.35, ease: M.ease.accent }, t + 0.08);
  // Zählwerk: Ziffernrollen drehen eine Extrarunde und rasten ein
  tl.fromTo("#s15-ra", { yPercent: 0 }, { yPercent: -60, duration: 0.9, ease: "power3.out" }, t + 0.1);
  tl.fromTo("#s15-rb", { yPercent: 0 }, { yPercent: -75, duration: 1.15, ease: "power3.out" }, t + 0.15);
  shock("s15", t + 1.2);
  tap("#s15-n", t + 1.2, 1.08);
  slam("#s15-h .w", t + 0.4);
  var n = V ? 3 : 5;
  for (var i = 0; i < n; i++) {
    tl.from("#s15 .n" + i, { x: V ? 0 : 140, y: V ? -40 : 0, scale: 0.85, autoAlpha: 0, duration: 0.3, ease: M.ease.pop }, t + 0.6 + i * 0.5);
    tl.to("#s15 .n" + i + " .ic", { rotation: 18, duration: 0.06, yoyo: true, repeat: 3 }, t + 0.7 + i * 0.5);
  }
  push("s15", 1.03);

  t = T.s16;
  wipe("s16", -1);
  kick("#s16-k", t + 0.08);
  punch("#s16-n", t + 0.1, 1.6);
  smear("#s16-n", t + 0.1);
  slam("#s16-h .w", t + 0.3);
  tl.from("#s16-cal", { y: 80, rotation: 4, autoAlpha: 0, duration: 0.45, ease: M.ease.enter }, t + 0.15);
  [0, 1, 2, 3].forEach(function (i) {
    tl.fromTo("#s16 .h" + i, { "--k": 0 }, { "--k": 1, duration: 0.3, ease: "back.out(2)" }, t + 0.6 + i * 0.32);
    tap("#s16-cal", t + 0.6 + i * 0.32, 1.02);
  });
  push("s16", 1.03);

  t = T.s17;
  kick("#s17-k", t + 0.05);
  slam("#s17-h .w", t + 0.1, 0.06);
  tl.from("#s17 .mpin", { y: -160, autoAlpha: 0, duration: 0.4, ease: "power3.in" }, t + 0.15);
  tl.to("#s17 .mpin", { scaleY: 0.78, scaleX: 1.18, duration: 0.06, yoyo: true, repeat: 1, transformOrigin: "50% 100%" }, t + 0.55);
  [".w1", ".w2", ".w3"].forEach(function (w, i) {
    tl.fromTo("#s17 " + w, { scale: 1, opacity: 0.9 }, { scale: 34, opacity: 0, duration: 1.4, ease: "power1.out" }, t + 0.55 + i * 0.45);
  });
  document.querySelectorAll("#s17 .pt").forEach(function (p) {
    var dd = parseFloat(p.getAttribute("data-d"));
    tl.to(p, { backgroundColor: ACC, scale: 1.35, duration: 0.25, ease: "power2.out" }, t + 0.55 + dd / 330);
  });
  push("s17", 1.03);

  t = T.s18;
  tl.from("#s18 .chip", { x: function (i) { return [-520, 0, 520][i]; }, y: function (i) { return [40, -80, 40][i]; }, autoAlpha: 0, duration: 0.4, ease: M.ease.enter, stagger: 0.06 }, t + 0.05);
  slam("#s18-a .w", t + 0.2);
  slam("#s18-h > .m .w", t + 1.0, 0.07);
  pop("#s18-h .ul .ch", t + 1.12, 0.025);
  rgb("#s18-h .ul", t + 1.45);
  line("#s18-line", t + 1.5);
  tl.to("#s18 .chip", { borderColor: ACC, color: INK, duration: 0.2, stagger: 0.06 }, t + 1.5);
  shock("s18", t + 1.45);
  shake("s18", t + 1.47, 0.6);
  ghost("s18", -500);
  push("s18", 1.04);
})();

// ── S19 Payoff: dieselbe Anzeige fliegt in 3D zurück – jetzt mit Anfragen ──
(function () {
  var t = T.s19;
  wipe("s19", 1);
  tl.fromTo("#s19-ad", { rotationY: -38, rotationX: 10, z: -420, transformPerspective: 1400, autoAlpha: 0 },
    { rotationY: -6, rotationX: 2, z: 0, autoAlpha: 1, duration: 0.6, ease: M.ease.accent }, t + 0.05);
  tl.to("#s19-ad", { rotationY: 0, rotationX: 0, duration: END.s19 - t - 0.65, ease: "none" }, t + 0.65);
  tl.fromTo("#s19-ad .ad-prog", { scaleX: 0.55 }, { scaleX: 1, duration: END.s19 - t, ease: "none" }, t);
  shine("#s19-ad", t + 0.3);
  [0, 1, 2].forEach(function (i) {
    var tt = t + 0.5 + i * 0.4;
    tl.from("#s19 .k" + i, { x: 90, scale: 0.8, autoAlpha: 0, duration: 0.3, ease: M.ease.pop }, tt);
    tl.to("#s19 .k" + i + " .ic", { rotation: 18, duration: 0.06, yoyo: true, repeat: 3 }, tt + 0.1);
    tl.to("#s19-ad", { x: i % 2 ? 6 : -6, duration: 0.05, yoyo: true, repeat: 1 }, tt + 0.05);
  });
  kick("#s19-k", t + 0.12);
  slam("#s19-h .w", t + 0.2, 0.07);
  tl.to("#s19-hlb", { scaleX: 1, duration: 0.4, ease: M.ease.accent }, t + 0.7);
  push("s19", 1.03);
})();

// ── S20 Konkrete Ideen ──
(function () {
  var t = T.s20;
  for (var i = 0; i < 8; i++) {
    tl.set("#s20 .p" + i, { rotation: i * 45 }, t);
    tl.fromTo("#s20 .p" + i, { scaleY: 0, y: 0, opacity: 1 }, { scaleY: 1, y: -(V ? 260 : 320), opacity: 0, duration: 0.7, ease: "power3.out" }, t + 0.75);
  }
  kick("#s20-k", t + 0.05);
  slam("#s20-h > .m .w", t + 0.1, 0.08);
  pop("#s20-h .ul .ch", t + 0.4, 0.035);
  shock("s20", t + 0.75);
  line("#s20-line", t + 0.8);
  tl.to("#s20 .ul .w", { color: ACC, duration: 0.2 }, t + 0.8);
  tl.from("#s20-b", { y: 20, autoAlpha: 0, duration: 0.4, ease: "power2.out" }, t + 1.1);
  push("s20", 1.04);
})();

// ── S21 Ende: Logo rastet ein, letzter Frame = Peak ──
(function () {
  var t = T.s21;
  flash("s21", t);
  tl.from("#s21-logo", { scale: 0, rotation: -20, duration: 0.5, ease: "back.out(1.6)" }, t + 0.05);
  tl.from("#s21-logo .lc", { x: -90, autoAlpha: 0, duration: 0.3, ease: M.ease.enter }, t + 0.15);
  tl.from("#s21-logo .le", { x: 90, autoAlpha: 0, duration: 0.3, ease: M.ease.enter }, t + 0.15);
  shock("s21", t + 0.42);
  shake("s21", t + 0.44, 0.5);
  tl.from("#s21-brand", { scaleX: 1.35, autoAlpha: 0, duration: 0.55, ease: M.ease.accent }, t + 0.3);
  slam("#s21-claim .w", t + 0.6, 0.05);
  line("#s21-line", t + 1.1);
  tl.from("#s21-btn", { y: 40, scale: 0.8, autoAlpha: 0, duration: 0.45, ease: "back.out(1.5)" }, t + 0.8);
  tl.fromTo("#s21-btn .shim", { xPercent: 0 }, { xPercent: 570, duration: 0.7, ease: "power2.inOut" }, t + 1.4);
  tl.fromTo("#s21-btn .shim", { xPercent: 0 }, { xPercent: 570, duration: 0.7, ease: "power2.inOut", immediateRender: false }, t + 2.25);
  tl.to("#s21-btn", { scale: 1.05, duration: 0.35, yoyo: true, repeat: 1, ease: M.ease.hold }, t + 1.7);
  tl.fromTo("#s21-btn .arr", { x: 0 }, { x: 10, duration: 0.25, yoyo: true, repeat: 3, ease: M.ease.hold }, t + 1.6);
  ghost("s21", -300);
})();

// ── Untertitel (9:16) ──
document.querySelectorAll(".sub").forEach(function (el) {
  var a = parseFloat(el.getAttribute("data-a")), b = parseFloat(el.getAttribute("data-b"));
  tl.set(el, { autoAlpha: 1 }, a);
  if (b < TOTAL) tl.set(el, { autoAlpha: 0 }, b);
});

// ── Der eine Shader-Moment: Zoom von „fühlen“ in die Verkaufspsychologie ──
window.HyperShader.init({
  bgColor: getComputedStyle(document.documentElement).getPropertyValue("--bg").trim(),
  scenes: ["s10", "s11"],
  timeline: tl,
  transitions: [{ time: T.s11 - 0.25, shader: "cinematic-zoom", duration: 0.5 }]
});

window.__timelines["main"] = tl;
