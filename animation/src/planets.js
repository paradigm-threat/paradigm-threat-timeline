/**
 * Three.js planetary scene for BC / Golden Age visualization.
 * Renders simplified Saturnian collinear configuration and transitions.
 */
import * as THREE from 'three';
import { planetaryConfigs } from '../data/events.js';

let scene, camera, renderer, animationId;
let planets = {};
let plasmaParticles;
let currentConfig = null;

export function initPlanetScene(canvas) {
    scene = new THREE.Scene();

    camera = new THREE.PerspectiveCamera(60, canvas.clientWidth / canvas.clientHeight, 0.1, 1000);
    camera.position.set(0, 2, 15);
    camera.lookAt(0, 1, 0);

    renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
    renderer.setSize(canvas.clientWidth, canvas.clientHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.2;

    // Ambient light
    scene.add(new THREE.AmbientLight(0x222244, 0.5));

    // Point light (for Saturn glow effect)
    const saturnLight = new THREE.PointLight(0xffcc00, 2, 30);
    saturnLight.position.set(0, 4, 0);
    scene.add(saturnLight);
    planets.saturnLight = saturnLight;

    // Create planetary bodies
    createSaturn();
    createVenus();
    createMars();
    createEarth();
    createJupiter();
    createPlasmaField();
    createStarfield();

    // Handle resize
    window.addEventListener('resize', () => {
        const w = canvas.clientWidth;
        const h = canvas.clientHeight;
        camera.aspect = w / h;
        camera.updateProjectionMatrix();
        renderer.setSize(w, h);
    });

    // Start render loop
    animate();
}

function createSaturn() {
    const geo = new THREE.SphereGeometry(1.2, 32, 32);
    const mat = new THREE.MeshStandardMaterial({
        color: 0xffcc00,
        emissive: 0xff8800,
        emissiveIntensity: 0.8,
        roughness: 0.3,
    });
    const mesh = new THREE.Mesh(geo, mat);
    mesh.position.set(0, 4, 0);
    scene.add(mesh);
    planets.saturn = mesh;

    // Saturn glow (sprite)
    const glowTex = createGlowTexture();
    const glowMat = new THREE.SpriteMaterial({
        map: glowTex,
        color: 0xffaa00,
        transparent: true,
        opacity: 0.6,
        blending: THREE.AdditiveBlending,
    });
    const glowSprite = new THREE.Sprite(glowMat);
    glowSprite.scale.set(5, 5, 1);
    mesh.add(glowSprite);
    planets.saturnGlow = glowSprite;

    // Saturn rings (hidden by default — only in stabilization+ phases)
    const ringGeo = new THREE.RingGeometry(1.6, 2.4, 64);
    const ringMat = new THREE.MeshBasicMaterial({
        color: 0xccaa66,
        side: THREE.DoubleSide,
        transparent: true,
        opacity: 0,
    });
    const ringMesh = new THREE.Mesh(ringGeo, ringMat);
    ringMesh.rotation.x = Math.PI / 2.3;
    mesh.add(ringMesh);
    planets.saturnRings = ringMesh;
}

function createVenus() {
    // Venus as 8-pointed star plasmoid (geometry nodes approximation)
    const geo = new THREE.SphereGeometry(0.35, 8, 8);
    const mat = new THREE.MeshStandardMaterial({
        color: 0xffffff,
        emissive: 0xffffff,
        emissiveIntensity: 1.0,
        roughness: 0,
    });
    const mesh = new THREE.Mesh(geo, mat);
    mesh.position.set(0, 2, 0);
    scene.add(mesh);
    planets.venus = mesh;

    // Venus plasmoid glow
    const glowTex = createGlowTexture();
    const glowMat = new THREE.SpriteMaterial({
        map: glowTex,
        color: 0xaaccff,
        transparent: true,
        opacity: 0.5,
        blending: THREE.AdditiveBlending,
    });
    const glowSprite = new THREE.Sprite(glowMat);
    glowSprite.scale.set(2.5, 2.5, 1);
    mesh.add(glowSprite);
    planets.venusGlow = glowSprite;
}

function createMars() {
    const geo = new THREE.SphereGeometry(0.3, 16, 16);
    const mat = new THREE.MeshStandardMaterial({
        color: 0xcc3300,
        roughness: 0.7,
        metalness: 0.2,
    });
    const mesh = new THREE.Mesh(geo, mat);
    mesh.position.set(0, 0.5, 0);
    scene.add(mesh);
    planets.mars = mesh;
}

function createEarth() {
    const geo = new THREE.SphereGeometry(0.4, 24, 24);
    const mat = new THREE.MeshStandardMaterial({
        color: 0x3366cc,
        roughness: 0.5,
        metalness: 0.1,
    });
    const mesh = new THREE.Mesh(geo, mat);
    mesh.position.set(0, -1.5, 0);
    scene.add(mesh);
    planets.earth = mesh;
}

function createJupiter() {
    const geo = new THREE.SphereGeometry(0.9, 24, 24);
    const mat = new THREE.MeshStandardMaterial({
        color: 0xcc9944,
        roughness: 0.5,
        emissive: 0x442200,
        emissiveIntensity: 0.3,
    });
    const mesh = new THREE.Mesh(geo, mat);
    mesh.visible = false; // Only visible in round-table+ phases
    scene.add(mesh);
    planets.jupiter = mesh;
}

function createPlasmaField() {
    // Particle system for Absu plasma layers
    const count = 2000;
    const positions = new Float32Array(count * 3);
    const colors = new Float32Array(count * 3);

    for (let i = 0; i < count; i++) {
        const theta = Math.random() * Math.PI * 2;
        const phi = Math.random() * Math.PI;
        const r = 6 + Math.random() * 3;
        positions[i * 3] = r * Math.sin(phi) * Math.cos(theta);
        positions[i * 3 + 1] = r * Math.cos(phi);
        positions[i * 3 + 2] = r * Math.sin(phi) * Math.sin(theta);

        // Purple/blue plasma colors
        colors[i * 3] = 0.3 + Math.random() * 0.3;
        colors[i * 3 + 1] = 0.1 + Math.random() * 0.2;
        colors[i * 3 + 2] = 0.5 + Math.random() * 0.5;
    }

    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    const mat = new THREE.PointsMaterial({
        size: 0.08,
        vertexColors: true,
        transparent: true,
        opacity: 0.6,
        blending: THREE.AdditiveBlending,
        depthWrite: false,
    });

    plasmaParticles = new THREE.Points(geo, mat);
    scene.add(plasmaParticles);
}

function createStarfield() {
    const count = 5000;
    const positions = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
        positions[i * 3] = (Math.random() - 0.5) * 200;
        positions[i * 3 + 1] = (Math.random() - 0.5) * 200;
        positions[i * 3 + 2] = (Math.random() - 0.5) * 200;
    }
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    const mat = new THREE.PointsMaterial({
        size: 0.1,
        color: 0xffffff,
        transparent: true,
        opacity: 0.6,
    });
    scene.add(new THREE.Points(geo, mat));
}

