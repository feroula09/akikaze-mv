/* 《秋風恋歌》 scenes and fx (docs/STORYBOARD.md "需要新寫的場景與 fx").
 * Every motion is a closed-form function of song time t (no state, no unseeded randomness).
 *
 *   Z.AK.leaves({...})        fx: a drift of falling maple leaves (red / green mix), for illust fx / fxBack
 *   Z.AK.katashigure({...})   fx: rain on one side of the frame only, light on the other
 *   Z.AK.kazahana({...})      fx: rain streaks slow down, whiten and turn into snowflakes between t0 and t1
 *   Z.AK.leafLine({...})      fx: leaves flowing along a curve from point a to point b
 *   Z.AK.songLeaves({...})    fx: hand-written kana of the 手毬歌 drifting down like leaves
 *   Z.AK.ripples({...})       fx: watercolour rings spreading from a point, one per beat
 *   scene 'leaves'            つがいの楓 choreography: pair / part / solo / rise
 *   scene 'iienai'            a vertical brush word written stroke by stroke, then melted by rain
 *   scene 'oshiba'            pressed leaves appearing in washi + small title + end card
 */
(() => {
  'use strict';
  const Z = window.Z, D = Z.draw, E = Z.ease;
  const W = 1920, H = 1080;
  const P = 'assets/prop/';
  const RED = ['a', 'b', 'c'].map(s => P + `prop_leaf_red_${s}.png`);
  const GREEN = ['a', 'b', 'c'].map(s => P + `prop_leaf_green_${s}.png`);
  const INK = '#2B2722';

  // ---------------------------------------------------------------- one leaf: the falling-leaf arc (ひらひら)
  // A leaf swings like a pendulum while it sinks: sideways offset = sin(phase), it tilts along the swing and
  // tumbles (horizontal scale = cos of a slower phase, so it flips over and shows its edge now and then).
  const flutter = (t, i, seed, swing = 1) => {
    const w = 1.6 + 0.9 * Z.rnd(i, seed + 7), ph = Z.rnd(i, seed + 8) * Z.TAU;
    const s = Math.sin(w * t + ph);
    return {
      dx: swing * (70 + 60 * Z.rnd(i, seed + 9)) * s,
      dy: swing * 18 * Math.cos(2 * (w * t + ph)),                         // it lifts a little at each end of the swing
      rot: 0.75 * s * swing + Z.rnds(i, seed + 10) * 0.6,
      sx: Math.max(0.18, Math.abs(Math.cos(0.7 * w * t + ph * 1.7))) * Math.sign(Math.cos(0.7 * w * t + ph * 1.7) || 1),
    };
  };
  const drawLeaf = (ctx, src, x, y, size, rot, sx, alpha = 1) => {
    const img = Z.imgSync(src); if (!img) return;
    const s = size / Math.max(img.width, img.height);
    ctx.save(); ctx.globalAlpha *= alpha; ctx.translate(x, y); ctx.rotate(rot); ctx.scale(sx * s, s);
    ctx.imageSmoothingEnabled = true; ctx.imageSmoothingQuality = 'high';
    ctx.drawImage(img, -img.width / 2, -img.height / 2); ctx.restore();
  };
  const leafImg = (i, seed, red) => (Z.rnd(i, seed + 3) < red ? RED : GREEN)[Math.floor(Z.rnd(i, seed + 4) * 3)];

  // ---------------------------------------------------------------- fx: a drift of leaves
  // n, seed, red (0..1 share of red leaves), size [min,max] px, fall px/s, wind px/s, swing, area [x0,y0,x1,y1],
  // alpha, t0 (leaves start falling from the top at t0 instead of being already in the air), rain (fast, straight)
  const leaves = (o = {}) => ({ type: 'custom', fn: (ctx, S) => {
    const n = o.n ?? 24, seed = o.seed ?? 11, red = o.red ?? 1, [s0, s1] = o.size || [44, 90];
    const fall = o.fall ?? 120, wind = o.wind ?? 30, swing = o.swing ?? 1, A = o.area || [-120, -140, W + 120, H + 140];
    const span = A[3] - A[1], t = S.t;
    for (let i = 0; i < n; i++) {
      const sp = fall * (0.75 + 0.5 * Z.rnd(i, seed + 1));
      let k;
      if (o.t0 != null) { k = (t - o.t0) * sp / span - Z.rnd(i, seed + 2) * 1.2; if (k < 0 || k > 1) continue; }
      else k = Z.fract(Z.rnd(i, seed + 2) + t * sp / span);
      const f = flutter(t, i, seed, swing);
      const x = A[0] + Z.rnd(i, seed) * (A[2] - A[0]) + wind * (k * span / sp) + f.dx;
      const y = A[1] + k * span + f.dy;
      const size = s0 + (s1 - s0) * Z.rnd(i, seed + 5);
      drawLeaf(ctx, leafImg(i, seed, red), Z.fract((x + 200) / (W + 400)) * (W + 400) - 200, y, size, f.rot + (o.rain ? 0 : 0), f.sx, o.alpha ?? 1);
    }
  } });

  // ---------------------------------------------------------------- fx: 片時雨 -- rain on one side only
  let rainLayer = null;                                                      // reused offscreen canvas
  // split: x of the border (px), side: 'right' | 'left' (where it rains), soft: border blur width, color, n
  const katashigure = (o = {}) => ({ type: 'custom', fn: (ctx, S) => {
    const split = o.split ?? W * 0.55, rainRight = (o.side || 'right') === 'right', soft = o.soft ?? 160;
    // the dry side: a little warm light (soft-light keeps it from clipping on a bright plate)
    ctx.save(); ctx.globalCompositeOperation = 'soft-light';
    const g = ctx.createLinearGradient(split - soft, 0, split + soft, 0);
    const warm = 'rgba(255,226,170,0.55)', cold = 'rgba(70,90,115,0.55)';
    g.addColorStop(0, rainRight ? warm : cold); g.addColorStop(1, rainRight ? cold : warm);
    ctx.fillStyle = g; ctx.fillRect(0, 0, W, H); ctx.restore();
    // rain, faded out across the border band
    const c = rainLayer || (rainLayer = Z.canvas(W, H)), x = c.getContext('2d'); x.clearRect(0, 0, W, H);
    D.rain(x, S.t, { n: o.n ?? 320, angle: o.angle ?? 0.12, speed: 1500, len: 70, color: o.color || 'rgba(225,235,245,0.7)', width: 1.5, seed: 77 });
    x.globalCompositeOperation = 'destination-in';
    const m = x.createLinearGradient(split - soft, 0, split + soft, 0);
    m.addColorStop(0, `rgba(0,0,0,${rainRight ? 0 : 1})`); m.addColorStop(1, `rgba(0,0,0,${rainRight ? 1 : 0})`);
    x.fillStyle = m; x.fillRect(0, 0, W, H); x.globalCompositeOperation = 'source-over';
    ctx.drawImage(c, 0, 0);
  } });

  // ---------------------------------------------------------------- fx: 風花 -- rain turns into snow between t0 and t1
  const kazahana = (o = {}) => ({ type: 'custom', fn: (ctx, S) => {
    const k = o.t0 == null ? 1 : E.inOutSine(Z.clamp((S.t - o.t0) / ((o.t1 ?? o.t0 + 3) - o.t0)));
    if (k < 1) D.rain(ctx, S.t, { n: 260, angle: 0.1, speed: Z.lerp(1500, 260, k), len: Z.lerp(70, 6, k),
      color: `rgba(225,235,245,${0.65 * (1 - k)})`, width: 1.5, seed: 78 });
    if (k <= 0) return;
    const n = o.n ?? 160, seed = o.seed ?? 79, t = S.t;
    ctx.save(); ctx.fillStyle = o.color || '#FFFFFF';
    for (let i = 0; i < n; i++) {
      const sp = 40 + 50 * Z.rnd(i, seed + 1), depth = 0.5 + Z.rnd(i, seed + 3);
      const y = Z.fract(Z.rnd(i, seed) + t * sp * depth / (H + 60)) * (H + 60) - 30;
      const x = Z.fract(Z.rnd(i, seed + 2) + (o.wind ?? 0.004) * t) * W + 30 * Math.sin(t * (0.6 + Z.rnd(i, seed + 4)) + i);
      const r = (1.4 + 3.2 * Z.rnd(i, seed + 5)) * depth * (o.size ?? 1);
      ctx.globalAlpha = k * (o.alpha ?? 0.9) * (0.5 + 0.5 * depth);
      ctx.beginPath(); ctx.arc(x, y, r, 0, Z.TAU); ctx.fill();
    }
    ctx.restore();
  } });

  // ---------------------------------------------------------------- fx: leaves flowing along a curve a -> b
  // a, b: [x, y]; bend: control-point offset (px, perpendicular); n, speed (path lengths per second), green share
  const leafLine = (o = {}) => ({ type: 'custom', fn: (ctx, S) => {
    const [ax, ay] = o.a, [bx, by] = o.b, n = o.n ?? 46, seed = o.seed ?? 21, speed = o.speed ?? 0.12;
    const mx = (ax + bx) / 2, my = (ay + by) / 2, len = Math.hypot(bx - ax, by - ay);
    const nx = -(by - ay) / len, ny = (bx - ax) / len, bend = o.bend ?? 220;
    const cx = mx + nx * bend, cy = my + ny * bend;
    const grow = o.at == null ? 1 : E.outCubic(Z.clamp((S.t - o.at) / (o.dur ?? 1.5)));
    for (let i = 0; i < n; i++) {
      const u = Z.fract(i / n + S.t * speed + Z.rnd(i, seed) * 0.02);
      if (u > grow) continue;
      const q = 1 - u, x = q * q * ax + 2 * q * u * cx + u * u * bx, y = q * q * ay + 2 * q * u * cy + u * u * by;
      const f = flutter(S.t, i, seed, 0.25);
      drawLeaf(ctx, leafImg(i, seed, 1 - (o.green ?? 0.08)), x + f.dx + nx * 30 * Z.rnds(i, seed + 1), y + f.dy + ny * 30 * Z.rnds(i, seed + 2),
        (o.size ?? 54) * (0.7 + 0.6 * Z.rnd(i, seed + 3)), f.rot, f.sx, Math.min(1, u * 8, (1 - u) * 8));
    }
  } });

  // ---------------------------------------------------------------- fx: the 手毬歌 as falling hand-written kana
  const songLeaves = (o = {}) => ({ type: 'custom', fn: (ctx, S) => {
    const text = o.text || 'てんてんてまり てまりうた', n = o.n ?? 26, seed = o.seed ?? 31, t = S.t;
    ctx.save(); ctx.fillStyle = o.color || INK; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    for (let i = 0; i < n; i++) {
      const sp = 70 + 50 * Z.rnd(i, seed + 1), k = Z.fract(Z.rnd(i, seed + 2) + t * sp / (H + 200));
      const f = flutter(t, i, seed, 0.8);
      const x = (o.area ? o.area[0] + Z.rnd(i, seed) * (o.area[2] - o.area[0]) : Z.rnd(i, seed) * W) + f.dx;
      const y = -100 + k * (H + 200) + f.dy;
      const ch = [...text.replace(/\s/g, '')][i % [...text.replace(/\s/g, '')].length];
      ctx.save(); ctx.translate(x, y); ctx.rotate(f.rot * 0.6); ctx.scale(f.sx, 1);
      ctx.globalAlpha = (o.alpha ?? 0.8) * Math.min(1, k * 6, (1 - k) * 6);
      D.font(ctx, (o.size ?? 54) * (0.7 + 0.6 * Z.rnd(i, seed + 3)), 'hand', 600); ctx.fillText(ch, 0, 0);
      ctx.restore();
    }
    ctx.restore();
  } });

  // ---------------------------------------------------------------- fx: watercolour rings from a point, one per beat
  const ripples = (o = {}) => ({ type: 'custom', fn: (ctx, S) => {
    const spb = S.clock.spb || 0.588, t = S.t, life = o.life ?? 2.4;
    ctx.save(); ctx.globalCompositeOperation = o.comp || 'multiply';
    for (let j = 0; j < 4; j++) {
      const born = Math.floor((t - S.shot.t0) / spb - j) * spb + S.shot.t0;
      const age = t - born; if (born < S.shot.t0 || age > life) continue;
      const k = age / life, r = (o.r0 ?? 40) + (o.r1 ?? 520) * E.outCubic(k);
      ctx.strokeStyle = Z.rgba(o.color || '#B8322A', (o.alpha ?? 0.35) * (1 - k));
      ctx.lineWidth = (o.width ?? 16) * (1 - 0.7 * k);
      ctx.beginPath(); ctx.ellipse(o.x, o.y, r, r * (o.flat ?? 0.92), 0, 0, Z.TAU); ctx.stroke();
    }
    ctx.restore();
  } });

  // ---------------------------------------------------------------- scene: つがいの楓 choreography
  // args: bg, mode 'pair' | 'part' | 'solo' | 'rise', meet (song time the pair meets the centre), gust (part: when
  // they are blown apart), cx, cy, r (orbit radius), size, color ('red' | 'green', solo), dir ('up' | 'down', solo),
  // drift: background leaves fx options or null, tint [{color, a, comp}]
  const pairPos = (a, S, which) => {          // which: 0 red (comes from the left), 1 green (from the right)
    const t = S.t, cx = a.cx ?? 960, cy = a.cy ?? 500, r = a.r ?? 120, meet = a.meet ?? S.shot.t0 + S.dur * 0.55;
    const sgn = which ? 1 : -1, w = a.spin ?? 0.9;
    const ang = w * (t - meet) + (which ? 0 : Math.PI);                      // opposite sides of the orbit
    const orbit = [cx + Math.cos(ang) * r, cy + Math.sin(ang) * r * 0.55];
    if (t < meet) {                                                            // falling in from the upper corners
      const k = E.outSine(Z.clamp((t - S.shot.t0) / (meet - S.shot.t0)));
      const start = [cx + sgn * 820, -120];
      return [Z.lerp(start[0], orbit[0], k), Z.lerp(start[1], orbit[1], k), 1, 1 - k];
    }
    return [orbit[0], orbit[1], 1, 0];
  };
  Z.scene('leaves', {
    preload: a => [a.bg, ...RED, ...GREEN].filter(Boolean),
    draw(ctx, S) {
      const a = S.args, t = S.t, mode = a.mode || 'pair', size = a.size ?? 150;
      if (a.bg) D.cover(ctx, Z.imgSync(a.bg), D.viewLerp(a.bgFrom || { zoom: 1.04 }, a.bgTo || { zoom: 1.08 }, S.p));
      else D.fill(ctx, a.color || '#F4EFE4');
      for (const tn of a.tint || []) D.fill(ctx, tn.color, tn.a ?? 0.5, tn.comp || 'multiply');
      if (a.drift) Z.fx(ctx, S, leaves(a.drift));
      const leaf = (src, x, y, i, sw) => { const f = flutter(t, i, 5, sw); drawLeaf(ctx, src, x + f.dx, y + f.dy * 0.5, size, f.rot, f.sx); };
      if (mode === 'pair' || mode === 'rise' || mode === 'part') {
        for (const which of [0, 1]) {
          let [x, y, , sw] = pairPos(a, S, which);
          if (mode === 'rise') y -= 260 * E.inOutSine(S.p);
          if (mode === 'part' && t > a.gust) {                                 // blown apart: green up and away, red down
            const k = E.inCubic(Z.clamp((t - a.gust) / (a.gustDur ?? 2.4)));
            if (which) { x += 900 * k; y -= 900 * k; }
            else { const kd = Z.clamp((t - a.gust) / (a.fallDur ?? 4.5)); x -= 160 * kd; y = Z.lerp(y, a.land ?? 960, E.outSine(kd)); }
          }
          leaf(which ? GREEN[0] : RED[0], x, y, which, 0.35 + 0.65 * sw);
        }
      } else if (mode === 'solo') {
        const up = a.dir === 'up', k = S.p;
        const x = (a.x ?? 960) + (up ? 500 : -120) * k, y = up ? Z.lerp(a.y ?? 760, -200, E.inQuad(k)) : Z.lerp(-160, a.y ?? 900, k);
        leaf(a.color === 'green' ? GREEN[0] : RED[0], x, y, 2, 1);
      }
    },
  });

  // ---------------------------------------------------------------- scene: 言えない／癒えない／消えない
  // args: words [{text, at}], melt (song time the rain starts melting them), bg, x positions per word, size
  Z.scene('iienai', {
    preload: a => [a.bg].filter(Boolean),
    async init() { await document.fonts.load('400 200px "Yuji Syuku"', '言えない癒消'); },
    draw(ctx, S) {
      const a = S.args, t = S.t, spb = S.clock.spb || 0.588, size = a.size ?? 190;
      if (a.bg) D.cover(ctx, Z.imgSync(a.bg), { zoom: 1.05 }); else D.fill(ctx, '#E8EDF0');
      D.fill(ctx, a.wash || '#8698A8', a.washA ?? 0.32, 'multiply');
      D.rain(ctx, t, { n: 140, angle: 0.08, speed: 1300, len: 54, color: 'rgba(60,75,95,0.28)', width: 1.3, seed: 81 });
      (a.words || []).forEach((w, wi) => {
        const chars = [...w.text], x = w.x ?? 960, y0 = w.y ?? (H - chars.length * size * 1.02) / 2;
        const melt = Math.max(0, t - (w.melt ?? a.melt ?? 1e9));
        chars.forEach((ch, ci) => {
          const k = Z.clamp((t - w.at - ci * spb * 0.5) / (spb * 0.45));           // one character per half beat
          if (k <= 0) return;
          const y = y0 + ci * size * 1.02 + size / 2;
          ctx.save(); ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; D.font(ctx, w.size ?? size, 'brush', 400);
          // melting: the glyph drips down in a few fading copies, the original loses ink
          const drips = melt > 0 ? 5 : 1;
          for (let d = drips - 1; d >= 0; d--) {
            const dy = melt * (60 + 40 * Z.rnd(wi, ci, d)) * d, al = d ? 0.16 * Math.max(0, 1 - melt / 2.5) : Math.max(0, 1 - melt / 2.2);
            ctx.globalAlpha = al * E.outCubic(k); ctx.fillStyle = w.color || '#33404F';
            ctx.fillText(ch, x + Z.rnds(wi, ci, d) * 6 * d, y + dy);
          }
          ctx.restore();
        });
        // the rest of the sung line, small vertical mincho to the left of the word, from two beats after it
        if (w.rest) {
          const kr = Z.clamp((t - w.at - spb * 2) / 0.6);
          if (kr > 0) {
            ctx.save(); ctx.globalAlpha = Math.max(0, 1 - melt / 2.2);
            D.vtext(ctx, w.rest, x - size * 0.78, y0 + size * 0.3, { size: 44, fam: 'mincho', weight: 500, color: w.color || '#33404F', reveal: kr });
            ctx.restore();
          }
        }
      });
    },
  });

  // ---------------------------------------------------------------- scene: 押し葉 + end card
  // args: img (opaque pressed-leaf plate), appear [t0, t1], title {at}, credits {at, lines}
  Z.scene('oshiba', {
    preload: a => [a.img, a.bg].filter(Boolean),
    async init() { await document.fonts.load('400 80px "Yuji Syuku"', Z.TITLE); await document.fonts.load('500 30px "Shippori Mincho B1"', (Z.CREDIT || '') + '制作：Claude Opus 5.5'); },
    draw(ctx, S) {
      const a = S.args, t = S.t;
      D.fill(ctx, '#FFFFFF');
      const k = a.appear ? E.inOutSine(Z.clamp((t - a.appear[0]) / (a.appear[1] - a.appear[0]))) : 1;
      if (a.img) D.cover(ctx, Z.imgSync(a.img), { zoom: 1.02 + 0.03 * S.p }, k);   // the pressed leaves seep into the white page
      const txt = (s, x, y, size, fam, w, at, color = INK) => {
        const a2 = Z.clamp((t - at) / 1.2); if (a2 <= 0) return;
        ctx.save(); ctx.globalAlpha = E.outCubic(a2) * 0.9; ctx.fillStyle = color; ctx.textAlign = 'left'; ctx.textBaseline = 'alphabetic';
        D.font(ctx, size, fam, w); ctx.fillText(s, x, y); ctx.restore();
      };
      if (a.title) { txt(Z.TITLE, 1240, 520, 92, 'brush', 400, a.title.at); txt(Z.TITLE_SUB, 1246, 572, 22, 'mincho', 500, a.title.at + 0.4, '#6E655A'); }
      if (a.credits) a.credits.lines.forEach((s, i) => txt(s, 1246, 660 + i * 44, 26, 'mincho', 500, a.credits.at + i * 0.5, '#6E655A'));
    },
  });

  Z.AK = { leaves, katashigure, kazahana, leafLine, songLeaves, ripples, RED, GREEN, INK };
})();
