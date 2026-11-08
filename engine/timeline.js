/* engine/timeline.js -- THE EDIT of 《秋風恋歌》 (DeZI：R). Shot list: docs/STORYBOARD.md (shot ids s01..s58 = rows 01..58).
 * Structure kept from the template (helpers, JIZURA plans + curation, looks, global FX, vertical config); the night
 * defaults are re-tuned for a bright, high-key watercolour film (references/02 §13). Film scenes / fx: scenes/akikaze.js.
 * Every frame is a pure function of song time t. Bars = audio.json bars[].index (b33 = B(33)).
 */
(() => {
  'use strict';
  const Z = window.Z, D = Z.draw, E = Z.ease;
  const W = 1920, H = 1080;

  // ------------------------------------------------------------------ film identity
  Z.TITLE = '秋風恋歌';                                   // HUD, vertical header, end card
  Z.TITLE_SUB = 'AKIKAZE RENKA';                           // small Latin line under the title ('' = none)
  Z.ARTIST = 'DeZI：R';                              // artist name, used by the 9:16 header -- ask the artist
  Z.CREDIT = '原曲：秋風恋歌 / DeZI：R';      // title lockups, end card, vertical footer -- ask the artist
  const MADE_BY = '制作：Claude Opus 5.5';

  // ------------------------------------------------------------------ colour script (docs/CONCEPT.md); LUT rows P1..P5 = tools/style_palette_sheet.py
  const C = { washi: '#F4EFE4', ink: '#2B2722', inkSoft: '#6E655A', red: '#B8322A', crimson: '#C7302A', gold: '#F2D58A',
    green: '#9DBF5A', slate: '#33404F', mist: '#B9C6CF', snow: '#F2F5F8' };
  const LUT = { ima: 'P1', kaiso: 'P2', shigure: 'P3', momiji: 'P4', kazahana: 'P5' };

  const A = 'assets/char/', BG = 'assets/bg/', PR = 'assets/prop/';
  const AK = Z.AK;

  // ================================================================== setup
  Z.setup = async (audio) => {
    const lastBar = audio.bars.length ? audio.bars[audio.bars.length - 1].index : 0;
    const B = n => { const b = audio.bars.find(x => x.index === n); return b ? b.start : n > lastBar ? audio.music_cut : 0; };
    const nb = t => audio.beats.reduce((b, x) => (Math.abs(x - t) < Math.abs(b - t) ? x : b), audio.beats[0] ?? t);
    const END = audio.music_cut;                           // 280.12: the music stops, the last page holds
    const TAIL = 3.0;

    // ---- sections -> looks (daylight film: low bloom, high threshold, light vignette, no exposure pushes)
    const secs = audio.sections || [];
    for (const s of secs) s.look = s.label;
    Z.sectionAt = t => { let s = secs[0] || null; for (const x of secs) if (x.start <= t + 1e-6) s = x; return s; };
    Z.LOOK_DEFAULT = { boil: 0.8, bloom: 0.15, bloomThreshold: 0.93, grain: 0.045, vignette: 0.1, lutMix: 0 };
    Z.LOOKS = {
      verse: { boil: 0.7 },
      'pre-chorus': { boil: 0.8 },
      chorus: { boil: 0.9, bloom: 0.18, beatBloom: 0.05 },
      'last-chorus': { boil: 1.0, bloom: 0.2, beatBloom: 0.08 },
      break: { boil: 0.6, grain: 0.05 },
    };

    // ---- global punctuation: only two motivated light events, as colour flashes (never white on a white frame)
    const FLASH = [[B(86), 0.35, [1.0, 0.93, 0.78]], [B(95), 0.3, [1.0, 0.86, 0.8]]];
    Z.globalFX = (P, t) => {
      for (const [ft, a, col] of FLASH) { const d = t - ft; if (d >= 0 && d < 0.6) { const v = a * Math.exp(-d * 6); if (v > (P.flash || 0)) { P.flash = v; P.flashColor = col; } } }
    };

    // ---- leaf / prop sprites used by fx inside illust shots (illust only preloads bg / chars / layers)
    await Z.preload([...AK.RED, ...AK.GREEN, PR + 'prop_temari_faded.png']);

    // ---- JIZURA lyric plans
    let lrc = '';
    try { const r = await fetch(Z.ROOT + 'analysis/lyrics_mv.lrc'); if (r.ok) lrc = await r.text(); } catch (e) { /* no lyrics yet */ }
    if (!lrc.trim()) console.warn('analysis/lyrics_mv.lrc missing: rendering without the JIZURA lyric layer');
    lrc = lrc.replace(/^﻿/, '').replace(/^\[ti:.*\]\s*$/m, '');
    if (lrc.trim() && window.J) {
      JZ.setAudio({ duration: audio.duration, beats: audio.beats, energy: null, energyRate: 0 });
      const DENY = {
        layout: 'scatter ring wave labels pill knSeesaw knGearWords knTumble knPadGrid knPathRide zigzag arcTop gridCells bubble ticker searchBar chat notification ticket hanging wordCloud bounceLine elastic stickerBomb keycaps bubbles slotMachine flipBoard dotMatrix equalizer tape contents numbered poster ema ransom newspaper vinyl cassette bookSpine stampSheet calendar chochin routeMap stationSign noren tanzaku omikuji kakejiku shoji clapper warningLabel priceTag nameTag stickyNotes karuta cube flipCards accordion pile blocks balloons magnets tiles bulbs ledScroll billboard crowdBubbles crossword wordSearch puzzle dominoes burst fisheye origami zipper mosaicTiles stencil tyIndexTable tyStatCount typeSpecimen dictionary proofread magazine headlineDeck footnote ribbon flag pendulum knCollide knSlamStack halftoneBig tySquare tyRotBlock subtitleBar tile kaleido polaroid postcard letterPaper genkou panels splitScreen splitHalves wall cylinder cube',
        fx: 'panelWipe irisTrans doors blindsTrans splitSlide gridRepeat whiteFrame blackFrame strobe colorBars mirrorFlash starGlint focusLines speedLines halftone duotone kaleido bulge squash snapshot loopScroll crtOff tvStatic zoomStutter negativeRing edgeDetect hueShift posterize ditherBit rotateSnap invert bandInvert flash bloomFlash filmBurn',
        decor: 'dots arrows shapes qrBlock triangleSpin checkerStrip confetti petals heartsStars kamon seigaiha asanoha hanabi chochin shimenawa sensu momiji namiGashira memphis zigzagRibbon polkaPatch stripeCircle starburst cursorClick windowChrome progressBar toggleSwitch notifBell likeCounter mediaControls volumeBars musicNotes bubbles dandelion vines cloudPuffs tapePieces highlightMark staple paperClip indexTabs punchHoles swatches spinner tally qrBlock bracketsJP loopArrows halfCircles decoCorners tyColophon dateStamp tyTypeScale tyTextRule dataColumns timecodeBar rainStreaks glitchRects barcode reticle crosshair bars',
        cam: 'knCardFlip jelly bounce knJumpCut knTiltKick knReadPan knShearKick knRushIn shakeHard whipIn crashZoom beatPunch',
        treat: 'boxed marker knWordPlate circled sticker splitColor rainbow chrome extrude glow',
        enter: 'bubbles stickerPeel crumple loadingBar tokoroten bounceBig rubber neonOn heatHaze',
        exit: 'balloonOff crumpleOut peelOff popOut spinOut',
        bg: 'argyle tartan chevron houndstooth herringbone polka checker retroGrid eqBars kaleidoscope fireworks sunburst bigStripes isoCubes seigaiha asanoha tvBars splitDiag spiralArms squareTunnel moire noiseField scanBars',
        trans: 'flashCross shatterTiles knCornerSwing knStripSlam checker cubeTurn spinOut doorsOpen pixelate knStutterCut',
      };
      DENY.layout += ' shadowPlay glitchGrid tyBandHide tyRuby kanjiFocus contour circle tunnel curtain mirror type frameBox tyBaseline condensed gloss columnsBig tyLineFocus tyVRuler huge maskReveal tyErode tyCropGiant knQuarterTurn';   // + HUD-like labels (prompt, LINE nn, timecodes)   // giant glyphs over faces, blobs, black bars
      DENY.decor += ' watermarkKanji constellation moonPhases rulerEdge waveform grid rings headingTape fireflies atomOrbit cropMarks romajiLine tyRunningHead guides halftonePatch counter glyphLock sonarArcs tyBigPunct registration indexNum';   // gimmicks / additive light
      DENY.bg += ' vhsBand filmStrip borderFrame bokehBg';
      const MOODS = ['emotional', 'calm', 'editorial'];       // a quiet ballad: no glitch / pop parts
      const enabled = {};
      for (const g of J.GROUP_KEYS) {
        enabled[g] = {}; const deny = new Set((DENY[g] || '').split(/\s+/).filter(Boolean));
        for (const k of J.order(g)) {
          const d = J.registry(g)[k] || {}, tags = Array.isArray(d.tags) ? d.tags : null;
          let ok = !deny.has(k) && !/^hr[A-Z]/.test(k) && d.set !== 'horror';
          if (ok && MOODS && tags && !tags.some(m => MOODS.includes(m))) ok = false;
          if (k === 'none') ok = true;
          enabled[g][k] = ok;
        }
      }
      const common = {
        enabled, lyrics: lrc, fps: 30, res: 1080, aspect: '16:9', seed: 1111, unify: true, typeset: true, extra: true, wa: false, horror: false,
        colors: { accentOn: true, accent: C.red, ghostA: '#9A9284', ghostB: C.red }, schemes: [0, 3],
        fx: { motion: 0.45, glitch: 0.0, chroma: 0.08, decor: 0.3, density: 0.4, texture: 0.4, flash: false, koma: 12, hud: 'off', bgSwitch: 0 } };
      // main: 墨と朱 (brush display, Shippori Mincho, ink on washi) -- verses and choruses
      await JZ.addPlan('main', Object.assign({}, common, { style: 'sumi', mood: 'emotional' }));
      await JZ.addPlan('cf', Object.assign({}, common, { style: 'sumi', mood: 'emotional', centerFree: true }));
      // hand: 千鶴's voice in the Bridge -- Klee One handwriting, dark-green ink (forest light schemes)
      await JZ.addPlan('hand', Object.assign({}, common, { style: 'forest', mood: 'calm', schemes: [1, 3], seed: 1112,
        colors: { accentOn: true, accent: '#5E8C3A', ghostA: '#9DBF5A', ghostB: '#C9A487' } }));
      // pale: light text for the darkest rain / break frames
      await JZ.addPlan('pale', Object.assign({}, common, { style: 'sumi', mood: 'calm', schemes: [1], seed: 1113, centerFree: true }));
    }
    await Promise.all(['400 160px "Yuji Syuku"', '500 26px "Shippori Mincho B1"', '600 40px "Klee One"'].map(f => document.fonts.load(f, Z.TITLE + Z.CREDIT + MADE_BY + 'てんまりうた')));

    // ================================================================== shot helpers
    const S = [];
    const shot = (id, t0, t1, scene, args, extra = {}) => { if (t1 > t0 + 1e-3) S.push(Object.assign({ id, t0, t1, scene, args }, extra)); };
    const look = (lut, mix = 0.14, more = {}) => Object.assign({ lutA: LUT[lut], lutMix: mix }, more);
    const ill = (id, t0, t1, args, extra) => shot(id, t0, t1, 'illust', args, extra);
    const sayo = (img, x, y, h, more = {}) => Object.assign({ img: A + img + '.png', x, y, h, wave: { amp: 6, from: 0.35 } }, more);
    // 千鶴: slightly see-through with a soft warm halo -- she is no longer of this world (docs/CHARACTER.md)
    const chizu = (img, x, y, h, more = {}) => Object.assign({ img: A + img + '.png', x, y, h, alpha: 0.86, rim: { color: '#FFF4DC', off: [0, 0] },
      glowAt: [0, 0.55, 0.6], glowColor: '#FFF1D6', glowA: 0.18, wave: { amp: 5, from: 0.35 } }, more);
    const ink = (dur = 0.9, seed = 3) => ({ type: 'ink', dur, seed });
    const xf = (dur = 0.6) => ({ type: 'xfade', dur });
    const drift = (o = {}) => AK.leaves(Object.assign({ n: 14, size: [36, 70], fall: 90, wind: 25, alpha: 0.95 }, o));

    // 3D shots: until the Blender renders exist (blender/renders/<shot>/f_####.jpg) a 2D stand-in on the same plate
    const HAVE_3D = { pathA: true, stormB: true };

    // ===== Intro (quiet) b0-8 : 和紙 -- the pair meets and is blown apart
    shot('s01', 0, B(4), 'leaves', { bg: BG + 'bg_washi.png', mode: 'pair', meet: B(3), cx: 960, cy: 470, r: 150, size: 260 },
      { lyric: 'none', hud: false, post: { boil: 0.5, grain: 0.03 } });
    shot('s02', B(4), B(8), 'leaves', { bg: BG + 'bg_washi.png', mode: 'part', meet: B(3), cx: 960, cy: 470, r: 150, size: 260, gust: B(6), land: 980 },
      { lyric: 'none', hud: false, post: { boil: 0.5, grain: 0.03 } });

    // ===== Intro (band) b8-21 : 3D-A, the path one-take, title over its first bars
    const titleText = (ctx, St) => {
      const t = St.t, t0 = B(8) + 0.25, out = Z.clamp((B(13) - t) / 1.2);
      if (out <= 0) return;
      ctx.save(); ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      ctx.shadowColor = 'rgba(244,239,228,0.85)'; ctx.shadowBlur = 18;
      [...Z.TITLE].forEach((ch, i) => {                         // written one character per beat
        const k = E.outCubic(Z.clamp((t - t0 - i * 0.588) / 0.5)); if (k <= 0) return;
        ctx.globalAlpha = k * out; ctx.fillStyle = C.ink; D.font(ctx, 150, 'brush', 400);
        ctx.fillText(ch, 960 + (i - 1.5) * 168, 470 + 20 * (1 - k));
      });
      const k2 = Z.clamp((t - t0 - 2.6) / 0.8) * out;
      ctx.globalAlpha = k2; ctx.fillStyle = C.inkSoft; D.font(ctx, 26, 'mincho', 500);
      ctx.fillText(Z.TITLE_SUB.split('').join(' '), 960, 590);
      ctx.globalAlpha = Z.clamp((t - t0 - 3.4) / 0.8) * out; D.font(ctx, 24, 'mincho', 500);
      ctx.fillText(Z.CREDIT, 960, 640);
      ctx.restore();
    };
    if (HAVE_3D.pathA) {                                        // rendered on twos: 459 frames at 15 fps, frame 1 = B(8)
      const pathA = { pattern: 'blender/renders/pathA/f_####.jpg', t0: B(8), fps: 15, frames: 459 };
      shot('s03', B(8), B(17), 'seqx', Object.assign({ fx: [drift({ seed: 3 })] }, pathA),
        { lyric: 'none', hud: false, text: titleText, trans: xf(0.25), post: look('ima', 0.1) });
      shot('s04', B(17), B(21), 'seqx', Object.assign({
        chars: [sayo('sayo_walk_back', 1180, 900, 380, { x2: 1220, y2: 860, h2: 330, in: { dur: 1.2 } })], fx: [drift({ seed: 4 })] }, pathA),
        { trans: { type: 'cut' }, post: look('ima', 0.1) });
    } else {
      ill('s03', B(8), B(17), { bg: BG + 'bg_path_present.png', bgFrom: { zoom: 1.0, x: -0.2, y: 0.4 }, bgTo: { zoom: 1.32, x: 0.25, y: -0.1 }, bgEase: 'linear', fx: [drift({ seed: 3 })] },
        { lyric: 'none', hud: false, text: titleText, trans: xf(0.25), post: look('ima', 0.1) });
      ill('s04', B(17), B(21), { bg: BG + 'bg_path_present.png', bgFrom: { zoom: 1.32, x: 0.25, y: -0.1 }, bgTo: { zoom: 1.45, x: 0.4, y: -0.2 }, bgEase: 'outSine',
        chars: [sayo('sayo_walk_back', 1180, 900, 380, { x2: 1220, y2: 860, h2: 330, in: { dur: 1.2 } })], fx: [drift({ seed: 4 })] },
        { post: look('ima', 0.1) });
    }

    // ===== Verse 1 b21-25
    ill('s05', B(21), nb(52.53), { bg: BG + 'bg_canopy.png', bgFrom: { zoom: 1.08, rot: -0.02 }, bgTo: { zoom: 1.16, rot: 0.03 }, fx: [drift({ seed: 5, n: 10 })] },
      { trans: xf(0.8), post: look('ima', 0.12) });
    ill('s06', nb(52.53), B(25), { bg: BG + 'bg_path_present.png', bgFrom: { zoom: 1.5, x: 0.3 }, bgTo: { zoom: 1.56, x: 0.32 },
      chars: [sayo('sayo_hum', 1240, 1120, 980)], fx: [AK.leaves({ n: 5, seed: 6, size: [60, 90], fall: 110, wind: -20, t0: nb(52.53), area: [900, -140, 1700, 1220] })] },
      { plan: 'cf', trans: xf(0.5), post: look('ima', 0.1) });

    // ===== Pre-chorus 1 b25-33 : 現在段 with 回憶段 flashes
    ill('s07', B(25), nb(60.25), { bg: A + 'hands_temari_faded.png', bgFrom: { zoom: 1.04 }, bgTo: { zoom: 1.12 } }, { trans: xf(0.5), post: look('ima', 0.12) });
    ill('s08', nb(60.25), nb(62.55), { bg: A + 'hands_temari_new.png', bgFrom: { zoom: 1.12 }, bgTo: { zoom: 1.04 } }, { plan: 'cf', trans: ink(0.8, 4), post: look('kaiso', 0.12) });
    ill('s09', nb(62.55), nb(67.27), { bg: BG + 'bg_path_present.png', bgFrom: { zoom: 1.2, x: -0.3 }, bgTo: { zoom: 1.26, x: -0.25 },
      chars: [sayo('sayo_side_leaf', 760, 1110, 1000)] },
      { plan: 'cf', trans: ink(0.8, 5), post: S2 => look('ima', 0.12, { saturation: 1 - 0.45 * S2.p }) });
    ill('s10', nb(67.27), nb(71.98), { bg: BG + 'bg_path_summer.png', bgFrom: { zoom: 1.1, x: 0.1 }, bgTo: { zoom: 1.18, x: -0.05 },
      chars: [chizu('chizuru_sing', 900, 1120, 1000, { alpha: 1 })], fx: [{ type: 'dust', n: 40, color: 'rgba(255,240,200,0.6)' }] },
      { plan: 'cf', trans: ink(0.8, 6), post: look('kaiso', 0.1) });
    ill('s11', nb(71.98), nb(76.06), { bg: BG + 'bg_path_present.png', bgFrom: { zoom: 1.5, x: -0.3 }, bgTo: { zoom: 1.55, x: -0.3 },
      fxBack: [AK.ripples({ x: 960, y: 760, color: C.red, alpha: 0.28 })], chars: [sayo('sayo_hand_chest', 960, 1120, 1000)] },
      { plan: 'cf', trans: ink(0.8, 7), post: look('ima', 0.12) });

    // ===== Chorus 1 b33-42 : leaves everywhere, つがいの楓, 片時雨
    ill('s12', nb(76.06), nb(78.49), { bg: BG + 'bg_path_present.png', bgFrom: { zoom: 1.05 }, bgTo: { zoom: 1.12 },
      chars: [sayo('sayo_back_lookup', 1060, 1000, 420)], fx: [drift({ n: 60, seed: 12, fall: 160, size: [40, 90], t0: nb(76.06) - 0.4 })] },
      { trans: { type: 'cut' }, post: look('ima', 0.1) });
    ill('s13', nb(78.49), nb(80.78), { bg: BG + 'bg_canopy.png', bgFrom: { zoom: 1.2 }, bgTo: { zoom: 1.26 },
      chars: [sayo('sayo_lookup', 760, 1120, 1020)], fx: [drift({ n: 26, seed: 13, size: [70, 150], fall: 180 })] },
      { plan: 'cf', post: look('ima', 0.1) });
    shot('s14', nb(80.78), nb(85.49), 'leaves', { bg: BG + 'bg_path_present.png', bgFrom: { zoom: 1.6 }, bgTo: { zoom: 1.66 }, mode: 'pair', meet: B(35), cx: 960, cy: 520, r: 170, size: 250, spin: 1.3,
      tint: [{ color: C.washi, a: 0.55, comp: 'source-over' }], drift: { n: 8, seed: 14, size: [30, 50], fall: 70, alpha: 0.5 } },
      { plan: 'cf', trans: ink(0.6, 8), post: look('ima', 0.06) });
    ill('s15', nb(85.49), nb(87.84), { bg: BG + 'bg_path_present.png', bgFrom: { zoom: 1.2, x: 0.3 }, bgTo: { zoom: 1.24, x: -0.3 }, shake: 3,
      chars: [sayo('sayo_wind', 960, 1060, 940, { wave: { amp: 14, from: 0.3, speed: 6 } })], fx: [drift({ n: 40, seed: 15, wind: -900, fall: 60, swing: 0.3 })] },
      { post: look('ima', 0.1) });
    shot('s16', nb(87.84), nb(90.17), 'leaves', { bg: BG + 'bg_sky_overcast.png', mode: 'solo', color: 'green', dir: 'up', x: 700, y: 900, size: 160 },
      { post: look('ima', 0.08) });
    ill('s17', nb(90.17), B(40), { bg: BG + 'bg_sky_overcast.png', bgFrom: { zoom: 1.2, y: 0.8 }, bgTo: { zoom: 1.2, y: -0.4 },
      chars: [sayo('sayo_back_lookup', 960, 1140, 760, { y2: 1380 })] }, { trans: xf(0.4), post: look('ima', 0.1) });
    ill('s18', B(40), B(42), { bg: BG + 'bg_sky_overcast.png', bgFrom: { zoom: 1.12 }, bgTo: { zoom: 1.2 }, fx: [AK.katashigure({ split: 980 })] },
      { trans: xf(0.4), post: look('shigure', 0.08) });

    // ===== Interlude 1 b42-49 : the whole memory
    ill('s19', B(42), B(44), { bg: BG + 'bg_path_summer.png', bgFrom: { zoom: 1.12, y: 0.3 }, bgTo: { zoom: 1.22, y: 0.1 },
      chars: [sayo('sayo_walk_back', 1000, 960, 470), chizu('chizuru_walk_back', 1180, 960, 470, { alpha: 1, glowA: 0 })],
      fx: [{ type: 'dust', n: 50, color: 'rgba(255,240,200,0.6)' }] }, { lyric: 'none', trans: ink(1.2, 9), post: look('kaiso', 0.12) });
    ill('s20', B(44), B(45), { bg: BG + 'bg_path_summer.png', bgFrom: { zoom: 1.3, x: -0.2 }, bgTo: { zoom: 1.34, x: -0.2 },
      chars: [chizu('chizuru_bounce', 900, 1060, 900, { alpha: 1, glowA: 0 })], fx: [{ type: 'dust', n: 40, color: 'rgba(255,240,200,0.6)' }] },
      { lyric: 'none', trans: xf(0.4), post: look('kaiso', 0.1) });
    ill('s20b', B(45), B(46), { bg: BG + 'bg_path_summer.png', bgFrom: { zoom: 1.4, x: 0.3 }, bgTo: { zoom: 1.44, x: 0.3 },
      chars: [sayo('sayo_smile', 1000, 1120, 1000)] }, { lyric: 'none', trans: xf(0.4), post: look('kaiso', 0.1) });
    ill('s21', B(46), nb(110.84), { bg: BG + 'bg_steps_summer.png', bgFrom: { zoom: 1.06 }, bgTo: { zoom: 1.12 },
      chars: [sayo('sayo_sit', 760, 1010, 560), chizu('chizuru_sit', 1080, 1010, 560, { alpha: 1, glowA: 0 })] },
      { lyric: 'none', trans: xf(0.6), post: look('kaiso', 0.1) });
    ill('s22', nb(110.84), B(48), { bg: A + 'hands_two_leaves.png', bgFrom: { zoom: 1.08 }, bgTo: { zoom: 1.14 } }, { lyric: 'none', trans: xf(0.3), post: look('kaiso', 0.08) });
    ill('s23', B(48), B(49), { bg: A + 'hands_two_leaves.png', bgFrom: { zoom: 1.14 }, bgTo: { zoom: 1.2, y: 0.3 },
      fx: [{ type: 'rain', n: 260, angle: 0.08, speed: 1300, len: 70, color: 'rgba(225,235,245,0.6)' },
        { type: 'custom', fn: (ctx, St) => D.fill(ctx, '#8698A8', 0.55 * E.inSine(St.p), 'multiply') }] },
      { lyric: 'none', post: St => look('shigure', 0.1 + 0.25 * St.p, { saturation: 1 - 0.5 * St.p }) });

    // ===== Verse 2 b49-57
    ill('s24', B(49), nb(118.43), { bg: BG + 'bg_path_present.png', bgFrom: { zoom: 1.15, x: -0.5 }, bgTo: { zoom: 1.15, x: 0.5 }, fx: [drift({ seed: 24, wind: 120 })] },
      { trans: xf(0.5), post: look('ima', 0.12) });
    ill('s25', nb(118.43), nb(123.81), { bg: BG + 'bg_steps_autumn.png', bgFrom: { zoom: 1.06 }, bgTo: { zoom: 1.1 },
      chars: [sayo('sayo_sit', 760, 1010, 560)], fx: [drift({ seed: 25, n: 8 })] }, { trans: xf(0.6), post: look('ima', 0.12) });
    ill('s26', nb(123.81), nb(127.78), { bg: A + 'sayo_listen.png', bgFrom: { zoom: 1.04 }, bgTo: { zoom: 1.1 }, fx: [AK.songLeaves({ area: [1100, 0, 1880, H], alpha: 0.7 })] },
      { plan: 'cf', trans: xf(0.5), post: look('ima', 0.08) });
    ill('s27', nb(127.78), B(57), { bg: BG + 'bg_steps_autumn.png', bgFrom: { zoom: 1.4, x: -0.4 }, bgTo: { zoom: 1.45, x: -0.4 },
      fxBack: [AK.ripples({ x: 820, y: 700, color: C.red, alpha: 0.24 })], chars: [sayo('sayo_hand_chest', 820, 1120, 980)] },
      { plan: 'cf', trans: xf(0.5), post: look('ima', 0.12) });

    // ===== Pre-chorus 2 b57-65 : 言えない / 癒えない / 消えない (時雨)
    const W3 = [{ text: '言えない', rest: '恋は　その胸に', at: B(57) + 0.05, x: 1380, melt: B(58) + 1.0 },
      { text: '癒えない', rest: '傷を　重ねたね', at: B(59) + 0.05, x: 960, melt: B(60) + 1.0 },
      { text: '消えない', rest: '愛よ　叶うなら', at: B(61) + 0.05, x: 540, melt: B(62) + 1.4 }];
    shot('s28', B(57), B(59), 'iienai', { bg: BG + 'bg_washi.png', words: W3.slice(0, 1) }, { lyric: 'none', trans: ink(0.6, 10), post: Object.assign(look('shigure', 0.1), { boil: 0.4 }) });
    shot('s29', B(59), B(61), 'iienai', { bg: BG + 'bg_washi.png', words: W3.slice(0, 2) }, { lyric: 'none', post: Object.assign(look('shigure', 0.1), { boil: 0.4 }) });
    shot('s30', B(61), nb(147.26), 'iienai', { bg: BG + 'bg_washi.png', words: W3 }, { lyric: 'none', post: Object.assign(look('shigure', 0.1), { boil: 0.4 }) });
    ill('s31', nb(147.26), nb(151.36), { bg: BG + 'bg_path_rain.png', bgFrom: { zoom: 1.5, x: 0.2 }, bgTo: { zoom: 1.55, x: 0.2 },
      chars: [sayo('sayo_sing_rain', 1240, 1120, 1000)], fx: [{ type: 'rain', n: 220, angle: 0.1, speed: 1500, len: 60, color: 'rgba(230,238,245,0.45)' }] },
      { plan: 'cf', trans: xf(0.5), post: look('shigure', 0.14) });

    // ===== Chorus 2 b65-73 : only the red leaf, in the rain
    const rain = (n = 260, a = 0.45) => ({ type: 'rain', n, angle: 0.1, speed: 1500, len: 60, color: `rgba(230,238,245,${a})` });
    ill('s32', nb(151.36), nb(153.70), { bg: BG + 'bg_path_rain.png', bgFrom: { zoom: 1.05 }, bgTo: { zoom: 1.1 },
      chars: [sayo('sayo_back_lookup', 1060, 1000, 420)], fx: [drift({ seed: 32, red: 1, n: 30, fall: 200, swing: 0.5 }), rain()] }, { post: look('shigure', 0.12) });
    shot('s33', nb(153.70), nb(156.16), 'leaves', { bg: BG + 'bg_path_rain.png', bgFrom: { zoom: 1.5 }, bgTo: { zoom: 1.56 }, mode: 'solo', color: 'red', dir: 'down', x: 1060, y: 820, size: 170 },
      { post: look('shigure', 0.12) });
    ill('s34', nb(156.16), nb(158.49), { bg: BG + 'bg_path_rain.png', bgFrom: { zoom: 1.7, y: 0.9 }, bgTo: { zoom: 1.76, y: 0.9 },
      layers: [{ img: PR + 'prop_temari_faded.png', x: 900, y: 860, h: 300, h2: 310, anchor: [0.5, 0.5] }], fx: [rain(300, 0.5)] },
      { plan: 'cf', post: look('shigure', 0.12) });
    ill('s35', nb(158.49), nb(160.87), { bg: BG + 'bg_path_rain.png', bgFrom: { zoom: 1.5, x: 0.3 }, bgTo: { zoom: 1.55, x: 0.3 },
      chars: [sayo('sayo_hum', 1240, 1120, 980)], fx: [rain()] }, { plan: 'cf', post: look('shigure', 0.12) });
    // 詠い / 詠え / 詠う (word onsets 160.87 / 162.05 / 163.51, analysis/lyrics.json): one picture per word
    ill('s36', nb(160.87), nb(162.05), { bg: BG + 'bg_path_rain.png', bgFrom: { zoom: 1.6, x: -0.3 }, bgTo: { zoom: 1.64, x: -0.3 },
      chars: [sayo('sayo_sing_rain', 820, 1160, 1080)], fx: [rain()] }, { plan: 'cf', post: look('shigure', 0.12) });
    ill('s36b', nb(162.05), nb(163.51), { bg: A + 'hands_temari_faded.png', bgFrom: { zoom: 1.2 }, bgTo: { zoom: 1.26 }, fx: [rain(160, 0.4)] },
      { plan: 'cf', post: look('shigure', 0.14) });
    ill('s36c', nb(163.51), nb(165.49), { bg: A + 'sayo_listen.png', bgFrom: { zoom: 1.16 }, bgTo: { zoom: 1.22 }, fx: [rain(160, 0.4)] },
      { plan: 'cf', post: look('shigure', 0.14) });
    ill('s37', nb(165.49), B(73), { bg: BG + 'bg_path_rain.png', bgFrom: { zoom: 1.45, x: -0.2 }, bgTo: { zoom: 1.52, x: -0.2 },
      chars: [sayo('sayo_sleeve', 900, 1120, 1000)], fx: [rain(300, 0.5)] }, { plan: 'cf', trans: xf(0.4), post: look('shigure', 0.16) });

    // ===== Break b73-79 : the greyest, longest hold
    ill('s38', B(73), B(77), { bg: BG + 'bg_path_rain.png', bgFrom: { zoom: 1.05 }, bgTo: { zoom: 1.22, y: 0.2 }, bgEase: 'linear',
      chars: [sayo('sayo_crouch', 980, 960, 380, { x2: 980, y2: 990, h2: 470, ease: 'linear', wave: false })], fx: [rain(320, 0.5)] },
      { lyric: 'none', trans: xf(1.0), post: look('shigure', 0.2, { saturation: 0.8 }) });
    ill('s39', B(77), B(79), { bg: A + 'hands_temari_faded.png', bgFrom: { zoom: 1.1 }, bgTo: { zoom: 1.18 }, fx: [rain(200, 0.4)] },
      { lyric: 'none', trans: xf(0.8), post: look('shigure', 0.22, { saturation: 0.75 }) });

    // ===== Build b79-82 : a little light
    ill('s40', B(79), B(81), { bg: BG + 'bg_sky_rain.png', bgFrom: { zoom: 1.1 }, bgTo: { zoom: 1.2, x: 0.4, y: -0.3 }, fx: [rain(160, 0.35)] },
      { lyric: 'none', trans: xf(0.6), post: look('shigure', 0.15) });
    ill('s41', B(81), nb(191.92), { bg: BG + 'bg_path_rain.png', bgFrom: { zoom: 1.6, y: 0.6 }, bgTo: { zoom: 1.64, y: 0.6 },
      chars: [sayo('sayo_crouch', 900, 1300, 1150, { wave: false })],
      fx: [{ type: 'rain', n: 120, angle: 0.06, speed: 700, len: 30, color: 'rgba(230,238,245,0.35)' },
        AK.leaves({ n: 1, seed: 41, red: 0, size: [120, 120], fall: 120, t0: B(81), area: [1200, -140, 1500, 1220] })] },
      { lyric: 'none', post: look('shigure', 0.12) });

    // ===== Bridge b82-89 : 千鶴 speaks, the clouds open
    ill('s42', nb(191.92), nb(198.75), { bg: BG + 'bg_sky_rain.png', bgFrom: { zoom: 1.15, y: 0.4 }, bgTo: { zoom: 1.2, y: -0.2 },
      chars: [sayo('sayo_lookup_tears', 960, 1130, 1000, { front: true })] }, { plan: 'hand', trans: xf(0.5), post: look('shigure', 0.1) });
    ill('s43', nb(198.75), B(86), { bg: BG + 'bg_sky_open.png', bgFrom: { zoom: 1.3, y: 0.5 }, bgTo: { zoom: 1.22, y: 0.2 } },
      { plan: 'hand', trans: xf(0.8), post: look('kazahana', 0.06, { exposure: -0.04 }) });
    ill('s44', B(86), nb(206.06), { bg: BG + 'bg_sky_open.png', bgFrom: { zoom: 1.12 }, bgTo: { zoom: 1.06 },
      fxBack: [{ type: 'rays', x: 960, y: 200, n: 16, len: 1400, color: '#FFF1D6', a: 0.12 }],
      chars: [chizu('chizuru_float', 960, 940, 820, { in: { dur: 2.0, dy: 60 } })] }, { plan: 'hand', post: look('kazahana', 0.05, { exposure: -0.06 }) });
    ill('s45', nb(206.06), nb(207.82), { bg: BG + 'bg_sky_open.png', bgFrom: { zoom: 1.4 }, bgTo: { zoom: 1.44 },
      chars: [chizu('chizuru_smile', 960, 1120, 1000)] }, { plan: 'hand', trans: xf(0.3), post: look('kazahana', 0.05, { exposure: -0.06 }) });

    // ===== Last chorus b89-97 : full crimson
    if (HAVE_3D.stormB) shot('s46', nb(207.82), B(92), 'seq', { pattern: 'blender/renders/stormB/f_####.jpg', t0: nb(207.82), fps: 30, frames: 230 },
      { trans: { type: 'cut' }, post: look('momiji', 0.08) });
    else ill('s46', nb(207.82), B(92), { bg: BG + 'bg_forest_red.png', bgFrom: { zoom: 1.0, y: 0.5 }, bgTo: { zoom: 1.4, y: -0.3 }, bgEase: 'inOutSine',
      fx: [AK.leaves({ n: 90, seed: 46, size: [40, 120], fall: 260, wind: 60, red: 0.97 })] }, { trans: { type: 'cut' }, post: look('momiji', 0.08) });
    ill('s47', B(92), nb(221.94), { bg: BG + 'bg_forest_red.png', bgFrom: { zoom: 1.2, y: 0.6 }, bgTo: { zoom: 1.25, y: 0.3 },
      chars: [sayo('sayo_reach_up', 560, 1100, 700, { front: true }), chizu('chizuru_reach_down', 1420, 520, 520)],
      fx: [AK.leafLine({ a: [640, 420], b: [1340, 340], bend: 260, at: B(92) + 0.3, dur: 2.0 }), drift({ seed: 47, n: 20, red: 1 })] },
      { plan: 'cf', trans: xf(0.4), post: look('momiji', 0.08) });
    ill('s48', nb(221.94), nb(226.68), { bg: BG + 'bg_forest_red.png', bgFrom: { zoom: 1.3 }, bgTo: { zoom: 1.4 }, beatZoom: 0.01,
      chars: [sayo('sayo_sing_power', 960, 1120, 1020, { front: true, wave: { amp: 14, from: 0.3, speed: 5 } })],
      fx: [AK.leaves({ n: 120, seed: 48, size: [36, 90], fall: 700, wind: 40, swing: 0.25, red: 1, t0: B(95) - 0.6 })] },
      { plan: 'cf', trans: { type: 'cut' }, post: look('momiji', 0.1) });

    // ===== Coda b97-105 : the title line, rain into 風花
    shot('s49', nb(226.68), nb(231.35), 'leaves', { bg: BG + 'bg_washi.png', mode: 'rise', meet: nb(226.68) + 1.2, cx: 960, cy: 620, r: 160, size: 240, spin: 1.1 },
      { trans: ink(0.9, 11), post: { boil: 0.5, grain: 0.03 } });
    ill('s50', nb(231.35), nb(236.07), { bg: BG + 'bg_path_snow.png', bgFrom: { zoom: 1.5, x: 0.3 }, bgTo: { zoom: 1.56, x: 0.3 },
      chars: [sayo('sayo_smile_snow', 1240, 1120, 1000)], fx: [AK.kazahana({ t0: nb(231.35), t1: B(100) })] },
      { plan: 'cf', trans: xf(0.6), post: look('kazahana', 0.08) });
    ill('s51', nb(236.07), nb(240.80), { bg: BG + 'bg_path_snow.png', bgFrom: { zoom: 1.4, x: -0.3 }, bgTo: { zoom: 1.45, x: -0.3 },
      chars: [chizu('chizuru_wave', 820, 1120, 980, { out: { at: 3.4, dur: 1.3, dy: -40 } })], fx: [AK.kazahana({})] },
      { plan: 'cf', trans: xf(0.6), post: look('kazahana', 0.08) });
    ill('s52', nb(240.80), B(105), { bg: A + 'sayo_tear_smile.png', bgFrom: { zoom: 1.04 }, bgTo: { zoom: 1.1 }, fx: [AK.kazahana({ alpha: 0.7 })] },
      { plan: 'cf', trans: xf(0.5), post: look('kazahana', 0.06) });

    // ===== Outro b105-118 + tail : white-out, pressed leaves, end card
    ill('s53', B(105), B(109), { bg: BG + 'bg_path_snow.png', bgFrom: { zoom: 1.1 }, bgTo: { zoom: 1.25, y: -0.1 },
      chars: [sayo('sayo_walk_back', 980, 880, 360, { x2: 1060, y2: 760, h2: 220, ease: 'linear' })], fx: [AK.kazahana({ n: 200 })] },
      { lyric: 'none', trans: xf(0.8), post: look('kazahana', 0.08) });
    ill('s54', B(109), B(113), { bg: BG + 'bg_path_snow.png', bgFrom: { zoom: 1.25, y: -0.1 }, bgTo: { zoom: 1.35, y: -0.2 }, fx: [AK.kazahana({ n: 260, size: 1.3 }),
      { type: 'custom', fn: (ctx, St) => D.fill(ctx, '#FFFFFF', E.inOutSine(St.p)) }] }, { lyric: 'none', post: look('kazahana', 0.06) });
    const OSH = { img: PR + 'prop_oshiba.png', appear: [B(113), B(115)] };
    shot('s55', B(113), B(116), 'oshiba', OSH, { lyric: 'none', hud: false, post: { boil: 0.3, grain: 0.03 } });
    shot('s56', B(116), B(118), 'oshiba', Object.assign({ title: { at: B(116) + 0.2 } }, OSH), { lyric: 'none', hud: false, post: { boil: 0.3, grain: 0.03 } });
    const CARD = Object.assign({ title: { at: -1 }, credits: { at: B(118) + 0.2, lines: [Z.CREDIT, MADE_BY] } }, OSH);
    shot('s57', B(118), END, 'oshiba', CARD, { lyric: 'none', hud: false, post: { boil: 0.3, grain: 0.03 } });
    shot('s58', END, END + TAIL, 'oshiba', CARD, { lyric: 'none', hud: false, post: { boil: 0, grain: 0.03 } });

    Z.SHOTS = S;
    window.__zankoMeta.duration = END + TAIL;

    // ---- no corner HUD in this film (the typography is ink on paper)
    Z.hud = () => {};

    // ---- 9:16 vertical build
    Z.VERTICAL_CFG = {
      full: ['s01', 's02', 's14', 's16', 's28', 's29', 's30', 's49', 's55', 's56', 's57', 's58'],
      planMap: { main: 'v_main', cf: 'v_main', hand: 'v_hand', pale: 'v_pale' },
      title: Z.TITLE, sub: Z.TITLE_SUB, artist: Z.ARTIST, credits: [B(8), B(17)],
      schemes: 'light', ambience: [236, 230, 218],
    };
  };
})();
