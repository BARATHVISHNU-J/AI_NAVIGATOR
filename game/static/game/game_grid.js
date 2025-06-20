const ROWS = 10, COLS = 10;
const gridTable = document.getElementById('grid-table');
let mode = 'start';
let startCell = null, goalCell = null;
let gridState = Array.from({ length: ROWS }, () => Array(COLS).fill('empty'));
let lastAlgorithm = null;
let astarPath = [];
let dijkstraPath = [];

const images = {
    start: '/static/game/start.png',
    goal: '/static/game/goal.png',
    obstacle: '/static/game/obstacle.png',
};

let algorithmRunSinceLastClear = false;

function renderGrid() {
    gridTable.innerHTML = '';
    for (let r = 0; r < ROWS; r++) {
        const row = document.createElement('tr');
        for (let c = 0; c < COLS; c++) {
            const cell = document.createElement('td');
            cell.style.padding = '0';
            cell.style.border = 'none';
            const btn = document.createElement('button');
            btn.className = 'grid-cell-btn';
            btn.dataset.row = r;
            btn.dataset.col = c;
            btn.onclick = (e) => handleCellClick(r, c, btn, e);
            btn.oncontextmenu = (e) => handleCellRightClick(r, c, btn, e);
            // Set cell state classes and images
            if (gridState[r][c] === 'start') {
                btn.classList.add('start');
                btn.innerHTML = `<img src="${images.start}" alt="S">`;
            } else if (gridState[r][c] === 'goal') {
                btn.classList.add('goal');
                btn.innerHTML = `<img src="${images.goal}" alt="G">`;
            } else if (gridState[r][c] === 'obstacle') {
                btn.classList.add('obstacle');
                btn.innerHTML = `<img src="${images.obstacle}" alt="#">`;
            } else if (gridState[r][c] === 'path-astar') {
                btn.classList.add('path-astar');
                btn.innerHTML = '';
            } else if (gridState[r][c] === 'path-dijkstra') {
                btn.classList.add('path-dijkstra');
                btn.innerHTML = '';
            } else if (gridState[r][c] === 'path-both') {
                btn.classList.add('path-both');
                btn.innerHTML = '';
            } else {
                btn.innerHTML = '';
            }
            cell.appendChild(btn);
            row.appendChild(cell);
        }
        gridTable.appendChild(row);
    }
}

function handleCellClick(r, c, btn, e) {
    if (e && e.button === 2) return; // Ignore right click here
    if (!startCell) {
        gridState[r][c] = 'start';
        startCell = [r, c];
        renderGrid();
        return;
    }
    if (!goalCell && gridState[r][c] !== 'start') {
        gridState[r][c] = 'goal';
        goalCell = [r, c];
        renderGrid();
        return;
    }
    if (gridState[r][c] === 'empty') {
        gridState[r][c] = 'obstacle';
    } else if (gridState[r][c] === 'obstacle') {
        gridState[r][c] = 'empty';
    }
    renderGrid();
}

function handleCellRightClick(r, c, btn, e) {
    e.preventDefault();
    if (gridState[r][c] === 'start') {
        gridState[r][c] = 'empty';
        startCell = null;
    } else if (gridState[r][c] === 'goal') {
        gridState[r][c] = 'empty';
        goalCell = null;
    } else if (gridState[r][c] === 'obstacle') {
        gridState[r][c] = 'empty';
    }
    renderGrid();
}

function clearGrid() {
    if (algorithmRunSinceLastClear) {
        fetch('/api/increment_games_played/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
        })
        .then(res => res.json())
        .then(data => {
            // Optionally handle response
        });
        algorithmRunSinceLastClear = false;
    }
    gridState = Array.from({ length: ROWS }, () => Array(COLS).fill('empty'));
    startCell = null;
    goalCell = null;
    mode = 'start';
    renderGrid();
}

function getGridData() {
    let grid = [];
    for (let r = 0; r < ROWS; r++) {
        let row = [];
        for (let c = 0; c < COLS; c++) {
            row.push(gridState[r][c]);
        }
        grid.push(row);
    }
    return grid;
}

let lastUpdated = null;

// Ensure stats variables are always defined on window
if (typeof window !== 'undefined') {
    if (typeof window.lastAStarLength === 'undefined') window.lastAStarLength = 0;
    if (typeof window.lastDijkstraLength === 'undefined') window.lastDijkstraLength = 0;
}

