/**
 * Framework-agnostic Three.js planetary scene controller.
 *
 * Features:
 *  - Sun always visible as central reference
 *  - Venus = GREEN, Saturn = ORANGE
 *  - Full collinear column: Uranus → Neptune → Mercury → Earth → Mars → Venus → Saturn → Jupiter → Sun
 *    The column always POINTS TOWARD the Sun and orbits around it as a rigid unit
 *    Uranus is always furthest from the Sun
 *  - Three orbital styles with animated motion
 *  - Moon appears at -3147 (Earth capture) with rapid decaying orbit
 *  - Mercury, Neptune, Uranus added as column members
 *  - Orbit counting per planet per era
 */
import { planetaryConfigs } from '../../data/events.js';

let THREE = null;

const MOON_CAPTURE_YEAR = -3147;
const MOON_ORBIT_RADIUS = 0.8;

/* ── Collinear column config ──
 * The column orbits Sun at radius R in the XZ plane.
 * The column axis points radially inward (toward Sun).
 * 'dist' = distance along the column axis from the Sun.
 *   Larger dist = further from Sun.
 *
 * Order toward Sun:  Uranus → Neptune → Mercury → Earth → Mars → Venus → Saturn → Jupiter → [Sun]
 */
const COL = {
  R: 10, // orbital radius of column center around Sun
  period: 1.0,
  // dist: distance from Sun along column axis (Jupiter closest, Uranus furthest)
  jupiter: { dist: 1.5 },
  saturn:  { dist: 3.5 },
  venus:   { dist: 5.5 },
  mars:    { dist: 7.0 },
  earth:   { dist: 8.5 },
  mercury: { dist: 10.0 },
  neptune: { dist: 11.5 },
  uranus:  { dist: 13.0 },
};

/* ── Round Table config ──
 * Tilted ellipses around Jupiter (at origin). Sun visible off to side.
 */
const RT = {
  sunPos: [-10, -3, 0],
  saturn:  { rx: 5.0, ry: 3.5, tilt: 0.2,  period: 10 },
  venus:   { rx: 3.5, ry: 2.0, tilt: 0.5,  period: 0.615 },
  mars:    { rx: 3.0, ry: 2.5, tilt: -0.3, period: 1.88 },
  earth:   { rx: 2.2, ry: 1.5, tilt: -0.1, period: 1.0 },
  mercury: { rx: 1.0, ry: 0.8, tilt: 0.4,  period: 0.24 },
  neptune: { rx: 6.5, ry: 4.0, tilt: -0.2, period: 164 },
  uranus:  { rx: 6.0, ry: 3.8, tilt: 0.6,  period: 84 },
};

/* ── Modern config ──
 * Standard concentric XZ-plane circles around Sun at origin.
 */
const MOD = {
  mercury: { r: 2.0,  period: 0.24 },
  venus:   { r: 3.5,  period: 0.615 },
  earth:   { r: 5.0,  period: 1.0 },
  mars:    { r: 7.0,  period: 1.88 },
  jupiter: { r: 10.0, period: 11.86 },
  saturn:  { r: 13.0, period: 29.46 },
  uranus:  { r: 16.0, period: 84 },
  neptune: { r: 19.0, period: 164 },
};

