"use strict";
document.addEventListener('DOMContentLoaded', () => {
    const init = window.INIT_BOARD;
    const boardId = init.id;
    let rows = init.rows;
    let cols = init.cols;
    const initialDots = init.dots;
    const gridContainer = document.getElementById('grid-container');
    const save = document.getElementById('save-board');
    const reset = document.getElementById('reset-board');
    const regen = document.getElementById('regenerate');
    const placedDots = [];
    const colorCount = new Map();
    function buildGrid(r, c) {
        gridContainer.innerHTML = '';
        gridContainer.style.setProperty('--rows', String(r));
        gridContainer.style.setProperty('--cols', String(c));
        for (let row = 1; row <= r; row++) {
            for (let col = 1; col <= c; col++) {
                const cell = document.createElement('div');
                cell.classList.add('grid-cell');
                cell.dataset.row = String(row);
                cell.dataset.col = String(col);
                gridContainer.appendChild(cell);
            }
        }
    }
    buildGrid(rows, cols);
    initialDots.forEach(dot => {
        placeDot(dot.row, dot.col, dot.color);
    });
    regen.addEventListener('click', () => {
        const r = parseInt(document.getElementById('id_rows').value, 10);
        const c = parseInt(document.getElementById('id_cols').value, 10);
        placedDots.length = 0;
        colorCount.clear();
        buildGrid(r, c);
        rows = r;
        cols = c;
    });
    const pickerContainer = document.getElementById('color-picker-container');
    let activeH = 0;
    let activeColor = 'hsl(0,100%,50%)';
    const hueCanvas = document.createElement('canvas');
    hueCanvas.id = 'hue-slider-canvas';
    hueCanvas.width = 200;
    hueCanvas.height = 20;
    pickerContainer.appendChild(hueCanvas);
    const hueCtx = hueCanvas.getContext('2d');
    function drawHue() {
        const grad = hueCtx.createLinearGradient(0, 0, hueCanvas.width, 0);
        for (let i = 0; i <= 360; i += 60)
            grad.addColorStop(i / 360, `hsl(${i},100%,50%)`);
        hueCtx.fillStyle = grad;
        hueCtx.fillRect(0, 0, hueCanvas.width, hueCanvas.height);
    }
    drawHue();
    hueCanvas.addEventListener('click', e => {
        const x = e.clientX - hueCanvas.getBoundingClientRect().left;
        const data = hueCtx.getImageData(x, 1, 1, 1).data;
        const hue = Math.round((Math.atan2(Math.sqrt(3) * (data[1] - data[2]), 2 * data[0] - data[1] - data[2]) * 180 / Math.PI + 360) % 360);
        activeH = hue;
        activeColor = `hsl(${activeH},100%,50%)`;
        previewBox.style.background = activeColor;
    });
    const previewBox = document.createElement('div');
    previewBox.id = 'color-preview';
    previewBox.style.cssText = 'width:32px;height:32px;border:1px solid #000;margin-left:8px;';
    previewBox.style.background = activeColor;
    pickerContainer.appendChild(previewBox);
    function placeDot(row, col, color) {
        const sel = `.grid-cell[data-row="${row}"][data-col="${col}"]`;
        const cell = document.querySelector(sel);
        if (!cell || cell.querySelector('.dot-circle'))
            return;
        const count = colorCount.get(color) || 0;
        if (count >= 2)
            return;
        const dotEl = document.createElement('div');
        dotEl.classList.add('dot-circle');
        dotEl.style.background = color;
        cell.appendChild(dotEl);
        placedDots.push({ row, col, color });
        colorCount.set(color, count + 1);
    }
    gridContainer.addEventListener('click', e => {
        const cell = e.target.closest('.grid-cell');
        if (!cell)
            return;
        const row = parseInt(cell.dataset.row, 10);
        const col = parseInt(cell.dataset.col, 10);
        placeDot(row, col, activeColor);
    });
    reset.addEventListener('click', () => {
        document.querySelectorAll('.dot-circle')
            .forEach(dot => dot.remove());
        placedDots.length = 0;
        colorCount.clear();
    });
    save.addEventListener('click', () => {
        var _a;
        const payload = {
            id: boardId,
            rows: rows,
            cols: cols,
            dots: placedDots,
        };
        console.log('Save payload', payload);
        const csrftoken = ((_a = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))) === null || _a === void 0 ? void 0 : _a.split('=')[1]) || '';
        fetch(`/boards/${payload.id}/save/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify(payload),
        })
            .then(res => {
            if (!res.ok)
                throw new Error('Network response was not OK');
            return res.json();
        })
            .then(data => {
            alert('Plansza zapisana pomyślnie!');
        })
            .catch(err => {
            console.error('Save error:', err);
            alert('Wystąpił błąd podczas zapisu.');
        });
    });
});
//# sourceMappingURL=board-interaction.js.map