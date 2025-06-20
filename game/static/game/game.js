console.log('Grid JS loaded');
const gridElement = document.getElementById('grid');
const fallback = document.getElementById('grid-fallback');
const ROWS = 20, COLS = 20;
let grid = [];
let mode = 'start';
let startCell = null, goalCell = null;

function createGrid() {
    if (fallback) fallback.style.display = 'none';
    gridElement.innerHTML = '';
    grid = [];
    for (let r = 0; r < ROWS; r++) {
        let row = [];
        for (let c = 0; c < COLS; c++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            cell.dataset.row = r;
            cell.dataset.col = c;
            cell.addEventListener('click', () => handleCellClick(cell));
            gridElement.appendChild(cell);
            row.push(cell);
        }
        grid.push(row);
    }
    console.log('Grid created with', ROWS, 'rows and', COLS, 'cols');
}

function handleCellClick(cell) {
    if (mode === 'start') {
        if (startCell) startCell.classList.remove('start');
        cell.classList.add('start');
        startCell = cell;
        mode = 'goal';
    } else if (mode === 'goal') {
        if (goalCell) goalCell.classList.remove('goal');
        cell.classList.add('goal');
        goalCell = cell;
        mode = 'obstacle';
    } else if (mode === 'obstacle') {
        cell.classList.toggle('obstacle');
    }
}

function clearGrid() {
    createGrid();
    mode = 'start';
    startCell = null;
    goalCell = null;
}

document.addEventListener('DOMContentLoaded', function() {
    createGrid();
    window.addEventListener('resize', createGrid);
});