/**
 * Create and return a PlanetController bound to the given canvas.
 * @param {HTMLCanvasElement} canvas
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
  const sunLight = new THREE.PointLight(0xffffcc, 3.0, 120);
  sunLight.position.set(0, 0, 0);
  scene.add(sunLight);
  const fillLight = new THREE.DirectionalLight(0xaabbcc, 0.6);
  fillLight.position.set(0, 5, 15);
  scene.add(fillLight);

  // ── Build scene objects ──
  const p = {};
  buildSun(scene, p, THREE);
  buildSaturn(scene, p, THREE);
  buildVenus(scene, p, THREE);
  buildMars(scene, p, THREE);
  buildEarth(scene, p, THREE);
  buildJupiter(scene, p, THREE);
  buildMercury(scene, p, THREE);
  buildNeptune(scene, p, THREE);
  buildUranus(scene, p, THREE);
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
  L.mercury = buildLabel('MERCURY', '#bbaa88', THREE);
  L.neptune = buildLabel('NEPTUNE', '#4466ff', THREE);
  L.uranus  = buildLabel('URANUS',  '#66dddd', THREE);
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
    if (p.sun) p.sun.rotation.y += 0.001;
    if (p.saturn?.visible) p.saturn.rotation.y += 0.002;
    if (p.venus?.visible) p.venus.rotation.y += 0.005;
    if (p.mars?.visible) p.mars.rotation.y += 0.004;
    if (p.earth?.visible) p.earth.rotation.y += 0.003;
    if (p.jupiter?.visible) p.jupiter.rotation.y += 0.001;
    if (p.mercury?.visible) p.mercury.rotation.y += 0.006;
    if (p.neptune?.visible) p.neptune.rotation.y += 0.001;
    if (p.uranus?.visible) p.uranus.rotation.y += 0.001;
    if (plasma?.visible) {
      plasma.rotation.y += 0.0005;
      plasma.rotation.x = Math.sin(performance.now() * 0.0001) * 0.05;
    }
    camera.position.lerp(camPosGoal, 0.03);
    camera.lookAt(camLookGoal);
    // Labels
    syncLabel(L.sun,     p.sun,     1.4, camera);
    syncLabel(L.saturn,  p.saturn,  1.8, camera);
    syncLabel(L.venus,   p.venus,   0.8, camera);
    syncLabel(L.mars,    p.mars,    0.7, camera);
    syncLabel(L.earth,   p.earth,   0.8, camera);
    syncLabel(L.jupiter, p.jupiter, 1.4, camera);
    syncLabel(L.mercury, p.mercury, 0.5, camera);
    syncLabel(L.neptune, p.neptune, 0.7, camera);
    syncLabel(L.uranus,  p.uranus,  0.7, camera);
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
      if (style === 'collinear') {
        camPosGoal.set(0, 18, 22);
        camLookGoal.set(0, 0, 0);
      } else if (style === 'roundTable') {
        camPosGoal.set(0, 10, 22);
        camLookGoal.set(0, 0, 0);
      } else if (style === 'modern') {
        camPosGoal.set(0, 30, 30);
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
      const periodDays = 10 + (27.3 - 10) * frac;
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
      orbitCounts.column = Math.abs(elapsed); // entire column orbits once per Earth year
      orbitCounts.earth  = Math.abs(elapsed);
    } else if (style === 'roundTable') {
      orbitCounts.earth   = Math.abs(elapsed);
      orbitCounts.venus   = Math.abs(elapsed / 0.615);
      orbitCounts.mars    = Math.abs(elapsed / 1.88);
      orbitCounts.saturn  = Math.abs(elapsed / 10);
      orbitCounts.mercury = Math.abs(elapsed / 0.24);
    } else if (style === 'modern') {
      orbitCounts.mercury = Math.abs(elapsed / 0.24);
      orbitCounts.venus   = Math.abs(elapsed / 0.615);
      orbitCounts.earth   = Math.abs(elapsed);
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
  // The column is a rigid bar pointing radially toward the Sun.
  // It orbits Sun at radius COL.R in the XZ plane (y=0).
  // Each planet sits along the radial direction at its 'dist' from Sun.
  function placeCollinear(elapsed, cfg) {
    const angle = (elapsed / COL.period) * Math.PI * 2;
    // Unit vector pointing from Sun toward the column (outward)
    const dx = Math.cos(angle);
    const dz = Math.sin(angle);

    p.sun.position.set(0, 0, 0);
    sunLight.position.set(0, 0, 0);

    // Helper: place planet along the radial line at distance 'dist' from Sun
    const placeOnColumn = (mesh, label, dist, show) => {
      if (show) {
        mesh.visible = true;
        if (label) label.visible = true;
        mesh.position.set(dx * dist, 0, dz * dist);
      } else {
        mesh.visible = false;
        if (label) label.visible = false;
      }
    };

    // Column order toward Sun: Uranus(far) → Neptune → Mercury → Earth → Mars → Venus → Saturn → Jupiter(near Sun)
    placeOnColumn(p.jupiter, L.jupiter, COL.jupiter.dist, true);
    placeOnColumn(p.saturn,  L.saturn,  COL.saturn.dist,  true);
    p.saturnGlow.material.opacity = (cfg.saturn?.glow || 0.5) * 0.6;
    p.saturnRings.material.opacity = cfg.saturn?.rings ? 0.5 : 0;

    placeOnColumn(p.venus,   L.venus,   COL.venus.dist,   !!cfg.venus);
    placeOnColumn(p.mars,    L.mars,    COL.mars.dist,    !!cfg.mars);
    placeOnColumn(p.earth,   L.earth,   COL.earth.dist,   !!cfg.earth);
    placeOnColumn(p.mercury, L.mercury, COL.mercury.dist, true);
    placeOnColumn(p.neptune, L.neptune, COL.neptune.dist, true);
    placeOnColumn(p.uranus,  L.uranus,  COL.uranus.dist,  true);
  }

  // ── Round Table placement (around Jupiter) ──
  function placeRoundTable(elapsed, cfg) {
    p.sun.position.set(...RT.sunPos);
    sunLight.position.set(...RT.sunPos);

    p.jupiter.visible = true; L.jupiter.visible = true;
    p.jupiter.position.set(0, 0, 0);

    const placeEllipse = (mesh, label, def, show) => {
      if (!show) { mesh.visible = false; if (label) label.visible = false; return; }
      mesh.visible = true; if (label) label.visible = true;
      const a = (elapsed / def.period) * Math.PI * 2;
      mesh.position.set(
        def.rx * Math.cos(a),
        def.ry * Math.sin(a) * Math.cos(def.tilt),
        def.ry * Math.sin(a) * Math.sin(def.tilt)
      );
    };

    placeEllipse(p.saturn,  L.saturn,  RT.saturn,  !!cfg.saturn);
    if (cfg.saturn) {
      p.saturnGlow.material.opacity = (cfg.saturn.glow || 0.3) * 0.6;
      p.saturnRings.material.opacity = cfg.saturn.rings ? 0.5 : 0;
    }
    placeEllipse(p.venus,   L.venus,   RT.venus,   !!cfg.venus);
    placeEllipse(p.mars,    L.mars,    RT.mars,    !!cfg.mars);
    placeEllipse(p.earth,   L.earth,   RT.earth,   !!cfg.earth);
    placeEllipse(p.mercury, L.mercury, RT.mercury, true);
    placeEllipse(p.neptune, L.neptune, RT.neptune, true);
    placeEllipse(p.uranus,  L.uranus,  RT.uranus,  true);
  }

  // ── Modern placement (concentric around Sun) ──
  function placeModern(elapsed, cfg) {
    p.sun.position.set(0, 0, 0);
    sunLight.position.set(0, 0, 0);

    const placeCircle = (mesh, label, def, show) => {
      if (!show) { mesh.visible = false; if (label) label.visible = false; return; }
      mesh.visible = true; if (label) label.visible = true;
      const a = (elapsed / def.period) * Math.PI * 2;
      mesh.position.set(def.r * Math.cos(a), 0, def.r * Math.sin(a));
    };

    placeCircle(p.mercury, L.mercury, MOD.mercury, true);
    placeCircle(p.venus,   L.venus,   MOD.venus,   !!cfg.venus);
    placeCircle(p.earth,   L.earth,   MOD.earth,   !!cfg.earth);
    placeCircle(p.mars,    L.mars,    MOD.mars,    !!cfg.mars);
    placeCircle(p.jupiter, L.jupiter, MOD.jupiter, !!cfg.jupiter);
    placeCircle(p.saturn,  L.saturn,  MOD.saturn,  !!cfg.saturn);
    if (cfg.saturn) {
      p.saturnGlow.material.opacity = (cfg.saturn.glow || 0.05) * 0.6;
      p.saturnRings.material.opacity = cfg.saturn.rings ? 0.5 : 0;
    }
    placeCircle(p.uranus,  L.uranus,  MOD.uranus,  true);
    placeCircle(p.neptune, L.neptune, MOD.neptune, true);
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
    // Mercury, Neptune, Uranus — hide in chaotic phases
    p.mercury.visible = false; L.mercury.visible = false;
    p.neptune.visible = false; L.neptune.visible = false;
    p.uranus.visible = false;  L.uranus.visible = false;
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
    { ...RT.saturn,  color: 0xff8833 },
    { ...RT.venus,   color: 0x33ff77 },
    { ...RT.mars,    color: 0xff6644 },
    { ...RT.earth,   color: 0x66aaff },
    { ...RT.mercury, color: 0xbbaa88 },
    { ...RT.neptune, color: 0x4466ff },
    { ...RT.uranus,  color: 0x66dddd },
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
    { r: MOD.mercury.r, color: 0xbbaa88 },
    { r: MOD.venus.r,   color: 0x33ff77 },
    { r: MOD.earth.r,   color: 0x66aaff },
    { r: MOD.mars.r,    color: 0xff6644 },
    { r: MOD.jupiter.r, color: 0xffaa44 },
    { r: MOD.saturn.r,  color: 0xff8833 },
    { r: MOD.uranus.r,  color: 0x66dddd },
    { r: MOD.neptune.r, color: 0x4466ff },
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

// ── Glow texture ──
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

function buildMercury(scene, p, THREE) {
  const mesh = new THREE.Mesh(
    new THREE.SphereGeometry(0.2, 16, 16),
    new THREE.MeshStandardMaterial({
      color: 0xbbaa88, emissive: 0x887755, emissiveIntensity: 0.4, roughness: 0.7,
    })
  );
  mesh.visible = false;
  scene.add(mesh);
  p.mercury = mesh;
  const glow = new THREE.Sprite(new THREE.SpriteMaterial({
    map: glowTex(0xbbaa88, THREE), color: 0xbbaa88,
    transparent: true, opacity: 0.2, blending: THREE.AdditiveBlending,
  }));
  glow.scale.set(1.0, 1.0, 1);
  mesh.add(glow);
}

function buildNeptune(scene, p, THREE) {
  const mesh = new THREE.Mesh(
    new THREE.SphereGeometry(0.5, 20, 20),
    new THREE.MeshStandardMaterial({
      color: 0x4466ff, emissive: 0x2233aa, emissiveIntensity: 0.5, roughness: 0.4,
    })
  );
  mesh.visible = false;
  scene.add(mesh);
  p.neptune = mesh;
  const glow = new THREE.Sprite(new THREE.SpriteMaterial({
    map: glowTex(0x4466ff, THREE), color: 0x4466ff,
    transparent: true, opacity: 0.25, blending: THREE.AdditiveBlending,
  }));
  glow.scale.set(2, 2, 1);
  mesh.add(glow);
}

function buildUranus(scene, p, THREE) {
  const mesh = new THREE.Mesh(
    new THREE.SphereGeometry(0.5, 20, 20),
    new THREE.MeshStandardMaterial({
      color: 0x66dddd, emissive: 0x44aaaa, emissiveIntensity: 0.5, roughness: 0.4,
    })
  );
  mesh.visible = false;
  scene.add(mesh);
  p.uranus = mesh;
  const glow = new THREE.Sprite(new THREE.SpriteMaterial({
    map: glowTex(0x66dddd, THREE), color: 0x66dddd,
    transparent: true, opacity: 0.25, blending: THREE.AdditiveBlending,
  }));
  glow.scale.set(2, 2, 1);
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