function createGlowTexture() {
    const size = 128;
    const canvas = document.createElement('canvas');
    canvas.width = size;
    canvas.height = size;
    const ctx = canvas.getContext('2d');
    const gradient = ctx.createRadialGradient(size / 2, size / 2, 0, size / 2, size / 2, size / 2);
    gradient.addColorStop(0, 'rgba(255,255,255,1)');
    gradient.addColorStop(0.3, 'rgba(255,200,100,0.5)');
    gradient.addColorStop(1, 'rgba(255,100,0,0)');
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, size, size);
    return new THREE.CanvasTexture(canvas);
}

/**
 * Update the 3D scene based on the current year.
 */
export function updatePlanetScene(year) {
    const config = planetaryConfigs.find(
        c => year >= c.yearStart && year <= c.yearEnd
    );
    if (!config) return;

    currentConfig = config;

    // Sky color
    scene.background = new THREE.Color(config.skyColor);

    // Saturn
    if (config.saturn) {
        planets.saturn.visible = true;
        lerpPosition(planets.saturn, config.saturn.position);
        planets.saturnGlow.material.opacity = config.saturn.glow * 0.6;
        planets.saturnLight.intensity = config.saturn.glow * 2;
        if (config.saturn.color) {
            planets.saturn.material.color.set(config.saturn.color);
            planets.saturn.material.emissive.set(config.saturn.color);
        }
        // Rings
        planets.saturnRings.material.opacity = config.saturn.rings ? 0.5 : 0;
    }

    // Venus
    if (config.venus) {
        planets.venus.visible = true;
        lerpPosition(planets.venus, config.venus.position);
        const isPlasma = config.venus.type === 'plasmoid';
        planets.venus.material.emissiveIntensity = isPlasma ? 1.0 : 0.3;
        planets.venusGlow.material.opacity = isPlasma ? 0.5 : 0.15;
        if (config.venus.color) {
            planets.venus.material.color.set(config.venus.color);
            planets.venus.material.emissive.set(config.venus.color);
        }
    } else {
        planets.venus.visible = false;
    }

    // Mars
    if (config.mars) {
        planets.mars.visible = true;
        lerpPosition(planets.mars, config.mars.position);
    } else {
        planets.mars.visible = false;
    }

    // Earth
    if (config.earth) {
        planets.earth.visible = true;
        lerpPosition(planets.earth, config.earth.position);
        if (config.earth.color) {
            planets.earth.material.color.set(config.earth.color);
        }
    }

    // Jupiter
    if (config.jupiter) {
        planets.jupiter.visible = true;
        lerpPosition(planets.jupiter, config.jupiter.position);
    } else {
        planets.jupiter.visible = false;
    }

    // Plasma field (Absu) — visible before stabilization
    const plasmaVisible = year < -806;
    plasmaParticles.visible = plasmaVisible;
    if (plasmaVisible) {
        const intensity = Math.max(0, Math.min(1, (-year - 670) / 2477));
        plasmaParticles.material.opacity = intensity * 0.6;
    }
}

function lerpPosition(mesh, target) {
    if (!target) return;
    mesh.position.lerp(new THREE.Vector3(target[0], target[1], target[2]), 0.05);
}

function animate() {
    animationId = requestAnimationFrame(animate);

    const t = performance.now() * 0.001;

    // Gentle rotation on planets
    if (planets.saturn) planets.saturn.rotation.y += 0.002;
    if (planets.venus?.visible) planets.venus.rotation.y += 0.005;
    if (planets.mars?.visible) planets.mars.rotation.y += 0.004;
    if (planets.earth?.visible) planets.earth.rotation.y += 0.003;
    if (planets.jupiter?.visible) planets.jupiter.rotation.y += 0.001;

    // Plasma particle slow rotation
    if (plasmaParticles?.visible) {
        plasmaParticles.rotation.y += 0.0005;
        plasmaParticles.rotation.x = Math.sin(t * 0.1) * 0.05;
    }

    renderer.render(scene, camera);
}

export function getActivePlanetLabel(year) {
    const config = planetaryConfigs.find(c => year >= c.yearStart && year <= c.yearEnd);
    return config ? { label: config.label, description: config.description } : { label: '', description: '' };
}

export function destroyPlanetScene() {
    if (animationId) cancelAnimationFrame(animationId);
    renderer?.dispose();
}
