/**
 * Framework-agnostic Three.js planetary scene controller.
 * Accepts a canvas element — no hardcoded DOM ids.
 *
 * Features:
 *  - Sun always visible as central reference
 *  - Venus = GREEN, Saturn = ORANGE
 *  - Text label sprites per planet
 *  - Three orbital styles with animated motion:
 *      Collinear (Golden Age): stack orbits Sun as a group
 *      Round Table (Jupiter era): tilted ellipses around Jupiter
 *      Modern (stabilization+): concentric orbits around Sun
 *  - Moon appears at -3147 (Earth capture) with rapid decaying orbit
 *  - Orbit counting per planet per era
 */
import { planetaryConfigs } from '../../data/events.js';

let THREE = null;

const MOON_CAPTURE_YEAR = -3147;
const MOON_ORBIT_RADIUS = 0.8;

/* ── Collinear config ──
 * Entire vertical stack orbits Sun at radius R.
 * dy = height offset within stack. wr/wp = wobble radius/period.
 */
const COL = {
  R: 8,
  period: 1.0,
  saturn: { dy: 5,   wr: 0,    wp: Infinity },
  venus:  { dy: 3,   wr: 0.3,  wp: 0.615 },
  mars:   { dy: 1.5, wr: 0.2,  wp: 1.88 },
  earth:  { dy: 0,   wr: 0.15, wp: 1.0 },
};

/* ── Round Table config ──
 * Tilted ellipses around Jupiter (at origin). Sun visible off to side.
 */
const RT = {
  sunPos: [-8, -3, 0],
  saturn: { rx: 5.0, ry: 3.5, tilt: 0.2,  period: 10 },
  venus:  { rx: 3.5, ry: 2.0, tilt: 0.5,  period: 0.615 },
  mars:   { rx: 3.0, ry: 2.5, tilt: -0.3, period: 1.88 },
  earth:  { rx: 2.2, ry: 1.5, tilt: -0.1, period: 1.0 },
};

/* ── Modern config ──
 * Standard concentric XZ-plane circles around Sun at origin.
 */
const MOD = {
  venus:   { r: 3.5,  period: 0.615 },
  earth:   { r: 5.0,  period: 1.0 },
  mars:    { r: 7.0,  period: 1.88 },
  jupiter: { r: 10.0, period: 11.86 },
  saturn:  { r: 13.0, period: 29.46 },
};

/**
 * Create and return a PlanetController bound to the given canvas.
 * @param {HTMLCanvasElement} canvas
 * @returns {Promise<{setYear:Function, getPhaseInfo:Function, getOrbitInfo:Function, destroy:Function}>}
 */
