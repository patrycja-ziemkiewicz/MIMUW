

interface Coord { row: number; col: number; }
interface Dot   { row: number; col: number; color: string; }

document.addEventListener('DOMContentLoaded', () => {
  
  const grid = document.getElementById('grid-container') as HTMLElement;
  const saveBtn = document.getElementById('save-board') as HTMLButtonElement;
  const resetBtn = document.getElementById('reset-path') as HTMLButtonElement;
  const init = (window as any).INIT_BOARD as {
    id: number;
    rows: number;
    cols: number;
    dots: Dot[];
    paths: Record<string, Coord[]>;
  };
  const boardId = init.id;
  const rows = init.rows;
  const cols = init.cols;
  const dots = init.dots;
  const initialPaths = init.paths;

  
  grid.style.setProperty('--rows', String(rows));
  grid.style.setProperty('--cols', String(cols));

  const cellMap = new Map<string, HTMLElement>();
  const paths: Record<string, Coord[]> = {};
  let activeColor: string | null = null;
  let activePath: Coord[] = [];

  const cellKey = (r: number, c: number) => `${r},${c}`;


  for (let r = 1; r <= rows; r++) {
    for (let c = 1; c <= cols; c++) {
      const cell = document.createElement('div');
      cell.classList.add('grid-cell');
      cell.dataset.row = String(r);
      cell.dataset.col = String(c);
      cell.addEventListener('click', onCellClick);
      grid.appendChild(cell);
      cellMap.set(cellKey(r, c), cell);
    }
  }

  
  dots.forEach(dot => {
    const cell = cellMap.get(cellKey(dot.row, dot.col))!;
    cell.dataset.dotColor = dot.color;
    const dotEl = document.createElement('div');
    dotEl.classList.add('dot-circle');
    dotEl.style.background = dot.color;
    cell.appendChild(dotEl);
  });

  for (const color in initialPaths) {
    if (!Object.prototype.hasOwnProperty.call(initialPaths, color)) continue;
    const coords = initialPaths[color];
    paths[color] = coords.slice();
    coords.forEach(({ row, col }) => {
        const cell = cellMap.get(cellKey(row, col)) as HTMLElement;
        markCell(cell, color);
        });
    }

  resetBtn.addEventListener('click', resetBoard);

  function onCellClick(e: MouseEvent) {
    const cell = e.currentTarget as HTMLElement;
    const r = parseInt(cell.dataset.row!, 10);
    const c = parseInt(cell.dataset.col!, 10);
    const dotColor = cell.dataset.dotColor || null;

    if (!activeColor) {
      if (dotColor && !paths[dotColor]) {
        activeColor = dotColor;
        activePath = [{ row: r, col: c }];
        markCell(cell, activeColor);
      }
      return;
    }

    if (dotColor === activeColor && activePath.length > 0) {
      const last = activePath[activePath.length - 1];
      if (isAdjacent(last, { row: r, col: c })) {
        activePath.push({ row: r, col: c });
        markCell(cell, activeColor);
        paths[activeColor] = [...activePath];
        activeColor = null;
        activePath = [];
        return;
      }
    }

    const last = activePath[activePath.length - 1];
    const occupied = cell.dataset.pathColor || cell.dataset.dotColor;
    if (isAdjacent(last, { row: r, col: c }) && !occupied) {
      activePath.push({ row: r, col: c });
      markCell(cell, activeColor!);
      return;
    }

    resetActivePath();
  }

  function isAdjacent(a: Coord, b: Coord) {
    return Math.abs(a.row - b.row) + Math.abs(a.col - b.col) === 1;
  }

  function markCell(cell: HTMLElement, color: string) {
    cell.dataset.pathColor = color;
    cell.style.background = color;
  }

  function resetActivePath() {
    activePath.forEach(({ row, col }) => {
      const cell = cellMap.get(cellKey(row, col))!;
      delete cell.dataset.pathColor;
      cell.removeAttribute('style');
    });
    activeColor = null;
    activePath = [];
  }

  function resetBoard() {
    cellMap.forEach(cell => {
      delete cell.dataset.pathColor;
      cell.style.background = '';
    });
    Object.keys(paths).forEach(color => delete paths[color]);
    activeColor = null;
    activePath = [];
  }

  saveBtn.addEventListener('click', () => {
    const csrftoken: string = document.cookie
      .split('; ')
      .find(row => row.startsWith('csrftoken='))
      ?.split('=')[1] || '';

    fetch(`/boards/${boardId}/save_path/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
      },
      body: JSON.stringify({ paths })
    })
      .then(res => res.json())
      .then(() => alert('Ścieżki zapisane!'))
      .catch(() => alert('Błąd zapisu.'));
  });
});
