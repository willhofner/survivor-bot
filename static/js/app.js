// Survivor Bot - Main JavaScript

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
