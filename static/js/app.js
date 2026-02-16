// Survivor Bot - Main JavaScript

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

// Random player button
function goToRandomPlayer() {
    const seasons = Array.from({length: 39}, (_, i) => i + 1);
    const randomSeason = seasons[Math.floor(Math.random() * seasons.length)];
    window.location.href = `/castaways?season=${randomSeason}`;
}
