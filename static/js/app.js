// Survivor Bot - Main JavaScript

// Torch cursor fire — gentle flame that burns around the cursor like a torch
(function() {
    if ('ontouchstart' in window) return;

    const canvas = document.createElement('canvas');
    canvas.id = 'torch-canvas';
    document.body.appendChild(canvas);
    const ctx = canvas.getContext('2d');

    const glow = document.createElement('div');
    glow.id = 'torch-glow';
    glow.style.opacity = '0';
    document.body.appendChild(glow);

    function resize() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener('resize', resize);

    let mouseX = -200, mouseY = -200;
    let mouseActive = false;
    let torchEnabled = localStorage.getItem('survivor-torch') !== 'false'; // default ON

    // Expose toggle for nav button
    window.toggleTorchCursor = function() {
        torchEnabled = !torchEnabled;
        localStorage.setItem('survivor-torch', torchEnabled ? 'true' : 'false');
        if (!torchEnabled) {
            particles.length = 0;
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            glow.style.opacity = '0';
        }
        if (typeof updateTorchIcon === 'function') updateTorchIcon(torchEnabled);
    };

    document.addEventListener('mousemove', function(e) {
        mouseX = e.clientX;
        mouseY = e.clientY;
        if (!mouseActive) {
            mouseActive = true;
            if (torchEnabled) glow.style.opacity = '1';
        }
    });
    document.addEventListener('mouseleave', function() {
        mouseActive = false;
        glow.style.opacity = '0';
    });

    // Cartoon flame palette — yellow-gold inner, orange outer, red tips
    const fireColors = [
        { r: 255, g: 220, b: 80 },   // yellow-gold (inner core)
        { r: 255, g: 180, b: 40 },   // golden orange
        { r: 250, g: 140, b: 25 },   // warm orange
        { r: 235, g: 100, b: 15 },   // deep orange
        { r: 210, g: 60, b: 10 },    // red-orange
        { r: 160, g: 35, b: 5 },     // dark red
        { r: 80, g: 15, b: 2 },      // ember
    ];

    function lerpColor(life) {
        const t = (1 - life) * (fireColors.length - 1);
        const i = Math.min(Math.floor(t), fireColors.length - 2);
        const f = t - i;
        const a = fireColors[i], b = fireColors[i + 1];
        return { r: a.r + (b.r - a.r) * f, g: a.g + (b.g - a.g) * f, b: a.b + (b.b - a.b) * f };
    }

    const particles = [];
    const MAX_PARTICLES = 50;
    let time = 0;
    let spawnAccum = 0;

    // Slow dreamy sway
    function flameSway(t) {
        return Math.sin(t * 0.1) * 1.0 + Math.sin(t * 0.18) * 0.5;
    }

    function spawnParticles(dt) {
        if (!mouseActive || !torchEnabled) return;

        spawnAccum += dt;
        if (spawnAccum < 0.05) return; // ~20 spawns/sec
        spawnAccum = 0;

        const ox = mouseX + 4;
        const oy = mouseY + 2;

        // CORE tongues — fat, tall, bright, slow-moving base of flame
        if (particles.length < MAX_PARTICLES) {
            particles.push({
                x: ox + (Math.random() - 0.5) * 6,
                y: oy,
                vx: (Math.random() - 0.5) * 0.03,
                vy: -(0.08 + Math.random() * 0.12),
                life: 1,
                decay: 0.0015 + Math.random() * 0.001,
                width: 8 + Math.random() * 5,
                height: 18 + Math.random() * 12,
                wobblePhase: Math.random() * Math.PI * 2,
                wobbleAmp: 0.3 + Math.random() * 0.4,
                layer: 'core',
            });
        }

        // BODY tongues — medium, drift upward
        if (particles.length < MAX_PARTICLES) {
            particles.push({
                x: ox + (Math.random() - 0.5) * 10,
                y: oy - 4 - Math.random() * 8,
                vx: (Math.random() - 0.5) * 0.05,
                vy: -(0.12 + Math.random() * 0.18),
                life: 1,
                decay: 0.002 + Math.random() * 0.0015,
                width: 6 + Math.random() * 4,
                height: 14 + Math.random() * 10,
                wobblePhase: Math.random() * Math.PI * 2,
                wobbleAmp: 0.5 + Math.random() * 0.6,
                layer: 'body',
            });
        }

        // TIP tongues — narrow, tall, drift further up
        if (Math.random() < 0.5 && particles.length < MAX_PARTICLES) {
            particles.push({
                x: ox + (Math.random() - 0.5) * 6,
                y: oy - 12 - Math.random() * 12,
                vx: (Math.random() - 0.5) * 0.08,
                vy: -(0.15 + Math.random() * 0.2),
                life: 1,
                decay: 0.003 + Math.random() * 0.002,
                width: 3 + Math.random() * 3,
                height: 10 + Math.random() * 10,
                wobblePhase: Math.random() * Math.PI * 2,
                wobbleAmp: 0.8 + Math.random() * 1.0,
                layer: 'tip',
            });
        }

        // WISP — rare curling lick off the top
        if (Math.random() < 0.06 && particles.length < MAX_PARTICLES) {
            const dir = Math.random() < 0.5 ? -1 : 1;
            particles.push({
                x: ox + dir * (2 + Math.random() * 4),
                y: oy - 20 - Math.random() * 10,
                vx: dir * (0.08 + Math.random() * 0.12),
                vy: -(0.2 + Math.random() * 0.25),
                life: 1,
                decay: 0.005 + Math.random() * 0.003,
                width: 2 + Math.random() * 2,
                height: 8 + Math.random() * 8,
                wobblePhase: Math.random() * Math.PI * 2,
                wobbleAmp: 1.2 + Math.random() * 1.5,
                layer: 'wisp',
            });
        }
    }

    function update(dt) {
        const sway = flameSway(time);
        for (let i = particles.length - 1; i >= 0; i--) {
            const p = particles[i];
            p.life -= p.decay;
            if (p.life <= 0) { particles.splice(i, 1); continue; }

            // Slow wobble
            p.wobblePhase += dt * (0.15 + p.wobbleAmp * 0.08);
            const wobble = Math.sin(p.wobblePhase) * p.wobbleAmp;

            // Gentle sway
            const swayInfluence = p.layer === 'core' ? 0.1 : p.layer === 'body' ? 0.25 : 0.5;
            p.x += p.vx + wobble * dt * 0.3 + sway * swayInfluence * dt * 0.04;
            p.y += p.vy;
            p.vy *= 0.999;

            // Narrow as it rises
            const age = 1 - p.life;
            p.x += ((mouseX + 4) - p.x) * age * 0.003;

            // Shrink width faster than height — tongues get pointy
            p.width *= 0.9985;
            p.height *= 0.9995;
        }
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        if (!torchEnabled) return;

        ctx.globalCompositeOperation = 'lighter';

        // Draw outer layers first, core on top (bright center)
        const order = { wisp: 0, tip: 1, body: 2, core: 3 };
        particles.sort((a, b) => (order[a.layer] || 0) - (order[b.layer] || 0));

        for (const p of particles) {
            const color = lerpColor(p.life);
            let alpha;
            if (p.layer === 'core') {
                alpha = p.life * 0.7;
            } else if (p.layer === 'body') {
                alpha = p.life * 0.55;
            } else if (p.layer === 'tip') {
                alpha = p.life * 0.45;
            } else {
                alpha = p.life * 0.35;
            }

            const w = Math.max(p.width, 0.5);
            const h = Math.max(p.height, 1);

            ctx.save();
            ctx.translate(p.x, p.y);

            // Gradient runs from bottom (bright) to top (transparent) — flame tongue shape
            const grad = ctx.createRadialGradient(0, h * 0.3, 0, 0, -h * 0.1, Math.max(w, h));
            grad.addColorStop(0, `rgba(${color.r|0},${color.g|0},${color.b|0},${alpha})`);
            grad.addColorStop(0.35, `rgba(${color.r|0},${color.g|0},${color.b|0},${alpha * 0.6})`);
            grad.addColorStop(0.7, `rgba(${color.r|0},${color.g|0},${color.b|0},${alpha * 0.15})`);
            grad.addColorStop(1, `rgba(${color.r|0},${color.g|0},${color.b|0},0)`);
            ctx.fillStyle = grad;

            // Draw a vertically stretched ellipse — flame tongue
            ctx.beginPath();
            ctx.ellipse(0, 0, w, h, 0, 0, Math.PI * 2);
            ctx.fill();

            ctx.restore();
        }
        ctx.globalCompositeOperation = 'source-over';
    }

    let lastTime = performance.now();
    function loop(now) {
        const dt = Math.min((now - lastTime) / 1000, 0.05);
        lastTime = now;
        time += dt;

        spawnParticles(dt);
        update(dt);
        draw();

        if (torchEnabled) {
            glow.style.left = (mouseX + 4) + 'px';
            glow.style.top = (mouseY - 18) + 'px';
        }

        requestAnimationFrame(loop);
    }
    requestAnimationFrame(loop);
})();