export async function createPlanetController(canvas) {
  if (!THREE) THREE = await import('three');

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(
    60, canvas.clientWidth / canvas.clientHeight, 0.1, 1000
  );
  camera.position.set(0, 10, 25);
  camera.lookAt(0, 2, 0);

  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
  renderer.setSize(canvas.clientWidth, canvas.clientHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.4;

  // ── Lighting ──
  scene.add(new THREE.AmbientLight(0x8899bb, 1.4));
  const sunLight = new THREE.PointLight(0xffffcc, 3.0, 100);
  sunLight.position.set(0, 0, 0);
  scene.add(sunLight);
  const fillLight = new THREE.DirectionalLight(0xaabbcc, 0.6);
  fillLight.position.set(0, 5, 15);
  scene.add(fillLight);

  // ── Build scene objects ──
  const p = {}; // planet meshes
  buildSun(scene, p, THREE);
  buildSaturn(scene, p, THREE);
  buildVenus(scene, p, THREE);
  buildMars(scene, p, THREE);
  buildEarth(scene, p, THREE);
  buildJupiter(scene, p, THREE);
  buildMoon(scene, p, THREE);
  const plasma = buildPlasmaField(scene, THREE);
  buildStarfield(scene, THREE);

  // ── Labels ──
  const L = {};
  L.sun     = buildLabel('SUN',     '#ffffaa', THREE);
  L.saturn  = buildLabel('SATURN',  '#ff8833', THREE);
  L.venus   = buildLabel('VENUS',   '#33ff77', THREE);
  L.mars    = buildLabel('MARS',    '#ff6644', THREE);
  L.earth   = buildLabel('EARTH',   '#66aaff', THREE);
  L.jupiter = buildLabel('JUPITER', '#ffaa44', THREE);
  L.moon    = buildLabel('MOON',    '#cccccc', THREE);
  Object.values(L).forEach(s => scene.add(s));

  // ── Orbital path lines (static geometry) ──
  const oLines = {};
  oLines.collinear  = buildCollinearPaths(scene, THREE);
  oLines.roundTable = buildRoundTablePaths(scene, THREE);
  oLines.modern     = buildModernPaths(scene, THREE);
  setGroupVis(oLines.collinear, false);
  setGroupVis(oLines.roundTable, false);
  setGroupVis(oLines.modern, false);

  // ── State ──
  let currentYear = -5000;
  let curStyle = '';
  let orbitCounts = {};
  let animId = null;

  // Smooth camera targets
  let camPosGoal = new THREE.Vector3(0, 10, 25);
  let camLookGoal = new THREE.Vector3(0, 2, 0);

  // ── Resize ──
  const onResize = () => {
    const w = canvas.clientWidth, h = canvas.clientHeight;
    if (!w || !h) return;
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    renderer.setSize(w, h);
  };
  window.addEventListener('resize', onResize);

  // ── Render loop ──
  function animate() {
    animId = requestAnimationFrame(animate);
    // Self-rotation
    if (p.sun) p.sun.rotation.y += 0.001;
    if (p.saturn?.visible) p.saturn.rotation.y += 0.002;
    if (p.venus?.visible) p.venus.rotation.y += 0.005;
    if (p.mars?.visible) p.mars.rotation.y += 0.004;
    if (p.earth?.visible) p.earth.rotation.y += 0.003;
    if (p.jupiter?.visible) p.jupiter.rotation.y += 0.001;
    if (plasma?.visible) {
      plasma.rotation.y += 0.0005;
      plasma.rotation.x = Math.sin(performance.now() * 0.0001) * 0.05;
    }
    // Smooth camera
    camera.position.lerp(camPosGoal, 0.03);
    camera.lookAt(camLookGoal);
    // Labels
    syncLabel(L.sun,     p.sun,     1.4, camera);
    syncLabel(L.saturn,  p.saturn,  1.8, camera);
    syncLabel(L.venus,   p.venus,   0.8, camera);
    syncLabel(L.mars,    p.mars,    0.7, camera);
    syncLabel(L.earth,   p.earth,   0.8, camera);
    syncLabel(L.jupiter, p.jupiter, 1.4, camera);
    syncLabel(L.moon,    p.moon,    0.4, camera);
    renderer.render(scene, camera);
  }
  animate();

  // ═══════════════════ Public API ═══════════════════

  function setYear(year) {
    currentYear = year;
    const cfg = planetaryConfigs.find(c => year >= c.yearStart && year <= c.yearEnd);
    if (!cfg) return;

    scene.background = new THREE.Color(cfg.skyColor);
    const yl = cfg.yearLength || 365;
    const elapsed = year - cfg.yearStart;

    // ── Determine orbital style ──
    let style = 'none';
    if (cfg.id === 'golden-age') style = 'collinear';
    else if (cfg.id === 'round-table') style = 'roundTable';
    else if (cfg.id === 'stabilization' || cfg.id === 'modern-solar') style = 'modern';

    if (style !== curStyle) {
      setGroupVis(oLines.collinear,  style === 'collinear');
      setGroupVis(oLines.roundTable, style === 'roundTable');
      setGroupVis(oLines.modern,     style === 'modern');
      curStyle = style;
      // Camera targets per style
      if (style === 'collinear') {
        camPosGoal.set(0, 12, 26);
        camLookGoal.set(0, 2, 0);
      } else if (style === 'roundTable') {
        camPosGoal.set(0, 8, 20);
        camLookGoal.set(0, 0, 0);
      } else if (style === 'modern') {
        camPosGoal.set(0, 24, 24);
        camLookGoal.set(0, 0, 0);
      } else {
        camPosGoal.set(0, 8, 22);
        camLookGoal.set(0, 1, 0);
      }
    }

    // ── Sun always visible ──
    p.sun.visible = true;
    L.sun.visible = true;

    // ── Position by style ──
    if (style === 'collinear')       placeCollinear(elapsed, cfg);
    else if (style === 'roundTable') placeRoundTable(elapsed, cfg);
    else if (style === 'modern')     placeModern(elapsed, cfg);
    else                             placeFallback(cfg);

    // ── Moon ──
    if (year >= MOON_CAPTURE_YEAR && p.earth.visible) {
      p.moon.visible = true;
      L.moon.visible = true;
      const frac = Math.min(1, (year - MOON_CAPTURE_YEAR) / (-670 - MOON_CAPTURE_YEAR));
      const periodDays = 10 + (27.3 - 10) * frac; // rapid → modern
      const daysElapsed = (year - MOON_CAPTURE_YEAR) * yl;
      const moonAngle = (daysElapsed / periodDays) * Math.PI * 2;
      p.moon.position.set(
        p.earth.position.x + MOON_ORBIT_RADIUS * Math.cos(moonAngle),
        p.earth.position.y + MOON_ORBIT_RADIUS * Math.sin(moonAngle) * 0.25,
        p.earth.position.z + MOON_ORBIT_RADIUS * Math.sin(moonAngle)
      );
    } else {
      p.moon.visible = false;
      L.moon.visible = false;
    }

    // ── Plasma field (Absu) ──
    plasma.visible = (year < -806);
    if (plasma.visible) {
      plasma.material.opacity = Math.max(0, Math.min(1, (-year - 670) / 2477)) * 0.6;
    }

    // ── Orbit counts ──
    orbitCounts = {};
    if (style === 'collinear') {
      orbitCounts.earth  = Math.abs(elapsed);
      orbitCounts.venus  = Math.abs(elapsed / 0.615);
      orbitCounts.mars   = Math.abs(elapsed / 1.88);
    } else if (style === 'roundTable') {
      orbitCounts.earth  = Math.abs(elapsed);
      orbitCounts.venus  = Math.abs(elapsed / 0.615);
      orbitCounts.mars   = Math.abs(elapsed / 1.88);
      orbitCounts.saturn = Math.abs(elapsed / 10);
    } else if (style === 'modern') {
      orbitCounts.earth   = Math.abs(elapsed);
      orbitCounts.venus   = Math.abs(elapsed / 0.615);
      orbitCounts.mars    = Math.abs(elapsed / 1.88);
      orbitCounts.jupiter = Math.abs(elapsed / 11.86);
      orbitCounts.saturn  = Math.abs(elapsed / 29.46);
    }
    if (year >= MOON_CAPTURE_YEAR) {
      const frac = Math.min(1, (year - MOON_CAPTURE_YEAR) / (-670 - MOON_CAPTURE_YEAR));
      const periodDays = 10 + (27.3 - 10) * frac;
      orbitCounts.moon = Math.abs((year - MOON_CAPTURE_YEAR) * yl / periodDays);
    }
  }

  // ── Collinear placement ──
  function placeCollinear(elapsed, cfg) {
    const baseA = (elapsed / COL.period) * Math.PI * 2;
    const bx = COL.R * Math.cos(baseA);
    const bz = COL.R * Math.sin(baseA);

    // Sun at origin
    p.sun.position.set(0, 0, 0);
    sunLight.position.set(0, 0, 0);

    // Saturn — top of stack
    p.saturn.visible = true; L.saturn.visible = true;
    p.saturn.position.set(bx, COL.saturn.dy, bz);
    p.saturnGlow.material.opacity = (cfg.saturn?.glow || 0.5) * 0.6;
    p.saturnRings.material.opacity = cfg.saturn?.rings ? 0.5 : 0;

    // Venus
    if (cfg.venus) {
      p.venus.visible = true; L.venus.visible = true;
      const wa = (elapsed / COL.venus.wp) * Math.PI * 2;
      p.venus.position.set(
        bx + COL.venus.wr * Math.cos(wa), COL.venus.dy,
        bz + COL.venus.wr * Math.sin(wa)
      );
    } else { p.venus.visible = false; L.venus.visible = false; }

    // Mars
    if (cfg.mars) {
      p.mars.visible = true; L.mars.visible = true;
      const wa = (elapsed / COL.mars.wp) * Math.PI * 2;
      p.mars.position.set(
        bx + COL.mars.wr * Math.cos(wa), COL.mars.dy,
        bz + COL.mars.wr * Math.sin(wa)
      );
    } else { p.mars.visible = false; L.mars.visible = false; }

    // Earth
    if (cfg.earth) {
      p.earth.visible = true; L.earth.visible = true;
      const wa = (elapsed / COL.earth.wp) * Math.PI * 2;
      p.earth.position.set(
        bx + COL.earth.wr * Math.cos(wa), COL.earth.dy,
        bz + COL.earth.wr * Math.sin(wa)
      );
    } else { p.earth.visible = false; L.earth.visible = false; }

    // Jupiter not present in collinear
    p.jupiter.visible = false; L.jupiter.visible = false;
  }

  // ── Round Table placement (around Jupiter) ──
  function placeRoundTable(elapsed, cfg) {
    p.sun.position.set(...RT.sunPos);
    sunLight.position.set(...RT.sunPos);

    // Jupiter at center
    p.jupiter.visible = true; L.jupiter.visible = true;
    p.jupiter.position.set(0, 0, 0);

    // Saturn
    if (cfg.saturn) {
      p.saturn.visible = true; L.saturn.visible = true;
      const a = (elapsed / RT.saturn.period) * Math.PI * 2;
      p.saturn.position.set(
        RT.saturn.rx * Math.cos(a),
        RT.saturn.ry * Math.sin(a) * Math.cos(RT.saturn.tilt),
        RT.saturn.ry * Math.sin(a) * Math.sin(RT.saturn.tilt)
      );
      p.saturnGlow.material.opacity = (cfg.saturn.glow || 0.3) * 0.6;
      p.saturnRings.material.opacity = cfg.saturn.rings ? 0.5 : 0;
    }

    // Venus
    if (cfg.venus) {
      p.venus.visible = true; L.venus.visible = true;
      const a = (elapsed / RT.venus.period) * Math.PI * 2;
      p.venus.position.set(
        RT.venus.rx * Math.cos(a),
        RT.venus.ry * Math.sin(a) * Math.cos(RT.venus.tilt),
        RT.venus.ry * Math.sin(a) * Math.sin(RT.venus.tilt)
      );
    } else { p.venus.visible = false; L.venus.visible = false; }

    // Mars
    if (cfg.mars) {
      p.mars.visible = true; L.mars.visible = true;
      const a = (elapsed / RT.mars.period) * Math.PI * 2;
      p.mars.position.set(
        RT.mars.rx * Math.cos(a),
        RT.mars.ry * Math.sin(a) * Math.cos(RT.mars.tilt),
        RT.mars.ry * Math.sin(a) * Math.sin(RT.mars.tilt)
      );
    } else { p.mars.visible = false; L.mars.visible = false; }

    // Earth
    if (cfg.earth) {
      p.earth.visible = true; L.earth.visible = true;
      const a = (elapsed / RT.earth.period) * Math.PI * 2;
      p.earth.position.set(
        RT.earth.rx * Math.cos(a),
        RT.earth.ry * Math.sin(a) * Math.cos(RT.earth.tilt),
        RT.earth.ry * Math.sin(a) * Math.sin(RT.earth.tilt)
      );
    } else { p.earth.visible = false; L.earth.visible = false; }
  }

  // ── Modern placement (concentric around Sun) ──
  function placeModern(elapsed, cfg) {
    p.sun.position.set(0, 0, 0);
    sunLight.position.set(0, 0, 0);

    if (cfg.venus) {
      p.venus.visible = true; L.venus.visible = true;
      const a = (elapsed / MOD.venus.period) * Math.PI * 2;
      p.venus.position.set(MOD.venus.r * Math.cos(a), 0, MOD.venus.r * Math.sin(a));
    } else { p.venus.visible = false; L.venus.visible = false; }

    if (cfg.earth) {
      p.earth.visible = true; L.earth.visible = true;
      const a = (elapsed / MOD.earth.period) * Math.PI * 2;
      p.earth.position.set(MOD.earth.r * Math.cos(a), 0, MOD.earth.r * Math.sin(a));
    } else { p.earth.visible = false; L.earth.visible = false; }

    if (cfg.mars) {
      p.mars.visible = true; L.mars.visible = true;
      const a = (elapsed / MOD.mars.period) * Math.PI * 2;
      p.mars.position.set(MOD.mars.r * Math.cos(a), 0, MOD.mars.r * Math.sin(a));
    } else { p.mars.visible = false; L.mars.visible = false; }

    if (cfg.jupiter) {
      p.jupiter.visible = true; L.jupiter.visible = true;
      const a = (elapsed / MOD.jupiter.period) * Math.PI * 2;
      p.jupiter.position.set(MOD.jupiter.r * Math.cos(a), 0, MOD.jupiter.r * Math.sin(a));
    } else { p.jupiter.visible = false; L.jupiter.visible = false; }

    if (cfg.saturn) {
      p.saturn.visible = true; L.saturn.visible = true;
      const a = (elapsed / MOD.saturn.period) * Math.PI * 2;
      p.saturn.position.set(MOD.saturn.r * Math.cos(a), 0, MOD.saturn.r * Math.sin(a));
      p.saturnGlow.material.opacity = (cfg.saturn.glow || 0.05) * 0.6;
      p.saturnRings.material.opacity = cfg.saturn.rings ? 0.5 : 0;
    }
  }

  // ── Fallback: transitional / chaotic phases ──
  function placeFallback(cfg) {
    p.sun.position.set(0, -3, -5);
    sunLight.position.set(0, -3, -5);

    const lerp = (mesh, pos) => {
      if (!pos) return;
      mesh.position.lerp(new THREE.Vector3(pos[0], pos[1], pos[2]), 0.05);
    };

    if (cfg.saturn) {
      p.saturn.visible = true; L.saturn.visible = true;
      lerp(p.saturn, cfg.saturn.position);
      p.saturnGlow.material.opacity = (cfg.saturn.glow || 0.3) * 0.6;
      p.saturnRings.material.opacity = cfg.saturn.rings ? 0.5 : 0;
    }
    if (cfg.venus)   { p.venus.visible = true; L.venus.visible = true; lerp(p.venus, cfg.venus.position); }
    else             { p.venus.visible = false; L.venus.visible = false; }
    if (cfg.mars)    { p.mars.visible = true; L.mars.visible = true; lerp(p.mars, cfg.mars.position); }
    else             { p.mars.visible = false; L.mars.visible = false; }
    if (cfg.earth)   { p.earth.visible = true; L.earth.visible = true; lerp(p.earth, cfg.earth.position); }
    else             { p.earth.visible = false; L.earth.visible = false; }
    if (cfg.jupiter) { p.jupiter.visible = true; L.jupiter.visible = true; lerp(p.jupiter, cfg.jupiter.position); }
    else             { p.jupiter.visible = false; L.jupiter.visible = false; }
  }

  function getPhaseInfo() {
    const c = planetaryConfigs.find(c => currentYear >= c.yearStart && currentYear <= c.yearEnd);
    return c ? { label: c.label, description: c.description } : { label: '', description: '' };
  }

  function getOrbitInfo() { return { ...orbitCounts }; }

  function destroy() {
    if (animId) cancelAnimationFrame(animId);
    window.removeEventListener('resize', onResize);
    renderer.dispose();
  }

  return { setYear, getPhaseInfo, getOrbitInfo, destroy };
}

// ═══════════════════ Helper Functions ═══════════════════

// ── Label builder ──
function buildLabel(text, color, THREE) {
  const c = document.createElement('canvas');
  const ctx = c.getContext('2d');
  c.width = 256; c.height = 64;
  ctx.clearRect(0, 0, c.width, c.height);
  ctx.font = 'bold 48px Arial, sans-serif';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.shadowColor = 'rgba(0,0,0,0.8)';
  ctx.shadowBlur = 6;
  ctx.fillStyle = color;
  ctx.fillText(text, c.width / 2, c.height / 2);
  const tex = new THREE.CanvasTexture(c);
  tex.minFilter = THREE.LinearFilter;
  const sprite = new THREE.Sprite(new THREE.SpriteMaterial({
    map: tex, transparent: true, depthTest: false,
  }));
  sprite.scale.set(2.5, 0.6, 1);
  sprite.visible = false;
  return sprite;
}

function syncLabel(label, mesh, offset, camera) {
  if (!label?.visible || !mesh?.visible) return;
  label.position.set(mesh.position.x, mesh.position.y + offset, mesh.position.z);
  label.quaternion.copy(camera.quaternion);
}

// ── Orbital path line builders ──

function makeLine(pts, color, opacity, THREE) {
  const geo = new THREE.BufferGeometry().setFromPoints(pts);
  const mat = new THREE.LineBasicMaterial({ color, transparent: true, opacity, depthWrite: false });
  return new THREE.Line(geo, mat);
}

function setGroupVis(group, vis) {
  if (Array.isArray(group)) group.forEach(l => { l.visible = vis; });
  else if (group) group.visible = vis;
}

/** Collinear: single orbit circle at radius COL.R in XZ plane */
function buildCollinearPaths(scene, THREE) {
  const pts = [];
  for (let i = 0; i <= 96; i++) {
    const a = (i / 96) * Math.PI * 2;
    pts.push(new THREE.Vector3(COL.R * Math.cos(a), 0, COL.R * Math.sin(a)));
  }
  const line = makeLine(pts, 0xff8833, 0.3, THREE);
  scene.add(line);
  return [line];
}

/** Round Table: tilted ellipses around origin (Jupiter) */
function buildRoundTablePaths(scene, THREE) {
  const lines = [];
  const defs = [
    { ...RT.saturn, color: 0xff8833 },
    { ...RT.venus,  color: 0x33ff77 },
    { ...RT.mars,   color: 0xff6644 },
    { ...RT.earth,  color: 0x66aaff },
  ];
  for (const d of defs) {
    const pts = [];
    for (let i = 0; i <= 80; i++) {
      const a = (i / 80) * Math.PI * 2;
      pts.push(new THREE.Vector3(
        d.rx * Math.cos(a),
        d.ry * Math.sin(a) * Math.cos(d.tilt),
        d.ry * Math.sin(a) * Math.sin(d.tilt)
      ));
    }
    const line = makeLine(pts, d.color, 0.25, THREE);
    scene.add(line);
    lines.push(line);
  }
  return lines;
}

/** Modern: concentric circles in XZ plane */
function buildModernPaths(scene, THREE) {
  const lines = [];
  const defs = [
    { r: MOD.venus.r,   color: 0x33ff77 },
    { r: MOD.earth.r,   color: 0x66aaff },
    { r: MOD.mars.r,    color: 0xff6644 },
    { r: MOD.jupiter.r, color: 0xffaa44 },
    { r: MOD.saturn.r,  color: 0xff8833 },
  ];
  for (const d of defs) {
    const pts = [];
    for (let i = 0; i <= 96; i++) {
      const a = (i / 96) * Math.PI * 2;
      pts.push(new THREE.Vector3(d.r * Math.cos(a), 0, d.r * Math.sin(a)));
    }
    const line = makeLine(pts, d.color, 0.25, THREE);
    scene.add(line);
    lines.push(line);
  }
  return lines;
}

// ── Glow texture helper ──
function glowTex(color, THREE) {
  const sz = 128;
  const c = document.createElement('canvas');
  c.width = sz; c.height = sz;
  const ctx = c.getContext('2d');
  const tmp = new THREE.Color(color);
  const r = Math.round(tmp.r * 255), g = Math.round(tmp.g * 255), b = Math.round(tmp.b * 255);
  const grad = ctx.createRadialGradient(sz/2, sz/2, 0, sz/2, sz/2, sz/2);
  grad.addColorStop(0, `rgba(${r},${g},${b},1)`);
  grad.addColorStop(0.3, `rgba(${r},${g},${b},0.5)`);
  grad.addColorStop(1, `rgba(${r},${g},${b},0)`);
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, sz, sz);
  return new THREE.CanvasTexture(c);
}

