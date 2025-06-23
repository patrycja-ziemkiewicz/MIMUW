"use strict";
document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('map-container');
    const inputX = document.getElementById('id_x');
    const inputY = document.getElementById('id_y');
    if (!container || !inputX || !inputY) {
        console.error('Nie znaleziono elementów mapy lub pól formularza');
        return;
    }
    container.addEventListener('click', (event) => {
        const rect = container.getBoundingClientRect();
        const offsetX = event.clientX - rect.left;
        const offsetY = event.clientY - rect.top;
        inputX.value = offsetX.toFixed(2);
        inputY.value = offsetY.toFixed(2);
        const marker = document.createElement('div');
        marker.style.position = 'absolute';
        marker.style.left = `${offsetX - 5}px`;
        marker.style.top = `${offsetY - 5}px`;
        marker.style.width = '10px';
        marker.style.height = '10px';
        marker.style.border = '2px solid red';
        marker.style.borderRadius = '50%';
        marker.style.pointerEvents = 'none';
        container.appendChild(marker);
        setTimeout(() => marker.remove(), 500);
    });
    const svg = document.querySelector('#map-svg');
    if (!svg) {
        console.error('Nie znaleziono elementu SVG mapy');
        return;
    }
    let highlighted = null;
    const points = Array.from(svg.querySelectorAll('.route-point'));
    points.forEach(pt => {
        pt.style.cursor = 'pointer';
        pt.addEventListener('mouseenter', () => {
            if (highlighted && highlighted !== pt) {
                highlighted.removeAttribute('stroke');
                highlighted.removeAttribute('stroke-width');
            }
            pt.setAttribute('stroke', 'yellow');
            pt.setAttribute('stroke-width', '3');
            highlighted = pt;
        });
        pt.addEventListener('mouseleave', () => {
            pt.removeAttribute('stroke');
            pt.removeAttribute('stroke-width');
            highlighted = null;
        });
    });
});
//# sourceMappingURL=map-interactions.js.map