// Page transition loading overlay
document.addEventListener('DOMContentLoaded', function() {
    // Show loading on internal link clicks
    document.querySelectorAll('a[href^="/"]').forEach(link => {
        link.addEventListener('click', function(e) {
            // Skip for buttons, dropdown items with hash, etc.
            if (this.getAttribute('href') === '#' || this.getAttribute('target') === '_blank') return;
            const overlay = document.getElementById('loadingOverlay');
            if (overlay) {
                setTimeout(() => overlay.classList.add('active'), 150);
            }
        });
    });

    // Hide on page load (in case of back navigation)
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) overlay.classList.remove('active');
});

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

// Sortable tables — add class="sortable" to any <table>
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('table.sortable').forEach(table => {
        const headers = table.querySelectorAll('th');
        headers.forEach((header, colIndex) => {
            header.addEventListener('click', () => {
                const tbody = table.querySelector('tbody');
                const rows = Array.from(tbody.querySelectorAll('tr'));
                const isAsc = header.classList.contains('sort-asc');

                // Reset all headers
                headers.forEach(h => h.classList.remove('sort-asc', 'sort-desc'));
                header.classList.add(isAsc ? 'sort-desc' : 'sort-asc');

                rows.sort((a, b) => {
                    const aText = a.cells[colIndex]?.textContent.trim() || '';
                    const bText = b.cells[colIndex]?.textContent.trim() || '';
                    const aNum = parseFloat(aText);
                    const bNum = parseFloat(bText);

                    // Numeric sort if both are numbers
                    if (!isNaN(aNum) && !isNaN(bNum)) {
                        return isAsc ? bNum - aNum : aNum - bNum;
                    }
                    // String sort
                    return isAsc ? bText.localeCompare(aText) : aText.localeCompare(bText);
                });

                rows.forEach(row => tbody.appendChild(row));
            });
        });
    });
});