function runAStar() {
    if (!startCell || !goalCell) {
        alert('Please select start and goal cells.');
        return;
    }
    fetch('/run_astar/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({
            grid: getGridData(),
            start: [startCell[1], startCell[0]],
            goal: [goalCell[1], goalCell[0]],
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success && data.path && data.path.length > 0) {
            astarPath = data.path;
            lastUpdated = 'astar';
            if (typeof window !== 'undefined') {
                window.lastAStarLength = data.path.length;
            }
            algorithmRunSinceLastClear = true;
            showBothPaths();
        } else {
            alert('Goal cannot be reached: No path exists from start to goal.');
        }
    });
}

function runDijkstra() {
    if (!startCell || !goalCell) {
        alert('Please select start and goal cells.');
        return;
    }
    fetch('/run_dijkstra/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({
            grid: getGridData(),
            start: [startCell[1], startCell[0]],
            goal: [goalCell[1], goalCell[0]],
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success && data.path && data.path.length > 0) {
            dijkstraPath = data.path;
            lastUpdated = 'dijkstra';
            if (typeof window !== 'undefined') {
                window.lastDijkstraLength = data.path.length;
            }
            algorithmRunSinceLastClear = true;
            showBothPaths();
        } else {
            alert('Goal cannot be reached: No path exists from start to goal.');
        }
    });
}

function showBothPaths() {
    // Remove only previous path cells, but keep both paths if present
    for (let r = 0; r < ROWS; r++) {
        for (let c = 0; c < COLS; c++) {
            if (gridState[r][c] === 'path-astar' || gridState[r][c] === 'path-dijkstra' || gridState[r][c] === 'path-both') {
                gridState[r][c] = 'empty';
            }
        }
    }
    // Mark the other algorithm's path as static (for overlay), but do NOT mark the current one yet
    if (lastUpdated === 'astar') {
        // Only mark dijkstraPath statically
        dijkstraPath.forEach(([col, row]) => {
            if (gridState[row][col] === 'empty') gridState[row][col] = 'path-dijkstra';
        });
        renderGrid();
        animatePathWithOverlay(astarPath, 'astar');
    } else if (lastUpdated === 'dijkstra') {
        // Only mark astarPath statically
        astarPath.forEach(([col, row]) => {
            if (gridState[row][col] === 'empty') gridState[row][col] = 'path-astar';
        });
        renderGrid();
        animatePathWithOverlay(dijkstraPath, 'dijkstra');
    }
}

// Animate the path cell-by-cell, keep path fixed, and overlay if needed
async function animatePathWithOverlay(path, algorithm) {
    // Always use the same slow delay for both algorithms for smooth trace
    let delay = 220;
    for (let i = 0; i < path.length; i++) {
        const [col, row] = path[i];
        const cellBtn = document.querySelector(`#grid-table button[data-row='${row}'][data-col='${col}']`);
        if (!cellBtn) continue;
        cellBtn.style.transition = 'background 0.45s cubic-bezier(0.4,0,0.2,1), border 0.45s cubic-bezier(0.4,0,0.2,1)';
        let otherType = (algorithm === 'astar') ? 'path-dijkstra' : 'path-astar';
        let bothType = 'path-both';
        if (gridState[row][col] === otherType || cellBtn.classList.contains(otherType)) {
            gridState[row][col] = bothType;
            cellBtn.classList.remove('path-astar', 'path-dijkstra');
            cellBtn.classList.add(bothType);
        } else {
            gridState[row][col] = `path-${algorithm}`;
            cellBtn.classList.remove('path-astar', 'path-dijkstra', 'path-both');
            cellBtn.classList.add(`path-${algorithm}`);
        }
        await new Promise(res => setTimeout(res, delay));
    }
}

function getCSRFToken() {
    let name = 'csrftoken';
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Ensure grid renders on page load
window.addEventListener('DOMContentLoaded', function() {
    if (typeof renderGrid === 'function') {
        renderGrid();
    }
});

// Increment games played if navigating away after algorithm run
window.addEventListener('beforeunload', function (e) {
    if (algorithmRunSinceLastClear) {
        // Use navigator.sendBeacon for reliability on unload
        const csrfToken = getCSRFToken();
        const url = '/api/increment_games_played/';
        const data = new Blob([JSON.stringify({})], { type: 'application/json' });
        if (csrfToken) {
            navigator.sendBeacon(url, data);
        }
        algorithmRunSinceLastClear = false;
    }
});