// ── Scene Builders ──

function buildSun(scene, p, THREE) {
  const mesh = new THREE.Mesh(
    new THREE.SphereGeometry(0.8, 32, 32),
    new THREE.MeshStandardMaterial({
      color: 0xffffcc, emissive: 0xffdd44, emissiveIntensity: 1.5, roughness: 0,
    })
  );
  mesh.position.set(0, 0, 0);
  scene.add(mesh);
  p.sun = mesh;

  const glow = new THREE.Sprite(new THREE.SpriteMaterial({
    map: glowTex(0xffdd44, THREE), color: 0xffdd44,
    transparent: true, opacity: 0.7, blending: THREE.AdditiveBlending,
  }));
  glow.scale.set(5, 5, 1);
  mesh.add(glow);
}

function buildSaturn(scene, p, THREE) {
  const mesh = new THREE.Mesh(
    new THREE.SphereGeometry(1.2, 32, 32),
    new THREE.MeshStandardMaterial({
      color: 0xff8833, emissive: 0xcc6622, emissiveIntensity: 0.8, roughness: 0.3,
    })
  );
  mesh.position.set(0, 5, 0);
  scene.add(mesh);
  p.saturn = mesh;

  const glow = new THREE.Sprite(new THREE.SpriteMaterial({
    map: glowTex(0xff8833, THREE), color: 0xff8833,
    transparent: true, opacity: 0.6, blending: THREE.AdditiveBlending,
  }));
  glow.scale.set(5, 5, 1);
  mesh.add(glow);
  p.saturnGlow = glow;

  const ring = new THREE.Mesh(
    new THREE.RingGeometry(1.6, 2.4, 64),
    new THREE.MeshBasicMaterial({ color: 0xccaa66, side: THREE.DoubleSide, transparent: true, opacity: 0 })
  );
  ring.rotation.x = Math.PI / 2.3;
  mesh.add(ring);
  p.saturnRings = ring;
}