// Random season button
function goToRandomPlayer() {
    const seasons = Array.from({length: 39}, (_, i) => i + 1);
    const randomSeason = seasons[Math.floor(Math.random() * seasons.length)];
    window.location.href = `/castaways?season=${randomSeason}`;
}

// Discover a random player via API
function discoverRandomPlayer() {
    fetch('/api/random-player')
        .then(r => r.json())
        .then(data => {
            if (data.url) window.location.href = data.url;
        })
        .catch(() => goToRandomPlayer());
}

// On castaways page: scroll to and highlight a player from URL hash
(function() {
    if (!window.location.hash || !window.location.hash.startsWith('#player-')) return;
    const playerName = decodeURIComponent(window.location.hash.replace('#player-', ''));
    // Wait for DOM and any animations
    setTimeout(function() {
        const cards = document.querySelectorAll('.castaway-card');
        for (const card of cards) {
            if (card.dataset.name === playerName) {
                card.scrollIntoView({ behavior: 'smooth', block: 'center' });
                card.style.outline = '3px solid var(--torch-orange)';
                card.style.outlineOffset = '4px';
                card.style.transition = 'outline-color 3s';
                // Auto-open voting history
                const btn = card.querySelector('.btn-details');
                if (btn) btn.click();
                // Fade out highlight after 3s
                setTimeout(function() {
                    card.style.outlineColor = 'transparent';
                }, 3000);
                break;
            }
        }
    }, 500);
})();