function buildVenus(scene, p, THREE) {
  const mesh = new THREE.Mesh(
    new THREE.SphereGeometry(0.4, 16, 16),
    new THREE.MeshStandardMaterial({
      color: 0x33ff77, emissive: 0x22cc55, emissiveIntensity: 1.0, roughness: 0,
    })
  );
  mesh.position.set(0, 3, 0);
  scene.add(mesh);
  p.venus = mesh;

  const glow = new THREE.Sprite(new THREE.SpriteMaterial({
    map: glowTex(0x33ff77, THREE), color: 0x33ff77,
    transparent: true, opacity: 0.5, blending: THREE.AdditiveBlending,
  }));
  glow.scale.set(3, 3, 1);
  mesh.add(glow);
  p.venusGlow = glow;
}

function buildMars(scene, p, THREE) {
  const mesh = new THREE.Mesh(
    new THREE.SphereGeometry(0.35, 16, 16),
    new THREE.MeshStandardMaterial({
      color: 0xff4422, emissive: 0xcc3300, emissiveIntensity: 0.6,
      roughness: 0.6, metalness: 0.2,
    })
  );
  mesh.position.set(0, 1.5, 0);
  scene.add(mesh);
  p.mars = mesh;

  const glow = new THREE.Sprite(new THREE.SpriteMaterial({
    map: glowTex(0xff4422, THREE), color: 0xff4422,
    transparent: true, opacity: 0.25, blending: THREE.AdditiveBlending,
  }));
  glow.scale.set(1.5, 1.5, 1);
  mesh.add(glow);
}

function buildEarth(scene, p, THREE) {
  const mesh = new THREE.Mesh(
    new THREE.SphereGeometry(0.45, 24, 24),
    new THREE.MeshStandardMaterial({
      color: 0x4488ff, emissive: 0x2244aa, emissiveIntensity: 0.5,
      roughness: 0.4, metalness: 0.1,
    })
  );
  mesh.position.set(0, 0, 0);
  scene.add(mesh);
  p.earth = mesh;

  const glow = new THREE.Sprite(new THREE.SpriteMaterial({
    map: glowTex(0x4488ff, THREE), color: 0x4488ff,
    transparent: true, opacity: 0.2, blending: THREE.AdditiveBlending,
  }));
  glow.scale.set(1.8, 1.8, 1);
  mesh.add(glow);
}

function buildJupiter(scene, p, THREE) {
  const mesh = new THREE.Mesh(
    new THREE.SphereGeometry(0.9, 24, 24),
    new THREE.MeshStandardMaterial({
      color: 0xddaa44, emissive: 0x886622, emissiveIntensity: 0.5, roughness: 0.5,
    })
  );
  mesh.visible = false;
  scene.add(mesh);
  p.jupiter = mesh;

  const glow = new THREE.Sprite(new THREE.SpriteMaterial({
    map: glowTex(0xddaa44, THREE), color: 0xddaa44,
    transparent: true, opacity: 0.3, blending: THREE.AdditiveBlending,
  }));
  glow.scale.set(3, 3, 1);
  mesh.add(glow);
}

function buildMoon(scene, p, THREE) {
  const mesh = new THREE.Mesh(
    new THREE.SphereGeometry(0.15, 16, 16),
    new THREE.MeshStandardMaterial({
      color: 0xbbbbbb, emissive: 0x666666, emissiveIntensity: 0.3, roughness: 0.8,
    })
  );
  mesh.visible = false;
  scene.add(mesh);
  p.moon = mesh;

  const glow = new THREE.Sprite(new THREE.SpriteMaterial({
    map: glowTex(0xaaaaaa, THREE), color: 0xaaaaaa,
    transparent: true, opacity: 0.15, blending: THREE.AdditiveBlending,
  }));
  glow.scale.set(0.6, 0.6, 1);
  mesh.add(glow);
}

function buildPlasmaField(scene, THREE) {
  const count = 2000;
  const pos = new Float32Array(count * 3);
  const col = new Float32Array(count * 3);
  for (let i = 0; i < count; i++) {
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.random() * Math.PI;
    const r = 6 + Math.random() * 3;
    pos[i*3]   = r * Math.sin(phi) * Math.cos(theta);
    pos[i*3+1] = r * Math.cos(phi);
    pos[i*3+2] = r * Math.sin(phi) * Math.sin(theta);
    col[i*3]   = 0.3 + Math.random() * 0.3;
    col[i*3+1] = 0.1 + Math.random() * 0.2;
    col[i*3+2] = 0.5 + Math.random() * 0.5;
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(col, 3));
  const mat = new THREE.PointsMaterial({
    size: 0.08, vertexColors: true, transparent: true, opacity: 0.6,
    blending: THREE.AdditiveBlending, depthWrite: false,
  });
  const pts = new THREE.Points(geo, mat);
  scene.add(pts);
  return pts;
}

function buildStarfield(scene, THREE) {
  const count = 5000;
  const pos = new Float32Array(count * 3);
  for (let i = 0; i < count; i++) {
    pos[i*3]   = (Math.random() - 0.5) * 200;
    pos[i*3+1] = (Math.random() - 0.5) * 200;
    pos[i*3+2] = (Math.random() - 0.5) * 200;
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  scene.add(new THREE.Points(geo, new THREE.PointsMaterial({
    size: 0.1, color: 0xffffff, transparent: true, opacity: 0.6,
  })));
}
